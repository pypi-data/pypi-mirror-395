"""Access to information about TileDB tasks."""

import datetime
import uuid
from typing import TYPE_CHECKING, Any, Optional

import tiledb
from tiledb.client import array
from tiledb.client import client
from tiledb.client import rest_api
from tiledb.client import sql
from tiledb.client import tiledb_cloud_error
from tiledb.client._results import decoders
from tiledb.client._results import results
from tiledb.client.assets import TeamspaceLike
from tiledb.client.assets import _normalize_ids
from tiledb.client.pager import Pager
from tiledb.client.rest_api import ApiException as GenApiException
from tiledb.client.rest_api import ArrayTaskType
from tiledb.client.rest_api import models

if TYPE_CHECKING:
    import pandas


class TasksError(tiledb.TileDBError):
    """Raised when tasks can not be accessed."""


def task(id, async_req=False):
    """Fetch a single array task.

    Parameters
    ----------
    id : str
        The id to look up.

    Return
    ------
    ArrayTask
        Object with task details.

    Raises
    ------
    TasksError
        Raised when task can not be accessed.

    """

    if id is None:
        raise Exception("id parameter can not be empty")

    api_instance = client.build(rest_api.TasksApi)

    try:
        return api_instance.task_workspace_id_get(
            client.get_workspace_id(), id, async_req=async_req
        )

    except GenApiException as exc:
        raise TasksError("Can not retrieve task.") from tiledb_cloud_error.maybe_wrap(
            exc
        )


class ArrayTaskPager(Pager):
    def _generate(self):
        # Note: the tasks API is, unlike asset search, 0-indexed.
        if not self.response:
            self.call_page(0)
        if self.response.array_tasks:
            yield from self.response.array_tasks
            page = self.page + 1
            while page < self.response.pagination_metadata.total_pages:
                results_page = self.func(*self.args, page=page, **self.kwargs)
                if not results_page.array_tasks:
                    break
                yield from results_page.array_tasks
                page += 1

    @property
    def array_tasks(self):
        return self.response.array_tasks


def fetch_tasks(
    query: Optional[str] = None,
    array: Optional[str] = None,
    teamspace: Optional[TeamspaceLike] = None,
    start=None,
    end=datetime.datetime.now(datetime.timezone.utc),
    status: Optional[str] = None,
    type: Optional[ArrayTaskType] = None,
    exclude_type: Optional[list[ArrayTaskType]] = None,
    file_type: Optional[list[str]] = None,
    exclude_file_type: Optional[list[str]] = None,
    order_by: Optional[str] = None,
    page: Optional[int] = 1,
    per_page: Optional[int] = None,
) -> ArrayTaskPager:
    """Fetch all tasks a user has access to.

    Parameters
    ----------
    query : str, optional
        Query keywords.
    array : AssetLike, optional
        Filter for a specific array.
    teamspace : TeamspaceLike, optional
        Filter for a specific teamspaces, specified by object or id.
    start : datetime, optional
        Start time for listing of tasks, defaults to 7 days ago.
    end : datetime end, optional
        End time for listing of tasks. Defaults to now().
    status : ArrayTaskStatus, optional
        Filter on status, one of 'FAILED', 'RUNNING', 'COMPLETED'.
    type : ArrayTaskType, optional
        One of 'QUERY', 'SQL', 'UDF', or 'GENERIC_UDF'.
    exclude_type : list[ArrayTaskType], optional
        Exclude type of task arrays from matches, more than one can be included.
    file_type : list[str], optional
        Match file_type of task array, more than one can be included.
    exclude_file_type : list[str], optional
        Exclude file_type of task arrays from matches, more than one can be included.
    order_by : str, optional
        Sort by which field valid values include start_time, name.
    page : int, optional
        Which page of results to retrieve. 1-based.
    per_page : int, optional
        How many results to include on each page.

    Returns
    -------
    Pager for ArrayTasks

    Raises
    ------
    TasksError
        Raised when tasks can not be accessed.

    Examples
    --------
    >>> for task in fetch_tasks(status='RUNNING', start=datetime.datetime.now() - datetime.timedelta(hours=3))
    ...     print(task.id, task.start_time
    ...

    This prints the id and start time of all running tasks in the last 3 hours.

    """
    if array:
        teamspace, array = _normalize_ids(teamspace, array)

    if end is not None:
        if not isinstance(end, datetime.datetime):
            raise Exception("end must be datetime object")
        end = datetime.datetime.timestamp(end)

    if start is not None:
        if not isinstance(start, datetime.datetime):
            raise Exception("start must be datetime object")
        start = datetime.datetime.timestamp(start)

    # This API endpoint, unlike others, is 0-indexed.
    page = page - 1

    try:
        resp = ArrayTaskPager(
            client.build(rest_api.TasksApi).tasks_workspace_get,
            client.get_workspace_id(),
            search=query,
            array=array,
            teamspace=teamspace,
            start=int(start) if start else None,
            end=int(end),
            status=status,
            type=type,
            exclude_type=exclude_type,
            file_type=file_type,
            exclude_file_type=exclude_file_type,
            orderby=order_by,
            per_page=per_page,
        )
        resp.call_page(page)
    except GenApiException as exc:
        raise TasksError(
            "The task search request failed."
        ) from tiledb_cloud_error.maybe_wrap(exc)
    else:
        return resp


# maintain backwards compatibility for tiledb.client.tasks.tasks
tasks = fetch_tasks


def last_sql_task():
    """
    Fetch the last run sql array task
    :return task : object with task details
    """

    if sql.last_sql_task_id is None:
        raise Exception("There is no last run sql task in current python session")

    return task(id=sql.last_sql_task_id)


def last_udf_task():
    """
    Fetch the last run udf task
    :return task : object with task details
    """

    if array.last_udf_task_id is None:
        raise Exception("There is no last run udf task in current python session")

    return task(id=array.last_udf_task_id)


def fetch_results(
    task_id: uuid.UUID,
    *,
    result_format: Optional[str] = None,
) -> Any:
    """Fetches the results of a previously-executed UDF or SQL query."""
    decoder = None if result_format is None else decoders.Decoder(result_format)
    return results.fetch_remote(task_id, decoder)


def fetch_results_pandas(
    task_id: uuid.UUID,
    *,
    result_format: str = models.ResultFormat.NATIVE,
) -> "pandas.DataFrame":
    """Fetches the results of a previously-executed UDF or SQL query."""
    return results.fetch_remote(
        client.get_workspace_id(), task_id, decoders.PandasDecoder(result_format)
    )
