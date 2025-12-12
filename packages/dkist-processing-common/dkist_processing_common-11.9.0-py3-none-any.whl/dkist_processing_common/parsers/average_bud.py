"""Pre-made flower that reads a single header key from all files with specific task types and returns the average."""

from enum import StrEnum
from statistics import mean
from typing import Callable
from typing import Hashable

import numpy as np

from dkist_processing_common.parsers.near_bud import TaskNearFloatBud
from dkist_processing_common.parsers.task import passthrough_header_ip_task


class TaskAverageBud(TaskNearFloatBud):
    """
    Pre-made bud that returns the average of a single header key from all files with specific task types.

    Parameters
    ----------
    constant_name
        The name for the constant to be defined

    metadata_key
        The metadata key associated with the constant

    ip_task_types
        Only consider objects whose parsed header IP task type matches a string in this list

    task_type_parsing_function
        The function used to convert a header into an IP task type
    """

    key_to_petal_dict: dict[str, float]

    def __init__(
        self,
        constant_name: str,
        metadata_key: str | StrEnum,
        ip_task_types: str | list[str],
        task_type_parsing_function: Callable = passthrough_header_ip_task,
    ):
        super().__init__(
            constant_name=constant_name,
            metadata_key=metadata_key,
            ip_task_types=ip_task_types,
            tolerance=np.inf,
            task_type_parsing_function=task_type_parsing_function,
        )
