"""Time parser."""

from datetime import datetime
from datetime import timezone
from enum import StrEnum
from typing import Callable
from typing import Hashable
from typing import Type

import numpy as np

from dkist_processing_common.models.constants import BudName
from dkist_processing_common.models.fits_access import MetadataKey
from dkist_processing_common.models.flower_pot import SpilledDirt
from dkist_processing_common.models.flower_pot import Stem
from dkist_processing_common.models.tags import EXP_TIME_ROUND_DIGITS
from dkist_processing_common.models.tags import StemName
from dkist_processing_common.models.task_name import TaskName
from dkist_processing_common.parsers.l0_fits_access import L0FitsAccess
from dkist_processing_common.parsers.single_value_single_key_flower import (
    SingleValueSingleKeyFlower,
)
from dkist_processing_common.parsers.task import passthrough_header_ip_task
from dkist_processing_common.parsers.unique_bud import TaskUniqueBud


class ObsIpStartTimeBud(TaskUniqueBud):
    """A unique bud that yields the IP start time of the observe task."""

    def __init__(self):
        super().__init__(
            constant_name=BudName.obs_ip_start_time,
            metadata_key=MetadataKey.ip_start_time,
            ip_task_types=TaskName.observe,
        )


class TaskDatetimeBudBase(Stem):
    """
    Base class for making datetime-related buds.

    Returns a tuple of sorted values converted from datetimes to unix seconds.

    Complicated parsing of the header into a task type can be achieved by passing in a different
    header task parsing function.

    Parameters
    ----------
    stem_name
        The name for the constant to be defined

    metadata_key
        The metadata key associated with the constant

    ip_task_types
        Only consider objects whose parsed header IP task type matches a string in this list

    header_type_parsing_func
        The function used to convert a header into an IP task type
    """

    key_to_petal_dict: dict[str, float]

    def __init__(
        self,
        stem_name: str,
        metadata_key: str | StrEnum,
        ip_task_types: str | list[str],
        task_type_parsing_function: Callable = passthrough_header_ip_task,
    ):
        super().__init__(stem_name=stem_name)

        if isinstance(metadata_key, StrEnum):
            metadata_key = metadata_key.name
        self.metadata_key = metadata_key
        if isinstance(ip_task_types, str):
            ip_task_types = [ip_task_types]
        self.ip_task_types = [task.casefold() for task in ip_task_types]
        self.header_parsing_function = task_type_parsing_function

    def setter(self, fits_obj: L0FitsAccess) -> float | Type[SpilledDirt]:
        """
        Store the metadata key datetime value as unix seconds if the task type is in the desired types.

        Parameters
        ----------
        fits_obj
            The input fits object
        Returns
        -------
        The datetime in seconds
        """
        task = self.header_parsing_function(fits_obj)

        if task.casefold() in self.ip_task_types:
            return (
                datetime.fromisoformat(getattr(fits_obj, self.metadata_key))
                .replace(tzinfo=timezone.utc)
                .timestamp()
            )

        return SpilledDirt

    def getter(self, key: Hashable) -> tuple[float, ...]:
        """
        Return a tuple of sorted times in unix seconds.

        Parameters
        ----------
        key
            The input key

        Returns
        -------
        A tuple that is sorted times in unix seconds
        """
        return tuple(sorted(list(self.key_to_petal_dict.values())))


class CadenceBudBase(TaskDatetimeBudBase):
    """Base class for all Cadence Buds."""

    def __init__(self, constant_name: str):
        super().__init__(
            stem_name=constant_name,
            metadata_key=MetadataKey.time_obs,
            ip_task_types=TaskName.observe,
        )


class AverageCadenceBud(CadenceBudBase):
    """Class for the average cadence Bud."""

    def __init__(self):
        super().__init__(constant_name=BudName.average_cadence)

    def getter(self, key) -> np.float64:
        """
        Return the mean cadence between frames.

        Parameters
        ----------
        key
            The input key

        Returns
        -------
        The mean value of the cadences of the input frames
        """
        return np.mean(np.diff(super().getter(key)))


class MaximumCadenceBud(CadenceBudBase):
    """Class for the maximum cadence bud."""

    def __init__(self):
        super().__init__(constant_name=BudName.maximum_cadence)

    def getter(self, key) -> np.float64:
        """
        Return the maximum cadence between frames.

        Parameters
        ----------
        key
            The input key

        Returns
        -------
        The maximum cadence between frames
        """
        return np.max(np.diff(super().getter(key)))


class MinimumCadenceBud(CadenceBudBase):
    """Class for the minimum cadence bud."""

    def __init__(self):
        super().__init__(constant_name=BudName.minimum_cadence)

    def getter(self, key) -> np.float64:
        """
        Return the minimum cadence between frames.

        Parameters
        ----------
        key
            The input key

        Returns
        -------
        The minimum cadence between frames
        """
        return np.min(np.diff(super().getter(key)))


class VarianceCadenceBud(CadenceBudBase):
    """Class for the variance cadence Bud."""

    def __init__(self):
        super().__init__(constant_name=BudName.variance_cadence)

    def getter(self, key) -> np.float64:
        """
        Return the cadence variance between frames.

        Parameters
        ----------
        key
            The input key
        Returns
        -------
        Return the variance of the cadences over the input frames
        """
        return np.var(np.diff(super().getter(key)))


