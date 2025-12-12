"""Register, search, and manage arrays with TileDB."""

import posixpath
import urllib.parse
import uuid
from typing import Any, Callable, Iterable, List, Optional, Sequence, Union

import numpy

from . import client
from . import rest_api
from . import tiledb_cloud_error
from . import udf
from ._common import functions
from ._common import json_safe
from ._common import utils
from ._results import decoders
from ._results import results
from ._results import sender
from ._results import types
from .assets import Asset
from .assets import AssetLike
from .assets import Teamspace
from .assets import _normalize_ids
from .rest_api import ApiException as GenApiException
from .rest_api import models

last_udf_task_id: Optional[str] = None

# Re-export for compatibility.
split_uri = utils.split_uri


class ArrayList:
    """
    This class incrementally builds a list of UDFArrayDetails
    for use in multi array UDFs `list[UDFArrayDetails]`
    """

    def __init__(self):
        self.arrayList = []

    def add(self, uri=None, ranges=None, buffers=None, layout=None):
        """
        Adds an array to list
        """
        if layout is None:
            converted_layout = None
        elif layout.upper() == "R":
            converted_layout = "row-major"
        elif layout.upper() == "C":
            converted_layout = "col-major"
        elif layout.upper() == "G":
            converted_layout = "global-order"
        elif layout.upper() == "U":
            converted_layout = "unordered"

        if ranges:
            parsed = parse_ranges(ranges)  # check that the ranges are parseable.
        else:
            parsed = None

        udf_array_details = models.UDFArrayDetails(
            uri=uri,
            ranges=models.QueryRanges(layout=converted_layout, ranges=parsed),
            buffers=buffers,
            parameter_id=str(uuid.uuid4()),
        )
        self.arrayList.append(udf_array_details)

    def get(self):
        """
        Returns the list of UDFArrayDetails
        """
        return self.arrayList

    def _to_tgudf_args(self) -> Sequence[object]:
        tgudf_ified = tuple(
            {
                "__tdbudf__": "udf_array_details",
                "udf_array_details": entry,
            }
            for entry in self.arrayList
        )
        if not tgudf_ified:
            # If there are no arrays, nothing is prepended.
            return ()
        if len(tgudf_ified) == 1:
            # If there is one array, it is prepended as a single value.
            return ({"value": tgudf_ified[0]},)
        # Otherwise, the list of arrays is passed as a single parameter.
        return ({"value": tgudf_ified},)


