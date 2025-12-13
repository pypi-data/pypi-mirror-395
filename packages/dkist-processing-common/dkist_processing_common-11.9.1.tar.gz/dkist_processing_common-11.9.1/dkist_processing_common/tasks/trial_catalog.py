"""Tasks to support the generation of downstream artifacts in a trial workflow that wouldn't otherwise produce them."""

import importlib
import logging
from datetime import datetime
from itertools import chain
from pathlib import Path
from typing import Any
from typing import Generator
from uuid import uuid4

from dkist_processing_common.codecs.asdf import asdf_fileobj_encoder
from dkist_processing_common.codecs.basemodel import basemodel_decoder
from dkist_processing_common.codecs.fits import fits_access_decoder
from dkist_processing_common.codecs.json import json_encoder
from dkist_processing_common.codecs.path import path_decoder
from dkist_processing_common.codecs.quality import quality_data_decoder
from dkist_processing_common.models.fits_access import FitsAccessBase
from dkist_processing_common.models.input_dataset import InputDatasetPartDocumentList
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks.output_data_base import OutputDataBase

logger = logging.getLogger(__name__)

__all__ = ["CreateTrialDatasetInventory", "CreateTrialAsdf", "CreateTrialQualityReport"]


# Capture condition of dkist-processing-common[inventory] install
INVENTORY_EXTRA_INSTALLED = False
try:
    from dkist_inventory.inventory import generate_asdf_filename
    from dkist_inventory.inventory import generate_inventory_from_frame_inventory
    from dkist_inventory.inventory import generate_quality_report_filename

    INVENTORY_EXTRA_INSTALLED = True
except ModuleNotFoundError:
    pass

# Capture condition of dkist-processing-common[asdf] install
ASDF_EXTRA_INSTALLED = False
try:
    import asdf
    from dkist_inventory.asdf_generator import asdf_tree_from_filenames
    from dkist_inventory.asdf_generator import make_asdf_file_object

    ASDF_EXTRA_INSTALLED = True
except ModuleNotFoundError:
    pass

# Verify dkist-quality is installed
QUALITY_EXTRA_INSTALLED = False
try:
    from dkist_quality.report import ReportFormattingException
    from dkist_quality.report import format_report

    QUALITY_EXTRA_INSTALLED = True
except ModuleNotFoundError:
    pass


class CreateTrialDatasetInventory(OutputDataBase):
    """
    Task for use in Trial workflows that can simulate the generation of dataset inventory for the dataset.

    Warning: This task requires the dkist-inventory package.
    """

    def pre_run(self) -> None:
        """Require the dkist-inventory package be installed."""
        if not INVENTORY_EXTRA_INSTALLED:
            raise ModuleNotFoundError(
                f"{self.__class__.__name__} Task requires the dkist-inventory package "
                f"(e.g. via an 'inventory' pip_extra on dkist_processing_core.Workflow().add_node())"
                f" but the required dependencies were not found."
            )

    @property
    def output_frames(self) -> Generator[FitsAccessBase, None, None]:
        """Return the FitsAccess objects for the dataset-inventory-able frames."""
        yield from self.read(
            tags=self.output_frame_tags,
            decoder=fits_access_decoder,
            fits_access_class=FitsAccessBase,
        )

    @property
    def frame_inventories(self) -> Generator[dict, None, None]:
        """Return frame inventory dictionaries for the dataset-inventory-able frames."""
        for frame in self.output_frames:
            frame_inventory = frame.header_dict
            # keys that are added to inventory but are not in the header
            frame_inventory["objectKey"] = self.format_object_key(Path(frame.name))
            frame_inventory["_id"] = uuid4().hex
            frame_inventory["bucket"] = self.destination_bucket
            frame_inventory["frameStatus"] = "AVAILABLE"
            frame_inventory["createDate"] = datetime.utcnow().isoformat("T")
            frame_inventory["updateDate"] = None
            frame_inventory["lostDate"] = None
            frame_inventory["headerHDU"] = 1
            yield frame_inventory

    def run(self) -> None:
        """Generate a json file simulating the dataset inventory record that would be produced when cataloging the dataset."""
        with self.telemetry_span("Retrieve output frame headers"):
            json_headers = list(self.frame_inventories)
        with self.telemetry_span("Generate dataset inventory"):
            inventory: dict = generate_inventory_from_frame_inventory(
                bucket=self.destination_bucket, json_headers=json_headers
            )
        with self.telemetry_span("Save dataset inventory file"):
            self.write(
                inventory,
                tags=[Tag.output(), Tag.dataset_inventory()],
                encoder=json_encoder,
                relative_path=f"{self.constants.dataset_id}_inventory.json",
            )


