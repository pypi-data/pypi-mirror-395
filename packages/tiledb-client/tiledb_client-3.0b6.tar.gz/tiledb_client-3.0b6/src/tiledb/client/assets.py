"""An Asset is an item in the TileDB Catalog.

An Asset may represent an Array, a Group of Arrays, a Folder, or a File.

When a Folder is created, it becomes an asset and a corresponded Asset
is created in the Catalog. When a file is uploaded, it becomes an asset.
Similarly, creation or registration of arrays and groups produces new
assets in the Catalog.

"""

import logging
import pathlib
from typing import Any, Mapping, Optional, Sequence, Union
from urllib.parse import urlparse

import numpy
from typing_extensions import TypeAlias

import tiledb
from tiledb.datatypes import DataType

from . import client
from ._common.api_v4 import Asset
from ._common.api_v4 import AssetMemberType  # noqa: F401
from ._common.api_v4 import AssetMetadataSaveRequestInner
from ._common.api_v4 import AssetMetadataType
from ._common.api_v4 import AssetRegisterRequest
from ._common.api_v4 import AssetsApi
from ._common.api_v4 import AssetsMoveRequest
from ._common.api_v4 import AssetType
from ._common.api_v4 import AssetUpdateRequest
from ._common.api_v4 import Teamspace
from .pager import Pager
from .rest_api import ApiException
from .tiledb_cloud_error import maybe_wrap

logger = logging.getLogger(__name__)

AssetLike: TypeAlias = Union[Asset, str, object]
TeamspaceLike: TypeAlias = Union[Teamspace, str]


class AssetsError(tiledb.TileDBError):
    """Raised when assets can not be accessed."""


class AssetCreatorError(AssetsError):
    """Raised when _AssetCreator fails to create."""


