"""Base classes for ID bud parsing."""

from enum import StrEnum
from typing import Callable
from typing import Type

from dkist_processing_common.models.flower_pot import SpilledDirt
from dkist_processing_common.models.flower_pot import Stem
from dkist_processing_common.parsers.l0_fits_access import L0FitsAccess
from dkist_processing_common.parsers.task import passthrough_header_ip_task


class ContributingIdsBud(Stem):
    """Base class for contributing ID buds."""

    def __init__(self, constant_name: str, metadata_key: str | StrEnum):
        super().__init__(stem_name=constant_name)
        if isinstance(metadata_key, StrEnum):
            metadata_key = metadata_key.name
        self.metadata_key = metadata_key

    def setter(self, fits_obj: L0FitsAccess) -> str:
        """
        Set the id for any type of frame.

        Parameters
        ----------
        fits_obj
            The input fits object
        Returns
        -------
        The id
        """
        return getattr(fits_obj, self.metadata_key)

    def getter(self, key) -> tuple[str, ...]:
        """
        Get all ids seen for any type of frame.

        Parameters
        ----------
        key
            The input key

        Returns
        -------
        IDs from all types of frames
        """
        return tuple(set(self.key_to_petal_dict.values()))


class TaskContributingIdsBud(ContributingIdsBud):
    """Base class for contributing ID buds for a particular task type."""

    def __init__(
        self,
        constant_name: str,
        metadata_key: str | StrEnum,
        ip_task_types: str | list[str],
        task_type_parsing_function: Callable = passthrough_header_ip_task,
    ):
        super().__init__(constant_name=constant_name, metadata_key=metadata_key)

        if isinstance(ip_task_types, str):
            ip_task_types = [ip_task_types]
        self.ip_task_types = [task.casefold() for task in ip_task_types]
        self.parsing_function = task_type_parsing_function

    def setter(self, fits_obj: L0FitsAccess) -> str | Type[SpilledDirt]:
        """Ingest an object only if its parsed IP task type matches what's desired."""
        task = self.parsing_function(fits_obj)

        if task.casefold() in self.ip_task_types:
            return super().setter(fits_obj)

        return SpilledDirt