class TaskDateBeginBud(TaskDatetimeBudBase):
    """Class for the date begin task Bud."""

    def __init__(
        self,
        constant_name: str,
        ip_task_types: str | list[str],
        task_type_parsing_function: Callable = passthrough_header_ip_task,
    ):
        super().__init__(
            stem_name=constant_name,
            metadata_key=MetadataKey.time_obs,
            ip_task_types=ip_task_types,
            task_type_parsing_function=task_type_parsing_function,
        )

    def getter(self, key) -> str:
        """
        Return the earliest date begin for the ip task type converted from unix seconds to datetime string.

        Parameters
        ----------
        key
            The input key
        Returns
        -------
        Return the minimum date begin as a datetime string
        """
        min_time = super().getter(key)[0]
        min_time_dt = datetime.fromtimestamp(min_time, tz=timezone.utc)
        return min_time_dt.strftime("%Y-%m-%dT%H:%M:%S.%f")


class RoundTimeFlowerBase(SingleValueSingleKeyFlower):
    """Base flower for SingleValueSingleKeyFlowers that need to round their values to avoid value jitter."""

    def setter(self, fits_obj: L0FitsAccess):
        """
        Set the exposure time for this flower.

        Parameters
        ----------
        fits_obj
            The input fits object
        Returns
        -------
        The value of the exposure time
        """
        raw_value = super().setter(fits_obj)
        return round(raw_value, EXP_TIME_ROUND_DIGITS)


class ExposureTimeFlower(RoundTimeFlowerBase):
    """For tagging the frame FPA exposure time."""

    def __init__(self):
        super().__init__(
            tag_stem_name=StemName.exposure_time, metadata_key=MetadataKey.fpa_exposure_time_ms
        )


class ReadoutExpTimeFlower(RoundTimeFlowerBase):
    """For tagging the exposure time of each readout that contributes to an FPA."""

    def __init__(self):
        super().__init__(
            tag_stem_name=StemName.readout_exp_time,
            metadata_key=MetadataKey.sensor_readout_exposure_time_ms,
        )


class TaskRoundTimeBudBase(Stem):
    """
    Base class for making buds that need a set of rounded times for computing for specific task types.

    Metadata key values are already floats.  Returns tuple of sorted unique rounded values.

    Complicated parsing of the header into a task type can be achieved by passing in a different
    header task parsing function.

    Parameters
    ----------
    stem_name
        The name for the constant to be defined

    metadata_key
        The metadata key associated with the constant

    ip_task_types
        Only consider objects whose parsed header IP task type matches a string in this list

    header_task_parsing_func
        The function used to convert a header into an IP task type
    """

    key_to_petal_dict: dict[str, float]

    def __init__(
        self,
        stem_name: str,
        metadata_key: str | StrEnum,
        ip_task_types: str | list[str],
        header_task_parsing_func: Callable = passthrough_header_ip_task,
    ):
        super().__init__(stem_name=stem_name)

        if isinstance(metadata_key, StrEnum):
            metadata_key = metadata_key.name
        self.metadata_key = metadata_key
        if isinstance(ip_task_types, str):
            ip_task_types = [ip_task_types]
        self.ip_task_types = [task.casefold() for task in ip_task_types]
        self.header_parsing_function = header_task_parsing_func

    def setter(self, fits_obj: L0FitsAccess) -> float | Type[SpilledDirt]:
        """
        Store the metadata key value if the parsed task type is in the desired types.

        Parameters
        ----------
        fits_obj
            The input fits object
        Returns
        -------
        The rounded time
        """
        task = self.header_parsing_function(fits_obj)

        if task.casefold() in self.ip_task_types:
            raw_value = getattr(fits_obj, self.metadata_key)
            return round(raw_value, EXP_TIME_ROUND_DIGITS)

        return SpilledDirt

    def getter(self, key: Hashable) -> tuple[float, ...]:
        """
        Return a tuple of the sorted unique values found.

        Parameters
        ----------
        key
            The input key

        Returns
        -------
        A tuple that is the sorted set of unique times
        """
        return tuple(sorted(set(self.key_to_petal_dict.values())))


class TaskExposureTimesBud(TaskRoundTimeBudBase):
    """Produce a tuple of all FPA exposure times present in the dataset for a specific ip task type."""

    def __init__(
        self,
        stem_name: str,
        ip_task_types: str | list[str],
        header_task_parsing_func: Callable = passthrough_header_ip_task,
    ):
        super().__init__(
            stem_name=stem_name,
            metadata_key=MetadataKey.fpa_exposure_time_ms,
            ip_task_types=ip_task_types,
            header_task_parsing_func=header_task_parsing_func,
        )


class TaskReadoutExpTimesBud(TaskRoundTimeBudBase):
    """Produce a tuple of all sensor readout exposure times present in the dataset for a specific task type."""

    def __init__(
        self,
        stem_name: str,
        ip_task_types: str | list[str],
        header_task_parsing_func: Callable = passthrough_header_ip_task,
    ):
        super().__init__(
            stem_name=stem_name,
            metadata_key=MetadataKey.sensor_readout_exposure_time_ms,
            ip_task_types=ip_task_types,
            header_task_parsing_func=header_task_parsing_func,
        )