def info(uri, async_req=False):
    """
    Returns the cloud metadata

    :param async_req: return future instead of results for async support

    :return: metadata object
    """
    (namespace, array_name) = split_uri(uri)
    api_instance = client.build(rest_api.ArrayApi)

    try:
        return api_instance.get_array_metadata(
            namespace=namespace, array=array_name, async_req=async_req
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.maybe_wrap(exc) from None


def update_info(
    uri,
    array_name=None,
    description=None,
    access_credentials_name=None,
    tags=None,
    async_req=False,
):
    """
    Update an array's info
    :param str namespace: The username or organization that owns the array.
        If unset, will use the logged-in user.
    :param str array_name: name of array to rename to
    :param str description: optional description
    :param str access_credentials_name: The access credentials to use when
        accessing the backing array. Leave unset to not change.
    :param list tags: to update to
    :param str file_type: array represents give file type
    :param str file_properties: set file properties on array
    :param async_req: return future instead of results for async support
    """
    api_instance = client.build(rest_api.ArrayApi)
    (namespace, current_array_name) = split_uri(uri)

    try:
        return api_instance.update_array_metadata(
            namespace=namespace,
            array=current_array_name,
            array_metadata=models.ArrayInfoUpdate(
                description=description,
                name=array_name,
                uri=uri,
                access_credentials_name=access_credentials_name,
                tags=tags,
            ),
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.maybe_wrap(exc) from None


def update_file_properties(uri, file_type=None, file_properties=None, async_req=False):
    """
    Update an Array to indicate its a file and has given properties.
    Any properties set are returned with the array info.
    :param str uri: uri of array to update
    :param str file_type: file type to set
    :param dict file_properties: dictionary of properties to set
    :return:
    """

    api_instance = client.build(rest_api.ArrayApi)
    (namespace, current_array_name) = split_uri(uri)

    try:
        return api_instance.update_array_metadata(
            namespace=namespace,
            array=current_array_name,
            array_metadata=models.ArrayInfoUpdate(
                file_type=file_type, file_properties=file_properties
            ),
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.maybe_wrap(exc) from None


def register_array(
    uri,
    namespace=None,
    array_name=None,
    description=None,
    access_credentials_name=None,
    async_req=False,
    dest_uri: Optional[str] = None,
):
    """
    Register this array with the tiledb cloud service

    :param str uri: storage URI of array.
    :param str namespace: The user or organization to register the array
        under. If unset will default to the user
    :param str array_name: name of array, optional. Defaults to stem of
        the storage URI.
    :param str description: optional description
    :param str access_credentials_name: optional name of access
        credentials to use. If left blank default for namespace will be
        used.
    :param async_req: return future instead of results for async support
    :param dest_uri: If set, the ``tiledb://`` URI of the destination.
    """
    api_instance = client.build(rest_api.ArrayApi)

    namespace, array_name = utils.canonicalize_ns_name_uri(
        namespace=namespace, array_name=array_name, dest_uri=dest_uri
    )

    namespace = namespace or client.default_user().username

    if not array_name:
        # Extract the basename from the storage URI and use it for the name.
        parsed_uri = urllib.parse.urlparse(uri)
        array_name = posixpath.basename(parsed_uri.path)

    try:
        return api_instance.register_array(
            namespace=namespace,
            array=uri,
            array_metadata=models.ArrayInfoUpdate(
                description=description,
                name=array_name,
                uri=uri,
                access_credentials_name=access_credentials_name,
            ),
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.maybe_wrap(exc) from None


def deregister_array(uri, async_req=False):
    """
    Deregister the from the tiledb cloud service.
    This does not physically delete the array, it will remain in your bucket.
    All access to the array and cloud metadata will be removed.

    :param async_req: return future instead of results for async support

    :return success or error
    """
    (namespace, array_name) = split_uri(uri)

    api_instance = client.build(rest_api.ArrayApi)

    try:
        return api_instance.deregister_array(
            namespace=namespace, array=array_name, async_req=async_req
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.maybe_wrap(exc) from None


def delete_array(uri, *, async_req=False):
    """
    Deregister the array from the tiledb cloud service,
    then deletes physical array from disk.

    All access to the array and cloud metadata will be removed.

    :param async_req: return future instead of results for async support

    :return success or error
    """
    (namespace, array_name) = split_uri(uri)

    api_instance = client.build(rest_api.ArrayApi)

    try:
        return api_instance.delete_array(
            namespace=namespace,
            array=array_name,
            content_type="application/json",
            async_req=async_req,
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.maybe_wrap(exc) from None


def array_activity(uri, async_req=False):
    """
    Fetch array activity
    :param uri:
    :param async_req: return future instead of results for async support
    :return:
    """
    (namespace, array_name) = split_uri(uri)

    api_instance = client.build(rest_api.ArrayApi)

    try:
        return api_instance.array_activity_log(
            namespace=namespace, array=array_name, async_req=async_req
        )
    except GenApiException as exc:
        raise tiledb_cloud_error.maybe_wrap(exc) from None


def parse_ranges(ranges):
    """
    Takes a list of the following objects per dimension:

    - scalar index
    - (start,end) tuple
    - list of either of the above types

    :param ranges: list of (scalar, tuple, list)
    :param builder: function taking arguments (dim_idx, start, end)
    :return:
    """

    def make_range(dim_range):
        if isinstance(dim_range, (int, float, numpy.datetime64, numpy.timedelta64)):
            start, end = dim_range, dim_range
        elif isinstance(dim_range, (tuple, list)):
            if len(dim_range) == 0:
                return []
            elif len(dim_range) == 1:
                start, end = dim_range[0]
            elif len(dim_range) == 2:
                start, end = dim_range[0], dim_range[1]
            else:
                raise ValueError("List or tuple has count greater than 2 element")
        elif isinstance(dim_range, slice):
            assert dim_range.step is None, "slice steps are not supported!"
            start, end = dim_range.start, dim_range.stop
        elif dim_range is None:
            return []
        else:
            raise ValueError("Unknown index type! (type: '{}')".format(type(dim_range)))

        # Convert datetimes to int64
        if type(start) == numpy.datetime64 or type(start) == numpy.timedelta64:
            start = start.astype("int64").item()
        if type(end) == numpy.datetime64 or type(end) == numpy.timedelta64:
            end = end.astype("int64").item()

        return [start, end]

    result = list()
    for dim_idx, dim_range in enumerate(ranges):
        dim_list = []
        if isinstance(dim_range, numpy.ndarray):
            dim_list = dim_range.tolist()
        elif isinstance(
            dim_range, (int, float, tuple, slice, numpy.datetime64, numpy.timedelta64)
        ):
            dim_list = make_range(dim_range)
        elif isinstance(dim_range, list):
            for r in dim_range:
                dim_list.extend(make_range(r))
        elif dim_range is None:
            pass
        else:
            raise ValueError(
                "Unknown subarray/index type! (type: '{}', "
                ", idx: '{}', value: '{}')".format(type(dim_range), dim_idx, dim_range)
            )
        result.append(dim_list)

    return json_safe.Value(result)


def apply_base(
    array: Union[object, str],
    func: Union[str, Callable, Asset],
    *,
    teamspace: Union[Teamspace, str] = None,
    ranges: Sequence = (),
    attrs: Sequence = (),
    layout: Optional[str] = None,
    image_name: str = "default",
    http_compressor: str = "deflate",
    include_source_lines: bool = True,
    task_name: Optional[str] = None,
    result_format: str = models.ResultFormat.NATIVE,
    store_results: bool = False,
    stored_param_uuids: Iterable[uuid.UUID] = (),
    timeout: int = None,
    resource_class: Optional[str] = None,
    _download_results: bool = True,
    _server_graph_uuid: Optional[uuid.UUID] = None,
    _client_node_uuid: Optional[uuid.UUID] = None,
    **kwargs: Any,
) -> results.RemoteResult:
    """Apply a user-defined function to an array.

    Parameters
    ----------
    array : str or object
        The array asset to run the function on, identified by path,
        object, or "tiledb" URI.
    func : callable or Asset-like
        The function to run. This can be either a callable function, or
        a registered function asset identified by path, object, or
        "tiledb" URI.
    teamspace : TeamspaceLike, optional
        The teamspace to execute the UDF under. If the func or arrays
        parameters specify a teamspace, this parameter may be omitted.
    ranges : list, optional
        Ranges to issue query on.
    attrs : list, optional
        List of attributes or dimensions to fetch in query.
    layout : str, optional
        Tiledb query layout.
    image_name : str, optional
        UDF image name to use, useful for testing beta features.
    http_compressor : str, optional
        Set http compressor for results.
    include_source_lines : bool, optional
        True to send the source code of your UDF to the server with your
        request. (This means it can be shown to you in stack traces if
        an error occurs.) False to send only compiled Python bytecode.
    task_name : str, optional
        Name to assign the task for logging and audit purposes.
    result_format :  ResultFormat, optional
        Result serialization format.
    store_results : bool, optional
        True to temporarily store results on the server side for later
        retrieval (in addition to downloading them).
    stored_param_uuids : list, optional
        A list of UUIDs.
    timeout : int, optional
        Timeout for UDF in seconds.
    resource_class : str, optional
        The name of the resource class to use. Resource classes define
        maximum limits for cpu and memory usage.
    _download_results : bool, optional
        True to download and parse results eagerly.  False to not
        download results by default and only do so lazily (e.g. for an
        intermediate node in a graph).
    _server_graph_uuid : str, optional
        If this function is being executed within a DAG, the
        server-generated ID of the graph's log. Otherwise, None.
    _client_node_uuid : str, optional
        If this function is being executed within a DAG, the ID of this
        function's node within the graph. Otherwise, None.
    kwargs : dict
        named arguments to pass to function.

    Returns
    -------
    results.RemoteResult
        A future containing the results of the UDF.

    Examples
    --------
    >>> import numpy
    >>> def median(df):
    ...   return numpy.median(df["a"])
    ...
    >>> tiledb.cloud.array.apply_base(
    ...     "folder/array",
    ...     median,
    ...     teamspace="teamspace",
    ...     ranges=[(0,5), (0,5)],
    ...     attrs=["a", "b", "c"]
    ... ).result
    2.0

    """
    teamspace_id, array_id = _normalize_ids(teamspace, array)

    array_list = ArrayList()
    array_list.add(
        uri=f"tiledb://{client.get_workspace_id()}/{teamspace_id}/{array_id.lstrip('/')}",
        layout=layout,
        ranges=ranges,
        buffers=attrs,
    )

    udf_model = models.MultiArrayUDF(
        language=models.UDFLanguage.PYTHON,
        arrays=array_list.get(),
        version=utils.PYTHON_VERSION,
        image_name=image_name,
        task_name=task_name,
        result_format=result_format,
        store_results=store_results,
        stored_param_uuids=list(str(uuid) for uuid in stored_param_uuids),
        resource_class=resource_class,
        dont_download_results=not _download_results,
        task_graph_uuid=_server_graph_uuid and str(_server_graph_uuid),
        client_node_uuid=_client_node_uuid and str(_client_node_uuid),
    )

    if timeout is not None:
        udf_model.timeout = timeout

    if callable(func):
        udf_model._exec = utils.b64_pickle(func)
        if include_source_lines:
            udf_model.exec_raw = functions.getsourcelines(func)
    else:
        if isinstance(func, Asset):
            teamspace_id = func.teamspace_id
            func = func.path
        else:
            func_teamspace_id, func = _normalize_ids(teamspace, func)

        if not func.startswith("/"):
            func = "/" + func
        udf_model.udf_info_name = f"{func_teamspace_id}/{func}"

    json_arguments: List[object] = []
    json_arguments.extend(array_list._to_tgudf_args())
    json_arguments.extend(
        udf._StoredParamJSONer().encode_arguments(types.Arguments((), kwargs))
    )
    udf_model.arguments_json = json_arguments

    if kwargs:
        udf_model.argument = utils.b64_pickle((kwargs,))

    submit_kwargs = dict(
        udf=udf_model,
    )

    if http_compressor:
        submit_kwargs["accept_encoding"] = http_compressor

    api_instance = client.build(rest_api.UdfApi)

    return sender.send_udf_call(
        client.get_workspace_id(),
        teamspace_id,
        api_instance.submit_multi_array_udf,
        submit_kwargs,
        decoders.Decoder(result_format),
        id_callback=_maybe_set_last_udf_id,
        results_stored=store_results,
        results_downloaded=_download_results,
    )


@functions.signature_of(apply_base)
def apply(*args, **kwargs) -> Any:
    """
    Apply a user defined function to an array, synchronously.

    All arguments are exactly as in :func:`apply_base`, but this returns
    the data only.

    **Example:**

    >>> import tiledb, tiledb.client, numpy
    >>> def median(df):
    ...   return numpy.median(df["a"])
    >>> # Open the array then run the UDF
    >>> tiledb.client.array.apply("tiledb://TileDB-Inc/quickstart_dense", median, [(0,5), (0,5)], attrs=["a", "b", "c"])
    2.0
    """  # noqa: E501
    return apply_base(*args, **kwargs).get()


def apply_async(*args, **kwargs) -> results.AsyncResult:
    """Apply a user-defined function to an array, asynchronously.

    All arguments are exactly as in :func:`apply_base`, but this returns
    the data as a future-like AsyncResponse.
    """
    return sender.wrap_async_base_call(apply_base, *args, **kwargs)


def exec_multi_array_udf_base(
    func: Union[Callable, AssetLike],
    arrays: Union[List[dict[str, Any]], ArrayList],
    *,
    teamspace: Union[Teamspace, str] = None,
    image_name: str = "default",
    http_compressor: Optional[str] = "deflate",
    include_source_lines: bool = True,
    task_name: Optional[str] = None,
    result_format: str = models.ResultFormat.NATIVE,
    store_results: bool = False,
    stored_param_uuids: Iterable[uuid.UUID] = (),
    resource_class: Optional[str] = None,
    _download_results: bool = True,
    _server_graph_uuid: Optional[uuid.UUID] = None,
    _client_node_uuid: Optional[uuid.UUID] = None,
    **kwargs,
) -> results.RemoteResult:
    """
    Apply a user-defined function to multiple arrays.

    Parameters
    ----------
    func : callable or Asset-like
        The function to run. This can be either a callable function, or
        a registered function asset identified by path, object, or
        "tiledb" URI.
    arrays : list
        The list of arrays to run the function on, as an already-built
        ArrayList object, or as a list of dicts with "uri", "ranges",
        and "attrs" members.
    teamspace : TeamspaceLike, optional
        The teamspace to execute the UDF under. If the func or arrays
        parameters specify a teamspace, this parameter may be omitted.
    image_name : str, optional
        UDF image name to use, useful for testing beta features.
    http_compressor : str, optional
        Set http compressor for results.
    task_name : str, optional
        Name to assign the task for logging and audit purposes.
    result_format :  ResultFormat, optional
        Result serialization format.
    store_results : bool, optional
        True to temporarily store results on the server side for later
        retrieval (in addition to downloading them).
    _server_graph_uuid : str, optional
        If this function is being executed within a DAG, the
        server-generated ID of the graph's log. Otherwise, None.
    _client_node_uuid : str, optional
        If this function is being executed within a DAG, the ID of this
        function's node within the graph. Otherwise, None.
    resource_class : str, optional
        The name of the resource class to use. Resource classes define
        maximum limits for cpu and memory usage.
    kwargs : dict
        named arguments to pass to function.

    Returns
    -------
    results.RemoteResult
        A future containing the results of the UDF.

    Examples
    --------
    >>> import numpy as np
    >>> def median(numpy_ordered_dictionary):
    ...     return np.median(
    ...         numpy_ordered_dictionary[0]["a"]) + np.median(numpy_ordered_dictionary[1]["a"]
    ...     )
    ...
    >>> exec_multi_array_udf_base(
    ...     median, [
    ...         {"array": "folder/array1", "ranges": [(1, 4), (1, 4)], "attrs": ["a"]},
    ...         {"array": "folder/array2", "ranges": [(1, 4), (1, 4)], "attrs": ["a"]},
    ...     ],
    ...     teamspace="teamspace"
    ... ).get()

    """
    if isinstance(arrays, ArrayList):
        array_list = arrays
    else:
        array_list = ArrayList()
        for spec in arrays:
            teamspace_id, array_id = _normalize_ids(teamspace, spec["uri"])
            array_list.add(
                uri=f"tiledb://{client.get_workspace_id()}/{teamspace_id}/{array_id.lstrip('/')}",
                ranges=spec.get("ranges", []),
                buffers=spec.get("attrs", []),
                layout=spec.get("layout", None),
            )

    udf_model = models.MultiArrayUDF(
        language=models.UDFLanguage.PYTHON,
        arrays=array_list.get(),
        version=utils.PYTHON_VERSION,
        image_name=image_name,
        task_name=task_name,
        result_format=result_format,
        store_results=store_results,
        stored_param_uuids=list(str(uuid) for uuid in stored_param_uuids),
        resource_class=resource_class,
        dont_download_results=not _download_results,
        task_graph_uuid=_server_graph_uuid and str(_server_graph_uuid),
        client_node_uuid=_client_node_uuid and str(_client_node_uuid),
    )

    if isinstance(func, Asset):
        teamspace_id = func.teamspace_id
        func = func.path
    elif isinstance(func, str):
        teamspace_id, func = _normalize_ids(teamspace, func)

    if callable(func):
        udf_model._exec = utils.b64_pickle(func)
        if include_source_lines:
            udf_model.exec_raw = functions.getsourcelines(func)
    else:
        if not func.startswith("/"):
            func = "/" + func
        udf_model.udf_info_name = f"{teamspace_id}/{func}"

    json_arguments: List[object] = []
    json_arguments.extend(array_list._to_tgudf_args())
    json_arguments.extend(
        udf._StoredParamJSONer().encode_arguments(types.Arguments((), kwargs))
    )
    if kwargs:
        udf_model.argument = utils.b64_pickle((kwargs,))

    submit_kwargs = dict(
        udf=udf_model,
    )
    if http_compressor:
        submit_kwargs["accept_encoding"] = http_compressor

    api_instance = client.build(rest_api.UdfApi)

    return sender.send_udf_call(
        client.get_workspace_id(),
        teamspace_id,
        api_instance.submit_multi_array_udf,
        submit_kwargs,
        decoders.Decoder(result_format),
        id_callback=_maybe_set_last_udf_id,
        results_stored=store_results,
        results_downloaded=_download_results,
    )


@functions.signature_of(exec_multi_array_udf_base)
def exec_multi_array_udf(*args, **kwargs) -> Any:
    """Apply a user-defined function to multiple arrays, synchronously.

    All arguments are exactly as in :func:`exec_multi_array_udf_base`.
    """
    return exec_multi_array_udf_base(*args, **kwargs).get()


@functions.signature_of(exec_multi_array_udf_base)
def exec_multi_array_udf_async(*args, **kwargs) -> results.AsyncResult:
    """Apply a user-defined function to multiple arrays, asynchronously.

    All arguments are exactly as in :func:`exec_multi_array_udf_base`.
    """
    return sender.wrap_async_base_call(exec_multi_array_udf_base, *args, **kwargs)


def _pick_func(**kwargs: Union[str, Callable, None]) -> Union[str, Callable]:
    """Extracts the exactly *one* function from the provided arguments.

    Raises an error if either zero or more than one functions is passed.
    Uses the names of the arguments as part of the error message.
    """

    result: Union[str, Callable, None] = None
    count = 0

    for val in kwargs.values():
        if val:
            result = val
            count += 1

    if count != 1:
        names = ", ".join(kwargs)
        raise TypeError(f"exactly 1 of [{names}] must be provided")
    if not callable(result) and type(result) != str or not result:
        raise TypeError(
            "provided function must be a callable or the str name of a UDF, "
            f"not {type(result)}"
        )
    return result


def _maybe_set_last_udf_id(task_id: Optional[uuid.UUID]) -> None:
    """Tries to set the last_udf_id from the exception, if present."""
    global last_udf_task_id
    if task_id:
        last_udf_task_id = str(task_id)
