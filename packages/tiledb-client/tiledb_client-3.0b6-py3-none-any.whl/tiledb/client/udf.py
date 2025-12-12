import base64
import datetime
import logging
import uuid
from functools import partial
from typing import Any, Callable, Iterable, Optional, Tuple, Union

import tiledb

from . import array
from . import assets
from . import client
from . import rest_api
from . import tiledb_cloud_error
from ._common import functions
from ._common import json_safe
from ._common import utils
from ._common import visitor
from ._common.api_v4 import Teamspace
from ._results import decoders
from ._results import results
from ._results import sender
from ._results import stored_params
from ._results import tiledb_json
from ._results import types
from ._vendor import cloudpickle as tdbcp
from .assets import _normalize_ids
from .rest_api import ApiException as GenApiException
from .rest_api import models
from .rest_api.models import UDFType

# Deprecated; re-exported for backwards compatibility.
tiledb_cloud_protocol = utils.TILEDB_CLOUD_PROTOCOL

UDFResultType = models.ResultFormat
UDFInfo = models.UDFInfo
UDFInfoUpdate = models.UDFInfoUpdate

logger = logging.getLogger(__name__)


class UDFError(tiledb.TileDBError):
    """Raised when a UDF can not be registered, retrieved, or executed."""


def exec_base(
    func: Union[str, Callable, assets.Asset],
    *args: Any,
    teamspace: Union[Teamspace, str] = None,
    image_name: str = "default",
    http_compressor: Optional[str] = "deflate",
    include_source_lines: bool = True,
    task_name: Optional[str] = None,
    result_format: str = "tiledb_json",
    store_results: bool = False,
    stored_param_uuids: Iterable[uuid.UUID] = (),
    timeout: int = None,
    resource_class: Optional[str] = None,
    _download_results: bool = True,
    _server_graph_uuid: Optional[uuid.UUID] = None,
    _client_node_uuid: Optional[uuid.UUID] = None,
    access_credentials_name: Optional[str] = None,
    **kwargs,
) -> "results.RemoteResult":
    """Execute a user-defined function, returning the result and metadata.

    :param func: The function to call, either as a callable function, or as
        the name of a registered user-defined function. (If ``name`` is set,
        this is instead prepended to ``args`` for backwards compatibility.)
    :param args: The arguments to pass to the function.
    :param teamspace: teamspace to run udf under.
    :param image_name: udf image name to use, useful for testing beta features
    :param http_compressor: set http compressor for results
    :param include_source_lines: True to send the source code of your UDF to
        the server with your request. (This means it can be shown to you
        in stack traces if an error occurs.) False to send only compiled Python
        bytecode.
    :param str task_name: optional name to assign the task
        for logging and audit purposes
    :param ResultFormat result_format: result serialization format
    :param store_results: True to temporarily store results on the server side
        for later retrieval (in addition to downloading them).
    :param timeout: Timeout for UDF in seconds
    :param resource_class: The name of the resource class to use. Resource classes
        define maximum limits for cpu and memory usage.
    :param _download_results: True to download and parse results eagerly.
        False to not download results by default and only do so lazily
        (e.g. for an intermediate node in a graph).
    :param _server_graph_uuid: If this function is being executed within a DAG,
        the server-generated ID of the graph's log. Otherwise, None.
    :param _client_node_uuid: If this function is being executed within a DAG,
        the ID of this function's node within the graph. Otherwise, None.
    :param kwargs: named arguments to pass to function

    """
    if isinstance(func, assets.Asset):
        teamspace_id = func.teamspace_id
        func = func.path
    elif isinstance(func, str):
        teamspace_id, func = _normalize_ids(teamspace, func)
    else:
        teamspace_id = teamspace or "general"

    api_instance = client.build(rest_api.UdfApi)

    udf_model = models.MultiArrayUDF(
        language=models.UDFLanguage.PYTHON,
        result_format=result_format,
        store_results=store_results,
        version=utils.PYTHON_VERSION,
        image_name=image_name,
        task_name=task_name,
        stored_param_uuids=list(str(uuid) for uuid in stored_param_uuids),
        resource_class=resource_class,
        dont_download_results=not _download_results,
        task_graph_uuid=_server_graph_uuid and str(_server_graph_uuid),
        client_node_uuid=_client_node_uuid and str(_client_node_uuid),
        access_credentials_name=access_credentials_name,
    )

    if timeout is not None:
        udf_model.timeout = timeout

    if callable(func):
        udf_model._exec = utils.b64_pickle(func)
        if include_source_lines:
            udf_model.exec_raw = functions.getsourcelines(func)
    else:
        if not func.startswith("/"):
            func = "/" + func
        udf_model.udf_info_name = f"{teamspace_id}/{func}"

    arguments = types.Arguments(args, kwargs)
    udf_model.arguments_json = json_safe.Value(
        _StoredParamJSONer().encode_arguments(arguments)
    )

    submit_kwargs = dict(udf=udf_model)
    if http_compressor:
        submit_kwargs["accept_encoding"] = http_compressor

    try:
        return sender.send_udf_call(
            client.get_workspace_id(),
            teamspace_id,
            api_instance.submit_generic_udf,
            submit_kwargs,
            decoders.Decoder(result_format),
            id_callback=array._maybe_set_last_udf_id,
            results_stored=store_results,
            results_downloaded=_download_results,
        )
    except GenApiException as exc:
        raise UDFError("Failed to execute UDF.") from tiledb_cloud_error.maybe_wrap(exc)


