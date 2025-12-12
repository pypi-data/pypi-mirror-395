"""TileDB File Assets

The functions of this module allow a TileDB File to be downloaded to a
local filesystem, or uploaded from a local filesystem to TileDB so that
it becomes a catalog asset.

"""

import logging
import mimetypes
import pathlib
from os import PathLike
from typing import BinaryIO, Optional, Union
from xml.etree import ElementTree as ET

import urllib3

import tiledb
from tiledb.client import client
from tiledb.client import folders
from tiledb.client._common.api_v4 import AssetsApi
from tiledb.client._common.api_v4 import FilesApi
from tiledb.client.folders import Teamspace

from .assets import AssetType
from .assets import _normalize_ids
from .rest_api import ApiException

logger = logging.getLogger(__name__)


class FilesError(tiledb.TileDBError):
    """Raised when a file transfer operation fails."""


class FileUploaderError(Exception):
    """When file upload fails."""


class _FileUploader:
    def __init__(self, file, content_type=None, pool_manager=None):
        self.file = file
        self.content_type = content_type
        self.chunksize = 8000000
        self.http = pool_manager or urllib3.PoolManager()
        self.file_obj = None
        self.file_len = None
        self.file_name = None
        self.upload_id = None
        self.upload_path = None
        self.parts = []

    def begin(self, workspace, teamspace, path):
        """Begin an upload.

        This method will make a get_asset() request for `path`, but does
        not put any file bytes.

        `path` may be a path like /a/b/c or an asset_id. In the second
        case, we'll require that `path` identifies a folder.  In the
        first case, we'll require that `path` identifies a folder, or
        a new asset within a folder.
        """
        # Determine the length of the file and its default name.
        if hasattr(self.file, "read"):
            self.file_obj = self.file
            if hasattr(self.file, "name"):
                self.file_name = pathlib.Path(self.file.name).name
            else:
                self.file_name = None
            self.file_obj.seek(0, 2)
            self.file_len = self.file_obj.tell()
            self.file_obj.seek(0)
        elif isinstance(self.file, (str, PathLike)):
            file_path = pathlib.Path(self.file)
            self.file_name = file_path.name
            self.file_obj = file_path.open("rb")
            self.file_len = file_path.stat().st_size
        else:
            self.file_obj = memoryview(self.file)
            self.file_len = len(self.file_obj)
            self.file_name = None

        # Is there a folder at path or path.parent? We have to know up
        # front because the initiateMultipartUpload API won't complain
        # if the path is occupied.

        # Note: it's nonsensical to convert an asset_id to a Python Path
        # object, but it's useful for this implementation.  If we're
        # given an asset_id, we won't make it to the iteration of the
        # loop below.
        path_obj = pathlib.Path(path)

        for i, po in enumerate([path_obj, path_obj.parent]):
            logger.debug(
                "Checking the target path for a folder: path=%r, teamspace=%r",
                po,
                teamspace,
            )

            # If the path is a teamspace.
            if po.as_posix() in ["/", "."]:
                if i == 0:  # Original target path.
                    logger.debug(
                        "Teamspace at path, appending file name: path=%r, file_name=%r.",
                        po,
                        self.file_name,
                    )
                    if not self.file_name:
                        raise FileUploaderError(
                            "An unnamed sequence of bytes can not be uploaded."
                        )
                    path = po.joinpath(self.file_name).as_posix()

                # We've found the teamspace we are looking for.
                break

            try:
                folder = (
                    client.build(AssetsApi)
                    .get_asset(
                        workspace,
                        teamspace,
                        po.as_posix(),
                    )
                    .data
                )
            except ApiException as exc:
                if exc.status == 404:
                    # Check the parent in the next iteration.
                    continue
                elif exc.status < 500:
                    raise FileUploaderError("Invalid target path.") from exc
                else:
                    raise FileUploaderError("Failed to begin upload.") from exc
            else:
                if folder.type == AssetType.FOLDER:
                    if i == 0:  # Original target path.
                        logger.debug(
                            "Existing folder at path, appending file name: path=%r, file_name=%r.",
                            po,
                            self.file_name,
                        )
                        if not self.file_name:
                            raise FileUploaderError(
                                "An unnamed sequence of bytes can not be uploaded to a folder."
                            )
                        path = (
                            pathlib.Path(folder.path)
                            .joinpath(self.file_name)
                            .as_posix()
                        )
                    # We've found the folder we are looking for.
                    break
                else:
                    raise FileUploaderError("A file may only be uploaded to a folder.")

        else:
            # We found no folder in the target path.
            raise FileUploaderError("A file may only be uploaded to a folder.")

        if self.file_len > self.chunksize:
            server_address = client.config.config.host
            uri = f"{server_address}/v4/files/{workspace}/{teamspace}/{path.lstrip('/')}?uploads"
            logger.debug("Request to initiateMultipartUpload API: uri=%r", uri)
            resp = self.http.request("POST", uri, headers=client.config.config.api_key)
            self.upload_id = ET.fromstring(resp.data).find("UploadId").text

        self.upload_path = path

    def chunks(self):
        if isinstance(self.file_obj, memoryview):
            start = 0
            while dataslice := self.file_obj[start : start + self.chunksize]:
                yield dataslice.tobytes()
                start = start + self.chunksize
        else:
            while data := self.file_obj.read(self.chunksize):
                yield data

    def put_parts(self, workspace, teamspace):
        server_address = client.config.config.host
        headers = headers = client.config.config.api_key
        if self.content_type:
            headers.update({"Content-Type": self.content_type})

        if self.upload_id:  # is chunked.
            part_num = 1
            for data in self.chunks():
                headers.update({"Content-Length": len(data)})
                uri = f"{server_address}/v4/files/{workspace}/{teamspace}/{self.upload_path.lstrip('/')}?uploadId={self.upload_id}&partNumber={part_num}"
                logger.debug(
                    "Request to uploadPart API: uri=%r, headers=%r, len=%r",
                    uri,
                    headers,
                    len(data),
                )
                resp = self.http.request("PUT", uri, headers=headers, body=data)
                etag = resp.headers["ETag"]
                self.parts.append(etag.strip('"'))
                part_num = part_num + 1
        else:
            data = next(self.chunks())
            headers.update({"Content-Length": len(data)})
            uri = f"{server_address}/v4/files/{workspace}/{teamspace}/{self.upload_path.lstrip('/')}"
            logger.debug(
                "Putting single part: uri=%r, headers=%r, len=%r",
                uri,
                headers,
                len(data),
            )
            resp = self.http.request("PUT", uri, headers=headers, body=data)

    def finish(self, workspace, teamspace):
        if self.upload_id and self.parts:
            server_address = client.config.config.host
            uri = f"{server_address}/v4/files/{workspace}/{teamspace}/{self.upload_path.lstrip('/')}?uploadId={self.upload_id}"
            elem = ET.Element("CompleteMultipartUpload")
            for part_num, etag in enumerate(self.parts, start=1):
                part = ET.SubElement(elem, "Part")
                n = ET.SubElement(part, "PartNumber")
                n.text = str(part_num)
                e = ET.SubElement(part, "ETag")
                e.text = str(etag)

            doc = ET.tostring(elem, encoding="utf-8", xml_declaration=True)

            logger.debug(
                "Request to completeMultipartUpload API: uri=%r, doc=%r", uri, doc
            )
            self.http.request(
                "POST", uri, headers=client.config.config.api_key, body=doc
            )


