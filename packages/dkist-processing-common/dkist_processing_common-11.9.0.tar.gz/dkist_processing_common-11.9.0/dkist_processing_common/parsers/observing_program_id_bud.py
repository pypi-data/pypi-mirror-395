"""Observing Program Id parser."""

from typing import Callable

from dkist_processing_common.models.fits_access import MetadataKey
from dkist_processing_common.parsers.id_bud import TaskContributingIdsBud
from dkist_processing_common.parsers.task import passthrough_header_ip_task


class TaskContributingObservingProgramExecutionIdsBud(TaskContributingIdsBud):
    """Class to create a Bud for the supporting observing_program_execution_ids."""

    def __init__(
        self,
        constant_name: str,
        ip_task_types: str | list[str],
        task_type_parsing_function: Callable = passthrough_header_ip_task,
    ):
        super().__init__(
            constant_name=constant_name,
            metadata_key=MetadataKey.observing_program_execution_id,
            ip_task_types=ip_task_types,
            task_type_parsing_function=task_type_parsing_function,
        )