class CreateTrialAsdf(OutputDataBase):
    """
    Task for use in Trial workflows that can simulate the generation of an ASDF file for the dataset.

    Warning: This task requires the dkist-inventory[asdf] package.
    """

    def pre_run(self) -> None:
        """Require the dkist-inventory[asdf] package be installed."""
        if not ASDF_EXTRA_INSTALLED:
            raise ModuleNotFoundError(
                f"{self.__class__.__name__} Task requires the dkist-inventory[asdf] package "
                f"(e.g. via an 'asdf' pip_extra on dkist_processing_core.Workflow().add_node()) "
                f"but the required dependencies were not found."
            )

    @property
    def absolute_output_frame_paths(self) -> Generator[Path, None, None]:
        """Return the Path objects for the dataset-inventory-able frames."""
        yield from self.read(
            tags=self.output_frame_tags,
            decoder=path_decoder,
        )

    def run(self) -> None:
        """Generate an ASDF file simulating the ASDF file that would be produced when cataloging the dataset."""
        with self.telemetry_span("Collate input dataset parameters"):
            parameters = self.parse_input_dataset_parameters()

        with self.telemetry_span("Generate ASDF tree"):
            tree = asdf_tree_from_filenames(
                filenames=self.absolute_output_frame_paths,
                hdu=1,  # compressed
                relative_to=self.scratch.workflow_base_path,
                parameters=parameters,
            )

        trial_history = [
            (
                "Written with dkist-processing-common trial ASDF writer",
                {
                    "name": "dkist-processing-common",
                    "author": "DKIST Data Center",
                    "homepage": "https://bitbucket.org/dkistdc/dkist-processing-common",
                    "version": importlib.metadata.distribution("dkist-processing-common").version,
                },
            )
        ]
        with self.telemetry_span("Save ASDF file"):
            with make_asdf_file_object(tree, extra_history=trial_history) as asdf_obj:
                self.write(
                    asdf_obj,
                    tags=[Tag.output(), Tag.asdf()],
                    encoder=asdf_fileobj_encoder,
                    relative_path=generate_asdf_filename(
                        instrument=self.constants.instrument,
                        start_time=datetime.fromisoformat(self.constants.obs_ip_start_time),
                        dataset_id=self.constants.dataset_id,
                    ),
                )

    def parse_input_dataset_parameters(self) -> list[dict[str, Any]]:
        """
        Return the parameters associated with the dataset.

        Returns
        -------
        list[dict[str, Any]]
            A list of dictionaries, each containing a parameter name and its values.

        Raises
        ------
        ValueError
            If there is not exactly one ``InputDatasetPartDocumentList`` found.
        """
        part_docs_iter = self.read(
            tags=Tag.input_dataset_parameters(),
            decoder=basemodel_decoder,
            model=InputDatasetPartDocumentList,
        )
        docs = list(part_docs_iter)

        if not docs:
            logger.warning("No parameter list decoded from files")
            return []

        if len(docs) > 1:
            raise ValueError(f"Expected 1 parameter list, found {len(docs)}")

        parameters = docs[0].model_dump(by_alias=True).get("doc_list", [])
        return parameters


class CreateTrialQualityReport(OutputDataBase):
    """
    Task for use in Trial workflows to generate the quality report for the dataset.

    Warning: This task requires the dkist-quality package.
    """

    def pre_run(self) -> None:
        """Require the dkist-quality package be installed."""
        if not QUALITY_EXTRA_INSTALLED:
            raise ModuleNotFoundError(
                f"{self.__class__.__name__} Task requires the dkist-quality package "
                f"(e.g. via a 'quality' pip_extra on dkist_processing_core.Workflow().add_node())"
                f" but the required dependencies were not found."
            )

        if not INVENTORY_EXTRA_INSTALLED:
            raise ModuleNotFoundError(
                f"{self.__class__.__name__} Task requires the dkist-inventory package "
                f"(e.g. via an 'inventory' pip_extra on dkist_processing_core.Workflow().add_node())"
                f" but the required dependencies were not found."
            )

    def run(self) -> None:
        """Generate the quality report for the dataset."""
        self.create_trial_quality_report()

    def create_trial_quality_report(self) -> None:
        """Generate a trial quality report in pdf format and save to the file system for future upload."""
        with self.telemetry_span(f"Building the trial quality report"):
            # each quality_data file is a list - this will combine the elements of multiple lists into a single list
            quality_data = list(
                chain.from_iterable(
                    self.read(tags=Tag.quality_data(), decoder=quality_data_decoder)
                )
            )
            quality_report = format_report(
                report_data=quality_data, dataset_id=self.constants.dataset_id
            )

        with self.telemetry_span(f"Saving the trial quality report to the file system"):
            self.write(
                quality_report,
                tags=[Tag.output(), Tag.quality_report()],
                relative_path=generate_quality_report_filename(
                    dataset_id=self.constants.dataset_id
                ),
            )