def download_file(
    path: str,
    file: Union[BinaryIO, str],
    *,
    teamspace: Union[Teamspace, str],
) -> None:
    """Download a file from a teamspace.

    Parameters
    ----------
    path : str
        The path of the file to be downloaded.
    file : BinaryIO or str
        The file to be written.
    teamspace : Teamspace or str
        The teamspace to which the downloaded file belongs.

    Returns
    -------
    None

    Raises
    ------
    FilesError:
        If the file download failed.

    Examples
    --------
    >>> files.download_file(
    ...     "teamspace",
    ...     "README.md",
    ...     open("README.md", "wb"),
    ... )

    Notes
    -----
    The current implementation makes a copy of the file in memory
    before writing to the output file.

    """
    teamspace_id, path_id = _normalize_ids(teamspace, path)
    try:
        api_instance = client.client.build(FilesApi)
        resp = api_instance.file_get(
            client.get_workspace_id(),
            teamspace_id,
            path_id,
            _preload_content=False,
        )
    except ApiException as exc:
        raise FilesError("The file download failed.") from exc
    else:
        file.write(resp.read())


def upload_file(
    file: Union[BinaryIO, PathLike, bytes, bytearray, memoryview],
    path: Union[object, str],
    *,
    teamspace: Optional[Union[Teamspace, str]] = None,
    content_type: Optional[str] = None,
) -> None:
    """Upload a file to a teamspace.

    Parameters
    ----------
    file : BinaryIO, PathLike, or Buffer
        The file to be uploaded.
    path : str or object
        The TileDB path at which the file is to be registered. May be
        a path relative to a teamspace, a `Folder` or `Asset` instance,
        or an absolute "tiledb" URI. If the path to a folder is
        provided, the basename of the file will be appended to form
        a full asset path.
    teamspace : Teamspace or str, optional
        The teamspace to which the file will be registered, specified
        by object or id. If not provided, the `path` parameter is
        queried for a teamspace id.
    content_type: str, optional
        The content type of the uploaded file.

    Raises
    ------
    FilesError:
        If the file upload failed.

    Examples
    --------
    >>> folder = folders.create_folder(
    ...     "files",
    ...     teamspace="teamspace",
    ...     exists_ok=True,
    ... )
    >>> upload_file(
    ...     open("README.md", "rb"),
    ...     "files",
    ...     teamspace="teamspace",
    ...     content_type="text/markdown",
    ... )

    This creates a file asset at path "files/README.md" in the teamspace
    named "teamspace". The file's basename has been used to construct
    the full path.

    If you like, you can pass a Folder or Asset object instead of a path
    string and get the same result.

    >>> upload_file(
    ...     open("README.md", "rb"),
    ...     folder,
    ...     teamspace="teamspace",
    ...     content_type="text/markdown",
    ... )

    If you like, you can pass a Folder or Asset object instead of a path
    string and get the same result.

    >>> register_udf(get_tiledb_version, folder)

    A file can also be registered to a specific absolute "tiledb" URI
    that specifies a different name.

    >>> files.upload_file(
    ...     open("README.md", "rb"),
    ...     "tiledb://workspace/teamspace/files/index.md",
    ...     content_type="text/markdown",
    ... )

    """
    teamspace_id, path_id = _normalize_ids(teamspace, path)
    workspace = client.get_workspace_id()

    if not content_type:
        try:
            content_type, _ = mimetypes.guess_type(file)
        except (TypeError, UnicodeDecodeError):
            content_type = None

    uploader = _FileUploader(
        file,
        content_type=content_type or "application/octet-stream",
    )

    try:
        uploader.begin(workspace, teamspace_id, path_id)
        uploader.put_parts(workspace, teamspace_id)
        uploader.finish(workspace, teamspace_id)
    except FileUploaderError as exc:
        raise FilesError("Failed to upload file.") from exc