@functions.signature_of(exec_base)
def exec(*args, **kwargs) -> Any:
    """Run a user defined function, synchronously, returning only the result.

    Arguments are exactly as in :func:`exec_base`.
    """
    return exec_base(*args, **kwargs).get()


@functions.signature_of(exec_base)
def exec_async(*args, **kwargs) -> Any:
    """Run a user defined function, asynchronously.

    Arguments are exactly as in :func:`exec_base`.
    """
    return sender.wrap_async_base_call(exec_base, *args, **kwargs)


_TIME_FORMATS = (
    "%Y-%m-%d",
    "%Y-%m-%dT%H:%M",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M:%S.%f",
)


def _parse_udf_name_timestamp(
    full_name: str,
) -> Tuple[str, Optional[datetime.datetime]]:
    name, at, ts_str = full_name.partition("@")
    name = name.strip()
    ts_str = ts_str.strip()
    if not at:
        # This means that "@" was not found in the string,
        # and we're just running a normal UDF.
        return name, None
    ts_str = ts_str.replace(" ", "T")
    for fmt in _TIME_FORMATS:
        try:
            naive_ts = datetime.datetime.strptime(ts_str, fmt)
        except ValueError:
            continue
        return name, naive_ts.replace(tzinfo=datetime.timezone.utc)
    raise ValueError(
        f"Could not parse {ts_str} as a timestamp. "
        "Timestamp must be formatted as yyyy-MM-dd[ HH:mm[:ss[.SSS]]], "
        "and will interpreted as UTC."
    )


def register_udf(
    func: Callable,
    path: Union[object, str],
    *,
    teamspace: Optional[Union[Teamspace, str]] = None,
    image_name: Optional[str] = None,
    type: Optional[str] = None,
    include_source_lines: Optional[bool] = True,
) -> None:
    """Register a user-defined function (UDF).

    Parameters
    ----------
    func: callable
        The function to be registered.
    path : str or object
        The TileDB path at which the object is to be registered. May be
        a path relative to a teamspace, a `Folder` or `Asset` instance,
        or an absolute "tiledb" URI. If the path to a folder is
        provided, the name of the function will be appended to form
        a full asset path.
    teamspace : Teamspace or str, optional
        The teamspace to which the object will be registered, specified
        by object or id. If not provided, the `path` parameter is
        queried for a teamspace id.
    image_name : str, optional
        Image name.
    type : str, optional
        Type of udf: generic or single_array.
    include_source_lines : bool, optional
        If False, disables sending sources lines of function along with
        udf.

    Raises
    ------
    UDFError:
        When a function can not be registered.

    Examples
    --------
    >>> def get_tiledb_version():
    ...     import tiledb
    ...     return tiledb.__version__
    ...
    >>> folder = folders.create_folder(
    ...     "udfs",
    ...     teamspace="teamspace",
    ...     exists_ok=True,
    ... )
    >>> register_udf(get_tiledb_version, "udfs", teamspace="teamspace")

    This creates a user-defined function asset at path
    "udfs/get_tiledb_version" in the teamspace named "teamspace". The
    function's name has been used to construct the full path.

    If you like, you can pass a Folder or Asset object instead of a path
    string and get the same result.

    >>> register_udf(get_tiledb_version, folder)

    A UDF can also be registered to a specific absolute "tiledb" URI
    that specifies a different name.

    >>> register_udf(
    ...     get_tiledb_version,
    ...     "tiledb://workspace/teamspace/udfs/get_tdbpy_version"
    ... )

    """
    if not callable(func):
        raise TypeError("func is not callable.")

    teamspace_id, path_id = _normalize_ids(teamspace, path)

    api_instance = client.build(rest_api.UdfApi)
    pickledUDF = tdbcp.dumps(func, protocol=utils.TILEDB_CLOUD_PROTOCOL)
    pickledUDF = base64.b64encode(pickledUDF).decode("ascii")
    source_lines = functions.getsourcelines(func) if include_source_lines else None

    udf_model = models.UDFInfoUpdate(
        language=models.UDFLanguage.PYTHON,
        version=utils.PYTHON_VERSION,
        image_name=image_name,
        type=type,
        _exec=pickledUDF,
        exec_raw=None,
    )

    if source_lines is not None:
        udf_model.exec_raw = source_lines

    creator = assets._AssetCreator(api_instance.register_udf_info)
    try:
        creator.create(path_id, teamspace_id, udf_model, func.__name__)
    except assets.AssetCreatorError as exc:
        raise UDFError("Failed to register UDF.") from exc


