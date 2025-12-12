"""TileDB folders.

This module contains functions that operate on a teamspace; adding,
removing, retrieving, or listing folders. It also contains functions
operating on a folder; adding, removing, or listing asset contents; or
updating folder properties.

Model classes associated with these functions are also exported from
this module.
"""

import logging
import pathlib
from typing import Optional, Union

import tiledb
from tiledb.client import client
from tiledb.client._common.api_v4 import Asset
from tiledb.client._common.api_v4 import Folder
from tiledb.client._common.api_v4 import FolderCreateRequestInner
from tiledb.client._common.api_v4 import FoldersApi
from tiledb.client._common.api_v4 import Teamspace

from .assets import _normalize_ids
from .rest_api import ApiException
from .tiledb_cloud_error import maybe_wrap

logger = logging.getLogger(__name__)


class FoldersError(tiledb.TileDBError):
    """Raised when a folder CRUD operation fails."""


def create_folder(
    path: str,
    *,
    teamspace: Optional[Union[Teamspace, str]] = None,
    description: Optional[str] = None,
    parents: Optional[bool] = False,
    exist_ok: Optional[bool] = False,
) -> Folder:
    """Create a new folder in a teamspace.

    Optionally, parents of the new folder can also be created.

    Parameters
    ----------
    path : str
        The TileDB path at which the folder is to be created. May be
        a path relative to a teamspace or an absolute "tiledb" URI.
    teamspace : Teamspace or str, optional
        The teamspace to which the folder will be registered, specified
        by object or id. If not provided, the `path` parameter is
        queried for a teamspace id.
    description : str, optional
        Description of the folder to create.
    parents : bool, optional
        If True, parents will be created as needed. If False,
        a FoldersError will be raised if a parent is missing.
    exist_ok : bool, optional
        If False, a FoldersError will be raised if the folder already
        exists.

    Returns
    -------
    Folder

    Raises
    ------
    FoldersError:
        If the folder creation request failed.

    Examples
    --------
    >>> folder1 = folders.create_folder(
    ...     "folder1",
    ...     teamspace="teamspace",
    ...     description="Folder One",
    ... )

    A folder can be created within an existing folder.

    >>> folder2 = folders.create_folder(
    ...     "folder1/folder2",
    ...     teamspace="teamspace",
    ...     description="Folder Two",
    ... )

    An absolute "tiledb" URI may be used as the destination path
    without a teamspace argument.

    >>> folder3 = folders.create_folder(
    ...     "tiledb://workspace/teamspace/folder1/folder3",
    ...     description="Folder Two",
    ... )

    """
    teamspace_id, path_id = _normalize_ids(teamspace, path)
    tdb_path = pathlib.Path(path_id.strip("/"))
    api_instance = client.client.build(FoldersApi)

    # Traverse the destination path's parents, in reverse order.
    # We materialize the parents iterator to work around
    # https://github.com/python/cpython/issues/79679 for Python 3.9.
    for pth in list(tdb_path.parents)[-2::-1]:
        try:
            _ = api_instance.get_folder(
                client.get_workspace_id(),
                teamspace_id,
                pth.as_posix(),
            )
        except ApiException:
            if not parents:
                raise FoldersError("A parent folder does not exist.")
            else:
                try:
                    logger.debug("Creating parent folder: pth=%r", pth)
                    _ = api_instance.create_folder(
                        client.get_workspace_id(),
                        teamspace_id,
                        pth.as_posix(),
                        FolderCreateRequestInner(description=""),
                    )
                except ApiException as exc:
                    raise FoldersError(
                        "The folder creation request failed."
                    ) from maybe_wrap(exc)
    else:
        try:
            resp = api_instance.get_folder(
                client.get_workspace_id(),
                teamspace_id,
                tdb_path.as_posix(),
            )
        except ApiException:
            try:
                resp = api_instance.create_folder(
                    client.get_workspace_id(),
                    teamspace_id,
                    tdb_path.as_posix(),
                    FolderCreateRequestInner(description=(description or "")),
                )
            except ApiException as exc:
                raise FoldersError(
                    "The folder creation request failed."
                ) from maybe_wrap(exc)
        else:
            if not exist_ok:
                raise FoldersError("A folder exists at the specified path.")

    return resp.data


def get_folder(
    folder: Union[Folder, Asset, str],
    *,
    teamspace: Optional[Union[Teamspace, str]] = None,
) -> Folder:
    """Retrieve the representation of a TileDB folder.

    The folder may be identified by asset id, path relative to
    a teamspace, or object representation (Folder or Asset instance).

    Parameters
    ----------
    folder : Asset, Folder, or str
        The object representation, name, or path of an existing folder.
    teamspace : Teamspace or str, optional
        The representation or string identifier of the folder's
        teamspace. If the folder parameter is a Folder instance, the
        teamspace will be obtained from it.

    Returns
    -------
    Folder

    Raises
    ------
    FolderError
        If the folder cannot be retrieved.

    Examples
    --------
    >>> folder1 = get_folder("folder1", teamspace="teamspace")
    >>> folder2 = get_folder("folder1/folder2", teamspace="teamspace")

    """
    teamspace_id, asset_id = _normalize_ids(teamspace, folder)

    try:
        resp = client.client.build(FoldersApi).get_folder(
            client.get_workspace_id(),
            teamspace_id,
            asset_id,
        )
    except ApiException as exc:
        raise FoldersError("The folder retrieval request failed.") from exc
    else:
        return resp.data


def list_folder_contents(
    folder: Union[Folder, Asset, str],
    *,
    teamspace: Optional[Union[Teamspace, str]] = None,
) -> list[Asset]:
    """Retrieve a list of assets in the folder.

    The folder may be identified by asset id, path relative to
    a teamspace, or object representation (Folder or Asset instance).

    Parameters
    ----------
    folder : Asset, Folder, or str
        The representation or string identifier of an existing folder.
    teamspace : Teamspace or str, optional
        The representation or string identifier of the folder's
        teamspace. If the folder parameter is a Folder instance, the
        teamspace will be obtained from it.

    Returns
    -------
    list of Assets.

    Raises
    ------
    FolderError
        If the folder's cannot be listed.

    Examples
    --------
    >>> assets = folders.list_folder_contents(
    ...     "folder1",
    ...     teamspace="teamspace"
    ... )
    >>> [asset.name for asset in assets]
    ["folder2"]

    """
    teamspace_id, asset_id = _normalize_ids(teamspace, folder)

    try:
        resp = client.client.build(FoldersApi).get_folder_contents(
            client.get_workspace_id(),
            teamspace_id,
            asset_id,
        )
    except ApiException as exc:
        raise FoldersError("The folder contents listing request failed.") from exc
    else:
        return resp.data