def upload_tree(
    source: PathLike,
    path: Union[object, str],
    *,
    teamspace: Optional[Union[Teamspace, str]] = None,
) -> None:
    """Recursively upload an entire directory tree to a path.

    This function has the same semantics of `pathlib.Path.copy()` or
    `shutil.copytree()`. All intermediate folders needed to contain path
    will also be created by default.

    Parameters
    ----------
    source : PathLike
        The directory tree to be uploaded.
    path : str or object
        The TileDB path at which the directory tree is to be registered. May be
        a path relative to a teamspace, a `Folder` or `Asset` instance,
        or an absolute "tiledb" URI.
    teamspace : Teamspace or str, optional
        The teamspace to which the file will be registered, specified
        by object or id. If not provided, the `path` parameter is
        queried for a teamspace id.

    Raises
    ------
    FilesError:
        If the directory tree upload failed.

    Examples
    --------
    >>> upload_tree(
    ...     "local/files",
    ...     "/folder1/uploaded_files",
    ...     teamspace="teamspace",
    ... )

    Say `local/files` is a directory that contains one file and one subdirectory with one file.

        local/files
        ├── a.bin
        └── b
            └── b.bin

    The recursive upload creates

        /folder1/uploaded_files
        ├── a.bin
        └── b
            └── b.bin

    in the teamspace named "teamspace" in TileDB.

    """
    teamspace_id, path_id = _normalize_ids(teamspace, path)
    workspace = client.get_workspace_id()
    pool_manager = urllib3.PoolManager()

    src_path = pathlib.Path(source)
    dst_path = pathlib.Path(path_id)
    folders.create_folder(path_id, teamspace=teamspace_id, exist_ok=True, parents=True)

    for root, dirs, files in pathlib.Path(source).walk():
        root_path = pathlib.Path(root).relative_to(src_path)

        for dir in dirs:
            logger.info("Creating folder: path=%r", f"{path_id}/{root_path.name}/{dir}")

            folders.create_folder(
                f"{path_id}/{root_path.name}/{dir}",
                teamspace=teamspace_id,
                exist_ok=True,
                parents=True,
            )

        for file in files:
            file_path = src_path.joinpath(root_path.name, file)

            if file_path.stat().st_size == 0:
                logger.info("Skipping zero size source file: file_path=%r", file_path)
                continue

            content_type, _ = mimetypes.guess_type(file_path)

            logger.info(
                "Uploading file: file_path=%r, content_type=%r, path=%r",
                file_path,
                content_type,
                dst_path.joinpath(root_path.name, file).as_posix(),
            )

            uploader = _FileUploader(
                file_path,
                pool_manager=pool_manager,
                content_type=content_type or "application/octet-stream",
            )

            try:
                uploader.begin(
                    workspace,
                    teamspace_id,
                    dst_path.joinpath(root_path.name, file).as_posix(),
                )
                uploader.put_parts(workspace, teamspace_id)
                uploader.finish(workspace, teamspace_id)
            except FileUploaderError as exc:
                raise FilesError("Failed to upload file.") from exc
