"""Experiment Id parser."""

from dkist_processing_common.models.constants import BudName
from dkist_processing_common.models.fits_access import MetadataKey
from dkist_processing_common.models.task_name import TaskName
from dkist_processing_common.parsers.id_bud import ContributingIdsBud
from dkist_processing_common.parsers.unique_bud import TaskUniqueBud


class ExperimentIdBud(TaskUniqueBud):
    """Class to create a Bud for the experiment_id."""

    def __init__(self):
        super().__init__(
            constant_name=BudName.experiment_id,
            metadata_key=MetadataKey.experiment_id,
            ip_task_types=TaskName.observe,
        )


class ContributingExperimentIdsBud(ContributingIdsBud):
    """Class to create a Bud for the supporting experiment_ids."""

    def __init__(self):
        super().__init__(
            constant_name=BudName.contributing_experiment_ids,
            metadata_key=MetadataKey.experiment_id,
        )
