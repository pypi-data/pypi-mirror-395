"""Mixin to add methods to a Task to support globus transfers."""

import logging
from dataclasses import dataclass
from pathlib import Path

from globus_sdk import ClientCredentialsAuthorizer
from globus_sdk import ConfidentialAppAuthClient
from globus_sdk import GlobusError
from globus_sdk import TransferClient
from globus_sdk import TransferData
from globus_sdk.scopes import TransferScopes
from globus_sdk.transport import RetryConfig

from dkist_processing_common.config import common_configurations

logger = logging.getLogger(__name__)


@dataclass
class GlobusTransferItem:
    """Dataclass used to support globus transfers."""

    source_path: str | Path
    destination_path: str | Path
    recursive: bool = False  # file

    def __hash__(self) -> int:
        """Hash so we can do set stuff on these items."""
        return hash((self.source_path, self.destination_path, self.recursive))


class GlobusMixin:
    """Mixin to add methods to a Task to support globus transfers."""

    def globus_transfer_client_factory(self, transfer_data: TransferData) -> TransferClient:
        """Create a globus transfer client based on the direction of transfer and round-robin the available application credentials."""
        if (
            transfer_data["source_endpoint"] == common_configurations.object_store_endpoint
        ):  # inbound
            client_credentials = common_configurations.globus_inbound_client_credentials
        else:  # outbound
            client_credentials = common_configurations.globus_outbound_client_credentials

        # Round-robin the client credentials based on the recipe run id
        index = self.recipe_run_id % len(client_credentials)
        selected_credential = client_credentials[index]

        confidential_client = ConfidentialAppAuthClient(
            client_id=selected_credential.client_id,
            client_secret=selected_credential.client_secret,
        )
        authorizer = ClientCredentialsAuthorizer(confidential_client, scopes=TransferScopes)
        retry_config = RetryConfig(max_retries=common_configurations.globus_max_retries)

        return TransferClient(authorizer=authorizer, retry_config=retry_config)

    def globus_transfer_scratch_to_object_store(
        self,
        transfer_items: list[GlobusTransferItem],
        label: str = None,
        verify_checksum: bool = True,
    ) -> None:
        """Transfer data from scratch to the object store."""
        self.globus_transfer(
            source_endpoint=common_configurations.scratch_endpoint,
            destination_endpoint=common_configurations.object_store_endpoint,
            transfer_items=transfer_items,
            label=label,
            verify_checksum=verify_checksum,
        )

    def globus_transfer_object_store_to_scratch(
        self,
        transfer_items: list[GlobusTransferItem],
        label: str = None,
        verify_checksum: bool = True,
    ) -> None:
        """Transfer data from the object store to scratch."""
        self.globus_transfer(
            source_endpoint=common_configurations.object_store_endpoint,
            destination_endpoint=common_configurations.scratch_endpoint,
            transfer_items=transfer_items,
            label=label,
            verify_checksum=verify_checksum,
        )

    def _globus_format_transfer_data(
        self,
        source_endpoint: str,
        destination_endpoint: str,
        transfer_items: list[GlobusTransferItem],
        label: str = None,
        verify_checksum: bool = True,
    ) -> TransferData:
        """Format a globus TransferData instance."""
        transfer_data = self._globus_transfer_configuration(
            source_endpoint=source_endpoint,
            destination_endpoint=destination_endpoint,
            label=label,
            verify_checksum=verify_checksum,
        )
        for item in transfer_items:
            transfer_data.add_item(
                source_path=str(item.source_path),
                destination_path=str(item.destination_path),
                recursive=item.recursive,
            )
        return transfer_data

    def globus_transfer(
        self,
        source_endpoint: str,
        destination_endpoint: str,
        transfer_items: list[GlobusTransferItem],
        label: str = None,
        verify_checksum: bool = True,
    ) -> None:
        """Perform a transfer of data using globus."""
        transfer_data = self._globus_format_transfer_data(
            source_endpoint=source_endpoint,
            destination_endpoint=destination_endpoint,
            transfer_items=transfer_items,
            label=label,
            verify_checksum=verify_checksum,
        )
        self._blocking_globus_transfer(transfer_data=transfer_data)

    def _globus_transfer_configuration(
        self,
        source_endpoint: str,
        destination_endpoint: str,
        label: str = None,
        verify_checksum: bool = True,
    ) -> TransferData:
        label = label or "Data Processing Transfer"
        return TransferData(
            source_endpoint=source_endpoint,
            destination_endpoint=destination_endpoint,
            label=label,
            verify_checksum=verify_checksum,
        )

    def _blocking_globus_transfer(self, transfer_data: TransferData) -> None:
        tc = self.globus_transfer_client_factory(transfer_data=transfer_data)
        transfer_result = tc.submit_transfer(transfer_data)
        task_id = transfer_result["task_id"]
        logger.info(f"Starting globus transfer: label={transfer_data.get('label')}, {task_id=}, ")
        polling_interval = 60
        while not tc.task_wait(
            task_id=task_id, timeout=polling_interval, polling_interval=polling_interval
        ):
            events = list(tc.task_event_list(task_id=task_id, limit=1))
            if not events:
                logger.info(
                    f"Transfer task not started: recipe_run_id={self.recipe_run_id}, {task_id=}"
                )
                continue
            last_event = events[0]
            log_message = (
                f"Transfer status: {last_event=}, recipe_run_id={self.recipe_run_id}, {task_id=}"
            )
            if last_event["is_error"]:
                logger.warning(log_message)
            else:
                logger.info(log_message)
        task = tc.get_task(task_id)
        status = task["status"]
        if status != "SUCCEEDED":
            message = f"Transfer unsuccessful: {task=}, recipe_run_id={self.recipe_run_id}"
            logger.error(message)
            raise GlobusError(message)
        logger.info(
            f"Transfer Completed Successfully: recipe_run_id={self.recipe_run_id}, {task_id=}"
        )
