"""Utility functions."""

from tiledb.client.utilities._common import as_batch
from tiledb.client.utilities._common import chunk
from tiledb.client.utilities._common import find
from tiledb.client.utilities._common import max_memory_usage
from tiledb.client.utilities._common import process_stream
from tiledb.client.utilities._common import read_aws_config
from tiledb.client.utilities._common import read_file
from tiledb.client.utilities._common import run_dag
from tiledb.client.utilities._common import serialize_filter
from tiledb.client.utilities._common import set_aws_context
from tiledb.client.utilities.consolidate import consolidate_and_vacuum
from tiledb.client.utilities.consolidate import consolidate_fragments
from tiledb.client.utilities.consolidate import group_fragments
from tiledb.client.utilities.logging import get_logger
from tiledb.client.utilities.logging import get_logger_wrapper
from tiledb.client.utilities.profiler import Profiler
from tiledb.client.utilities.profiler import create_log_array
from tiledb.client.utilities.profiler import write_log_event
from tiledb.client.utilities.wheel import install_wheel
from tiledb.client.utilities.wheel import upload_wheel

__all__ = [
    "as_batch",
    "chunk",
    "find",
    "get_logger",
    "get_logger_wrapper",
    "max_memory_usage",
    "process_stream",
    "read_aws_config",
    "read_file",
    "run_dag",
    "set_aws_context",
    "consolidate_fragments",
    "consolidate_and_vacuum",
    "group_fragments",
    "serialize_filter",
    "Profiler",
    "create_log_array",
    "write_log_event",
    "upload_wheel",
    "install_wheel",
]