register_generic_udf = partial(register_udf, type=UDFType.GENERIC)
register_single_array_udf = partial(register_udf, type=UDFType.SINGLE_ARRAY)
register_multi_array_udf = partial(register_udf, type=UDFType.MULTI_ARRAY)


def update_udf(
    udf: Union[object, str],
    *,
    teamspace: Union[Teamspace, str],
    func: Optional[Callable] = None,
    image_name: Optional[str] = None,
    type: Optional[str] = None,
    include_source_lines: Optional[bool] = True,
    license_id: Optional[str] = None,
    license_text: Optional[str] = None,
    readme: Optional[str] = None,
):
    """Update a registered UDF.

    Parameters
    ----------
    udf : str or object
        The TileDB path at which the object is to be registered. May be
        a path relative to a teamspace, a `Folder` or `Asset` instance,
        or an absolute "tiledb" URI. If the path to a folder is
        provided, the name of the function will be appended to form
        a full asset path.
    teamspace : Teamspace or str
        The teamspace to which the object will be registered.
    func: callable
        The function to register.
    image_name : str, optional
        Image name.
    type : str, optional
        Type of udf: generic or single_array.
    include_source_lines : str, optional
        Disables sending sources lines of function along with udf.
    license_id : str, optional
        A new license id.
    license_text : str, optional
        A new license text.
    readme : str, optional
        A new long description for the UDF.

    Raises
    ------
    UDFError
        When the UDF can not be updated.

    """
    teamspace_id, udf_id = _normalize_ids(teamspace, udf)

    if func and not callable(func):
        raise TypeError("func is not callable.")

    try:
        api_instance = client.build(rest_api.UdfApi)
        pickledUDF = tdbcp.dumps(func, protocol=utils.TILEDB_CLOUD_PROTOCOL)
        pickledUDF = base64.b64encode(pickledUDF).decode("ascii")
        source_lines = functions.getsourcelines(func) if include_source_lines else None

        udf_model = models.UDFInfoUpdate(
            # name=update_udf_name,
            language=models.UDFLanguage.PYTHON,
            version=utils.PYTHON_VERSION,
            image_name=image_name,
            license_id=license_text,
            license_text=license_id,
            readme=readme,
            type=type,
            _exec=pickledUDF,
            exec_raw=None,
        )

        if source_lines is not None:
            udf_model.exec_raw = source_lines

        api_instance.update_udf_info(
            client.get_workspace_id(),
            teamspace_id,
            udf_id,
            udf_model,
        )

    except GenApiException as exc:
        raise tiledb_cloud_error.maybe_wrap(exc) from None


update_generic_udf = update_udf
update_single_array_udf = update_udf


def get_udf(
    udf: Union[object, str],
    *,
    teamspace: Optional[Union[Teamspace, str]] = None,
) -> UDFInfo:
    """Retrieve the representation of a registered UDF.

    The registration does not contain the source code of the
    user-defined function or any serialization of the function.

    Parameters
    ----------
    udf : Asset, object, or str
        The registered UDF, specified by object, path, or id.
    teamspace : Teamspace or str, optional
        The teamspace to search within, specified by object or id. If
        not provided, the `udf` parameter is queried for a teamspace
        id.

    Returns
    -------
    UDFInfo

    Raises
    ------
    UDFError
        When the UDF can not be retrieved.

    """
    teamspace_id, udf_id = _normalize_ids(teamspace, udf)

    try:
        api_instance = client.build(rest_api.UdfApi)
        return api_instance.get_udf_info(
            client.get_workspace_id(), teamspace_id, udf_id
        )
    except GenApiException as exc:
        raise UDFError(
            "The UDF can not be retrieved."
        ) from tiledb_cloud_error.maybe_wrap(exc)


class _StoredParamJSONer(tiledb_json.Encoder):
    """Turns parameters passed to the existing UDF APIs into TileDB JSON.

    Existing code needs to maintain the same interface for stored params,
    so to match the behavior of the Pickle-based argument encoding,
    we still accept ``StoredParam`` objects as parameters to the various UDF
    execution functions.
    """

    def maybe_replace(self, arg: object) -> Optional[visitor.Replacement]:
        if isinstance(arg, stored_params.StoredParam):
            return visitor.Replacement(
                {
                    tiledb_json.SENTINEL_KEY: "stored_param",
                    "task_id": str(arg.task_id),
                    # Because the decoder may contain special logic apart from
                    # "just read in the tdbjson-serialized object", we need to
                    # specify the exact Decoder object we will use.
                    "python_decoder": self.visit(arg.decoder),
                }
            )
        return super().maybe_replace(arg)