class _AssetCreator:
    """Helps create or register assets, allows folders as targets."""

    def __init__(self, api_method):
        # api_method is a fully configured api instance method such as
        # build(AssetsApi).register_asset. The args are
        # (workspace, teamspace, path, request, *args, **kwargs).
        self.api_method = api_method

    def call_api_method(self, workspace, teamspace, path, request):
        """Adapt generalized arguments to the underlying API method."""
        self.api_method(
            workspace,
            teamspace,
            path,
            request,
        )

    def create(self, path, teamspace, request, name, *args, **kwargs):
        workspace = tiledb.client.get_workspace_id()

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
            if po.as_posix() in ["/", ".", ""]:
                if i == 0:  # Original target path.
                    logger.debug(
                        "Teamspace at path, appending file name: path=%r, name=%r.",
                        po,
                        name,
                    )
                    if not name:
                        raise AssetCreatorError("An unnamed asset can not be uploaded.")
                    path = po.joinpath(name).as_posix()

                # We've found the teamspace we are looking for.
                break

            try:
                container = (
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
                    raise AssetCreatorError("Invalid target path.") from exc
                else:
                    raise AssetCreatorError("Failed to find container.") from exc
            else:
                if container.type in [AssetType.FOLDER, AssetType.GROUP]:
                    if i == 0:  # Original target path.
                        logger.debug(
                            "Existing container at path, appending file name: path=%r, name=%r.",
                            po,
                            name,
                        )
                        if not name:
                            raise AssetCreatorError(
                                "An unnamed asset can not be added to a folder or group."
                            )
                        path = pathlib.Path(container.path).joinpath(name).as_posix()

                    # We've found the folder we are looking for.
                    break
                else:
                    raise AssetCreatorError(
                        "An asset may only be added to a folder or group."
                    )

        else:
            # We found no folder in the target path. In theory, we
            # can't get here.
            raise AssetCreatorError("A file may only be uploaded to a folder.")

        try:
            logger.debug(
                "Calling API first time: teamspace=%r, path=%r, request=%r, args=%r, kwargs=%r",
                teamspace,
                path,
                request,
                args,
                kwargs,
            )
            resp = self.call_api_method(workspace, teamspace, path, request)
        except ApiException as exc:
            raise AssetCreatorError("Failed to create asset.") from exc

        if resp and hasattr(resp, "data"):
            return resp.data


def _normalize_ids(
    teamspace: Union[Teamspace, str, None],
    asset: Union[str, object],
    /,
) -> tuple[str, str]:
    """Maps asset identifiers to teamspace and asset id or name/path.

    The teamspace and asset id or name/path are used to make server
    requests.

    Parameters
    ----------
    teamspace : Teamspace object, id, or name
        May be None if the asset parameter is an Asset object or tiledb
        URI.
    asset : Asset object, tiledb URI, id, or path
        If id or path, a teamspace is required.

    Returns
    -------
    (str, str)
        A teamspace id or name, and an asset id or path.

    Examples
    --------
    >>> _normalize_ids(None, "tiledb://workspace/teamspace/a/b/c")
    ("teamspace", "a/b/c")

    >>> _normalize_ids("teamspace", "a/b/c")
    ("teamspace", "a/b/c")

    >>> _normalize_ids(None, Asset(id="ast_1", teamspace_id="ts_1"))
    ("ts_1", "ast_1")

    >>> _normalize_ids(None, Folder(asset_id="ast_1", teamspace_id="ts_1"))
    ("ts_1", "ast_1")

    """
    if isinstance(asset, str) and asset.startswith("tiledb://"):
        parts = asset[9:].split("/", 2)
        if len(parts) == 2:
            parts.extend([""])
        return parts[1], parts[2].rstrip("/")

    try:
        teamspace_id_or_name = getattr(teamspace, "teamspace_id", teamspace) or getattr(
            asset, "teamspace_id"
        )
        if not isinstance(teamspace_id_or_name, str):
            raise TypeError("teamspace_id_or_name is not a string.")

        asset_id_or_path = getattr(asset, "asset_id", None) or getattr(
            asset, "id", asset
        )
        if not isinstance(asset_id_or_path, str):
            raise TypeError("asset_id_or_path is not a string.")

    except (AttributeError, TypeError) as exc:
        raise AssetsError("An asset was not specified.") from exc
    else:
        return teamspace_id_or_name, asset_id_or_path


def list_assets(
    path: Union[object, str],
    *,
    teamspace: Optional[Union[Teamspace, str]] = None,
    type: Optional[str] = None,
    created_by: Optional[str] = None,
    expand: Optional[str] = None,
    page: Optional[int] = 1,
    per_page: Optional[int] = None,
    order_by: Optional[str] = None,
) -> Pager[Asset]:
    """List the assets of a folder or teamspace.

    An asset listing consists of a sequence of "pages", or batches, of
    lists of assets. This function returns a Pager object that
    represents one page of the listing. The object also serves as an
    iterator over all assets from that page to the last page, and it can
    be indexed to get all or a subset of assets from that page to the
    last page.

    Parameters
    ----------
    path : str or object
        The TileDB path of a folder. May be a path relative to
        a teamspace, a `Folder` or `Asset` instance, or an absolute
        "tiledb" URI. To list the assets of a teamspace, pass an empty
        string.
    teamspace : Teamspace or str, optional
        The teamspace to which the path belongs, specified by object or
        id. If not provided, the `path` parameter is queried for
        a teamspace id.
    type : str, optional
        Filters for assets of the specified type. Allowed types are
        enumerated by the AssetType class.
    created_by : str, optional
        Filters for assets created by a named user.
    expand : str, optional
        Specifies profiles of additional information
        to include in the response.
    page : int, optional
        Which page of results to retrieve. 1-based.
    per_page : int, optional
        How many results to include on each page.
    order_by : str, optional.
        The order to return assets, by default "created_at desc".
        Supported keys are "created_at", "name", and "asset_type". They
        can be used alone or with "asc" or "desc" separated by a space
        (e.g. "created_at", "asset_type asc").

    Returns
    -------
    Pager for Assets

    Raises
    ------
    AssetsError
        Raised when assets can not be accessed.

    Examples
    --------
    >>> for asset in list_assets(
    ...     "folder1/folder2",
    ...     teamspace="teamspace"
    ... ):
    ...     print(asset)

    Prints all of the assets found directly under the path
    "folder1/folder2".

    """
    teamspace_id, path_id = _normalize_ids(teamspace, path)

    if type is not None and type not in AssetType.allowable_values:
        raise AssetsError("Not a known asset type.")

    try:
        resp = Pager(
            client.client.build(AssetsApi).list_assets,
            client.get_workspace_id(),
            teamspace_id,
            path_id,
            asset_type=type,
            created_by=created_by,
            per_page=per_page,
            expand=expand,
            order_by=order_by,
        )
        resp.call_page(page)
    except ApiException as exc:
        raise AssetsError("The asset listing request failed.") from exc
    else:
        return resp


def get_asset(
    asset: Union[object, str],
    *,
    teamspace: Optional[Union[Teamspace, str]] = None,
) -> Asset:
    """Retrieve the representation of an asset by object, path, or id.

    The catalog representation of a Folder, File, Array, or Group may be
    identified by its object representation, path relative to
    a teamspace, or asset id.

    Parameters
    ----------
    asset : Asset or str
        The target asset, specified by object, path, or id.
    teamspace : Teamspace or str, optional
        The teamspace to search within, specified by object or id. If
        not provided, the `asset` parameter is queried for a teamspace
        id.

    Returns
    -------
    Asset

    Raises
    ------
    AssetsError
        Raised when an asset representation cannot be retrieved.

    Examples
    --------
    >>> obj = get_asset(
    ...     "path/to/asset",
    ...     teamspace="teamspace_id",
    ... )

    >>> obj = get_asset("tiledb://workspace/teamspace/path/to/asset")

    """
    teamspace_id, asset_id = _normalize_ids(teamspace, asset)

    try:
        resp = client.client.build(AssetsApi).get_asset(
            client.get_workspace_id(),
            teamspace_id,
            asset_id,
        )
    except ApiException as exc:
        raise AssetsError("The asset retrieval request failed.") from exc
    else:
        return resp.data


def delete_metadata(
    asset: Union[object, str],
    keys: Sequence[str],
    *,
    teamspace: Optional[Union[Teamspace, str]] = None,
) -> None:
    """Delete asset metadata.

    Metadata are represented as a Python dict with string keys and
    values that can be any builtin Python type or Numpy scalar.

    Parameters
    ----------
    asset : obj or str
        The target asset, specified by object or id.
    keys : Sequence
        A sequence of keys to delete along with their values.
    teamspace : Teamspace or str, optional
        The teamspace to search within, specified by object or id. If
        not provided, the `asset` parameter is queried for a teamspace
        id.

    Returns
    -------
    None

    Raises
    ------
    AssetsError
        Raised when metadata can not be created and saved.

    Examples
    --------
    >>> delete_metadata(
    ...     "asset_id",
    ...     ["field1"],
    ...     teamspace="teamspace_id",
    ... )

    """
    teamspace_id, asset_id = _normalize_ids(teamspace, asset)

    try:
        client.client.build(AssetsApi).delete_asset_metadata(
            client.get_workspace_id(),
            teamspace_id,
            asset_id,
            list(keys),
        )
    except ApiException as exc:
        raise AssetsError("The asset metadata deletion request failed.") from exc


def update_metadata(
    asset: Union[object, str],
    items: Mapping[str, Any],
    *,
    teamspace: Optional[Union[Teamspace, str]] = None,
) -> None:
    """Update asset metadata.

    Metadata are represented as a Python dict with string keys and
    values that can be any builtin Python type or Numpy scalar.

    Parameters
    ----------
    asset : obj or str
        The target asset, specified by object or id.
    items : Mapping
        A mapping of metadata keys and values.
    teamspace : Teamspace or str, optional
        The teamspace to search within, specified by object or id. If
        not provided, the `asset` parameter is queried for a teamspace
        id.

    Returns
    -------
    None

    Raises
    ------
    AssetsError
        Raised when metadata can not be created and saved.

    Examples
    --------
    >>> update_metadata(
    ...     "asset_id",
    ...     {"field1": "another string", "field2": numpy.float64(4.2)},
    ...     teamspace="teamspace_id",
    ... )

    """
    teamspace_id, asset_id = _normalize_ids(teamspace, asset)
    metadata = [
        AssetMetadataSaveRequestInner(
            key=k,
            value=str(v),
            type=getattr(
                AssetMetadataType,
                DataType.from_numpy(numpy.array(v).dtype).tiledb_type.name,
            ),
        )
        for k, v in items.items()
    ]

    try:
        _ = client.client.build(AssetsApi).update_asset_metadata(
            client.get_workspace_id(),
            teamspace_id,
            asset_id,
            metadata,
        )
    except ApiException as exc:
        raise AssetsError("The asset metadata creation request failed.") from exc


def get_metadata(
    asset: Union[object, str],
    *,
    teamspace: Optional[Union[Teamspace, str]] = None,
) -> dict:
    """Retrieve asset metadata.

    Metadata are represented as a Python dict with string keys and
    values that can be any builtin Python type or Numpy scalar.

    Parameters
    ----------
    asset : obj or str
        The target asset, specified by object or id.
    teamspace : Teamspace or str, optional
        The teamspace to search within, specified by object or id. If
        not provided, the `asset` parameter is queried for a teamspace
        id.

    Returns
    -------
    dict

    Raises
    ------
    AssetsError
        Raised when metadata can not be created and saved.

    Examples
    --------
    >>> get_metadata("asset_id", teamspace="teamspace_id")

    """
    teamspace_id, asset_id = _normalize_ids(teamspace, asset)

    try:
        resp = client.client.build(AssetsApi).get_asset_metadata(
            client.get_workspace_id(),
            teamspace_id,
            asset_id,
        )
    except ApiException as exc:
        raise AssetsError("The asset metadata retrieval request failed.") from exc
    else:
        items = [
            (
                md.key,
                tiledb.datatypes.DataType.from_tiledb(
                    getattr(tiledb.datatypes.lt.DataType, md.type.upper())
                ).np_dtype.type(md.value),
            )
            for md in resp.data
        ]
        return dict(items)


def register_asset(
    uri: str,
    path: Union[object, str],
    *,
    teamspace: Optional[Union[Teamspace, str]] = None,
    acn: Optional[str] = None,
) -> None:
    """Register a cloud storage object like an array or group.

    Parameters
    ----------
    uri : str
        Object identifier. For example: "s3://bucket/prefix/file".
    path : str or object
        The TileDB path at which the object is to be registered. May be
        a path relative to a teamspace, a `Folder` or `Asset` instance,
        or an absolute "tiledb" URI. If the path to a folder is
        provided, the basename or stem of the `uri` will be appended to
        form a full asset path.
    teamspace : Teamspace or str, optional
        The teamspace to which the object will be registered, specified
        by object or id. If not provided, the `path` parameter is
        queried for a teamspace id.
    acn : str, optional
        The name of a stored credential for accessing the object.

    Raises
    ------
    AssetsError:
        If the registration failed.

    Examples
    --------
    >>> folder = folders.create_folder(
    ...     "objects",
    ...     teamspace="teamspace",
    ...     exists_ok=True,
    ... )
    >>> assets.register_asset(
    ...     "s3://bucket/prefix/example1",
    ...     "objects",
    ...     teamspace="teamspace",
    ...     acn="bucket-credentials",
    ... )

    This creates an asset at path "objects/example1" in the teamspace
    named "teamspace". The object's basename has been used to construct
    the full path.

    If you like, you can pass a Folder or Asset object instead of a path
    string and get the same result.

    >>> register_asset(
    ...     "s3://bucket/prefix/example1",
    ...     folder,
    ...     acn="bucket-credentials",
    ... )

    An object can also be registered to a specific absolute "tiledb"
    URI that specifies a different name.

    >>> register_udf(
    ...     "s3://bucket/prefix/example1",
    ...     "tiledb://workspace/teamspace/objects/new_asset",
    ...     acn="bucket-credentials",
    ... )

    """
    teamspace_id, path_id = _normalize_ids(teamspace, path)
    req = AssetRegisterRequest(uri=uri, access_credentials_name=acn)
    parsed = urlparse(uri)
    obj_basename = pathlib.Path(parsed.path).name
    api = client.client.build(AssetsApi)
    creator = _AssetCreator(api.register_asset)
    try:
        creator.create(path_id, teamspace_id, req, obj_basename)
    except AssetCreatorError as exc:
        raise AssetsError("Failed to register asset.") from exc


def update_asset(
    asset: Union[Asset, str, object],
    *,
    teamspace: Optional[Union[Teamspace, str]] = None,
    description: Optional[str] = None,
    name: Optional[str] = None,
) -> None:
    """Update the name and description of a asset.

    An asset can be "moved" within a folder by updating its `name` property.

    The asset may be identified by asset id, path relative to
    a teamspace, or object representation (Asset instance).

    Parameters
    ----------
    asset : Asset or str
        The representation or string identifier of an existing asset.
    description : str, optional
        Description of the asset.
    name : str, optional
        Name of the asset.
    teamspace : Teamspace or str, optional
        The representation or string identifier of the asset's
        teamspace. If the asset parameter is an Asset instance, the
        teamspace will be obtained from it.

    Returns
    -------
    None

    Raises
    ------
    AssetsError
        If the asset cannot be updated.

    Examples
    --------
    >>> assets.update_asset(
    ...     "asset1",
    ...     teamspace="teamspace",
    ...     name="new-name",
    ...     description="An updated description for asset one.",
    ... )

    """
    teamspace_id, asset_id = _normalize_ids(teamspace, asset)
    asset_update_request = AssetUpdateRequest(name=name, description=description)

    try:
        client.client.build(AssetsApi).update_asset(
            client.get_workspace_id(),
            teamspace_id,
            asset_id,
            asset_update_request,
        )
    except ApiException as exc:
        raise AssetsError("The asset update request failed.") from exc


def move_assets(
    assets: Union[AssetLike, list[AssetLike]],
    folder: AssetLike,
    *,
    teamspace: Optional[Union[Teamspace, str]] = None,
) -> None:
    """Move one or more assets to a folder.

    This function can not be used to rename assets. For that, see
    `update_assets()`.

    Assets may be identified by asset id, path relative to
    a teamspace, or object representation (Asset instance).

    Parameters
    ----------
    assets : AssetLike or list of AssetLike
        The representation or string identifier(s) of an existing asset(s).
    folder : AssetLike
        The representation or string identifier of an existing folder.
    teamspace : Teamspace or str, optional
        The representation or string identifier of the assets'
        teamspace. If the folder parameter is an Asset instance, the
        teamspace will be obtained from it.

    Returns
    -------
    None

    Raises
    ------
    AssetsError
        If the assets cannot be moved.

    Examples
    --------
    >>> assets.move_assets(
    ...     "/asset1",
    ...     "/folder",
    ...     teamspace="teamspace",
    ... )

    """
    assets = [assets] if not isinstance(assets, list) else assets

    teamspace_id, folder_id = _normalize_ids(teamspace, folder)
    _, assets_to_add = zip(*(_normalize_ids(teamspace, ob) for ob in assets))
    assets_move_request = AssetsMoveRequest(
        assets_to_add=assets_to_add, target=folder_id
    )

    try:
        client.client.build(AssetsApi).move_assets(
            client.get_workspace_id(), teamspace_id, assets_move_request
        )
    except ApiException as exc:
        raise AssetsError("The assets move request failed.") from maybe_wrap(exc)


def delete_asset(
    asset: AssetLike,
    *,
    teamspace: Optional[TeamspaceLike] = None,
    delete_storage: Optional[bool] = False,
) -> None:
    """Remove an asset and its sub-assets from the TileDB catalog.

    The corresponding objects in cloud storage may be optionally deleted
    as well.

    The primary asset may be identified by its object representation,
    path relative to a teamspace, or asset id.

    Parameters
    ----------
    asset : AssetLike
        The target asset, specified by object, path, or id.
    teamspace : Teamspace or str, optional
        The teamspace to search within, specified by object or id. If
        not provided, the `asset` parameter is queried for a teamspace
        id.
    delete_storage : bool, optional
        If True, this function will also delete backing objects from
        storage (e.g., S3).  The default is False.

    Raises
    ------
    AssetsError
        Raised when an asset cannot be deleted.

    Examples
    --------
    >>> delete_asset(
    ...     "path/to/asset",
    ...     teamspace="teamspace_id",
    ... )

    """
    teamspace_id, asset_id = _normalize_ids(teamspace, asset)

    try:
        client.client.build(AssetsApi).delete_asset(
            client.get_workspace_id(),
            teamspace_id,
            asset_id,
            delete_assets="true" if delete_storage is True else "false",
        )
    except ApiException as exc:
        raise AssetsError("The asset deletion request failed.") from maybe_wrap(exc)


def search_assets(
    *,
    query: Optional[str] = None,
    fields: Optional[Union[list[str], str]] = None,
    metadata: Optional[Union[list[str], str]] = None,
    path: Optional[str] = None,
    teamspace: Optional[Union[list[TeamspaceLike], TeamspaceLike]] = None,
    teamspace_exclude: Optional[Union[list[TeamspaceLike], TeamspaceLike]] = None,
    public: Optional[bool] = None,
    sort: Optional[str] = None,
    sort_dir: Optional[str] = None,
    page: Optional[int] = 1,
    per_page: Optional[int] = None,
) -> Pager[Asset]:
    """Search the catalog for assets.

    A search result consists of a sequence of "pages", or batches, of
    lists of assets. This function returns a Pager object that
    represents one page of the listing. The object also serves as an
    iterator over all assets from that page to the last page, and it can
    be indexed to get all or a subset of assets from that page to the
    last page.

    Without parameters, this function will query all accessible assets,
    public or in private teamspaces that the user is a member of.

    Assets may be filtered using simple expressions. The expression
    syntax is {key}{op}{value}, where `key` is one of an asset's fields
    ("created_by", "backing_type", etc.) and `op` is one of: "<", ">",
    "<=", ">=", "=", "!=", or ":".  The op ":" sets up a range where two
    valid values {lo}..{hi}, equivalent to {lo} <= x <= {hi}, Date
    values ("created_at", "updated_at") can be relative times in the
    past ("today", "yesterday", "week", "month", "year"), or a RFC 3339
    value like "2006-01-02T15:04:05Z07:00".

    User-defined metadata fields may be used in filters with the same
    expression syntax.

    Parameters
    ----------
    query : str, optional
        Query keywords.
    fields : list[str], optional
        A list of expressions involving standard asset fields.
    metadata : list[str], optional
        A list of expressions involving user-defined metadata fields.
    path : str, optional
        The path to search within. Default is all paths.
    teamspace : list[Teamspace or str], optional
        The teamspaces to search within, specified by object or id.
    teamspace_exclude : list[Teamspace or str], optional
        The teamspaces to exclude from search, specified by object or
        id.
    public : bool, optional
        Whether to include assets of public teamspaces in result, or
        not. Default is True.
    sort : str, optional
        Sort order for results. Valid values are "relevance", "recency",
        or "name". The default is relevance.
    sort_dir : str, optional
        Sort direction for results. Valid values are "asc" (ascending)
        or "desc" (descending). The default is "desc".
    page : int, optional
        Which page of results to retrieve. 1-based.
    per_page : int, optional
        How many results to include on each page.

    Returns
    -------
    Pager for Assets

    Raises
    ------
    AssetsError
        Raised when assets can not be accessed.

    Examples
    --------
    >>> for asset in search_assets(
    ...     fields=["created_by=user1"],
    ...     path="folder1/folder2",
    ...     teamspace="teamspace"
    ... ):
    ...     print(asset)

    Prints the assets under path "folder1/folder2" that were created by
    the user named "user1".

    """
    # Four of our parameters accept a list of strings or a single string.
    # We normalize to a list of strings.
    teamspace = (
        [teamspace] if teamspace and not isinstance(teamspace, list) else teamspace
    )
    teamspace_exclude = (
        [teamspace_exclude]
        if teamspace_exclude and not isinstance(teamspace_exclude, list)
        else teamspace_exclude
    )
    fields = [fields] if fields and isinstance(fields, str) else fields
    metadata = [metadata] if fields and isinstance(metadata, str) else metadata

    try:
        resp = Pager(
            client.client.build(AssetsApi).search_assets,
            client.get_workspace_id(),
            q=query,
            filters=fields,
            metadata=metadata,
            path=path,
            teamspace=teamspace,
            teamspace_exclude=teamspace_exclude,
            public=public,
            sort=sort,
            sort_dir=sort_dir,
            per_page=per_page,
        )
        resp.call_page(page)
    except ApiException as exc:
        raise AssetsError("The asset search request failed.") from exc
    else:
        return resp
