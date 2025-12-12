"""Common configurations."""

from dkist_processing_core.config import DKISTProcessingCoreConfiguration
from dkist_service_configuration.settings import DEFAULT_MESH_SERVICE
from dkist_service_configuration.settings import MeshService
from pydantic import BaseModel
from pydantic import Field
from talus import ConnectionRetryerFactory
from talus import ConsumerConnectionParameterFactory
from talus import ProducerConnectionParameterFactory


class GlobusClientCredential(BaseModel):
    """Globus client credential."""

    client_id: str = Field(..., description="Globus client ID for transfers.")
    client_secret: str = Field(..., description="Globus client secret for transfers.")


class DKISTProcessingCommonConfiguration(DKISTProcessingCoreConfiguration):
    """Common configurations."""

    # metadata-store-api
    gql_auth_token: str | None = Field(
        default="dev", description="The auth token for the metadata-store-api."
    )
    # object-store-api
    object_store_access_key: str | None = Field(
        default=None, description="The access key for the object store."
    )
    object_store_secret_key: str | None = Field(
        default=None, description="The secret key for the object store."
    )
    object_store_use_ssl: bool = Field(
        default=False, description="Whether to use SSL for the object store connection."
    )
    # start object-clerk library
    multipart_threshold: int | None = Field(
        default=None, description="Multipart threshold for the object store."
    )
    s3_client_config: dict | None = Field(
        default=None, description="S3 client configuration for the object store."
    )
    s3_upload_config: dict | None = Field(
        default=None, description="S3 upload configuration for the object store."
    )
    s3_download_config: dict | None = Field(
        default=None, description="S3 download configuration for the object store."
    )
    # globus
    globus_max_retries: int = Field(
        default=5, description="Max retries for transient errors on calls to the globus api."
    )
    globus_inbound_client_credentials: list[GlobusClientCredential] = Field(
        default_factory=list,
        description="Globus client credentials for inbound transfers.",
        examples=[
            [
                {"client_id": "id1", "client_secret": "secret1"},
                {"client_id": "id2", "client_secret": "secret2"},
            ],
        ],
    )
    globus_outbound_client_credentials: list[GlobusClientCredential] = Field(
        default_factory=list,
        description="Globus client credentials for outbound transfers.",
        examples=[
            [
                {"client_id": "id3", "client_secret": "secret3"},
                {"client_id": "id4", "client_secret": "secret4"},
            ],
        ],
    )
    object_store_endpoint: str | None = Field(
        default=None, description="Object store Globus Endpoint ID."
    )
    scratch_endpoint: str | None = Field(default=None, description="Scratch Globus Endpoint ID.")
    # scratch
    scratch_base_path: str = Field(default="scratch/", description="Base path for scratch storage.")
    scratch_inventory_db_count: int = Field(
        default=16, description="Number of databases in the scratch inventory (redis)."
    )
    # docs
    docs_base_url: str = Field(
        default="my_test_url", description="Base URL for the documentation site."
    )

    @property
    def metadata_store_api_base(self) -> str:
        """Metadata store api url."""
        gateway = self.service_mesh_detail(service_name="internal-api-gateway")
        return f"http://{gateway.host}:{gateway.port}/graphql"

    @property
    def object_store_api_mesh_service(self) -> MeshService:
        """Object store host and port."""
        return self.service_mesh_detail(service_name="object-store-api")

    @property
    def scratch_inventory_mesh_service(self) -> MeshService:
        """Scratch inventory host and port."""
        mesh = self.service_mesh_detail(service_name="automated-processing-scratch-inventory")
        if mesh == DEFAULT_MESH_SERVICE:
            return MeshService(mesh_address="localhost", mesh_port=6379)  # testing default
        return mesh

    @property
    def scratch_inventory_max_db_index(self) -> int:
        """Scratch inventory's largest db index."""
        return self.scratch_inventory_db_count - 1

    @property
    def isb_producer_connection_parameters(self) -> ProducerConnectionParameterFactory:
        """Return the connection parameters for the ISB producer."""
        return ProducerConnectionParameterFactory(
            rabbitmq_host=self.isb_mesh_service.host,
            rabbitmq_port=self.isb_mesh_service.port,
            rabbitmq_user=self.isb_username,
            rabbitmq_pass=self.isb_password,
            connection_name="dkist-processing-common-producer",
        )

    @property
    def isb_consumer_connection_parameters(self) -> ConsumerConnectionParameterFactory:
        """Return the connection parameters for the ISB producer."""
        return ConsumerConnectionParameterFactory(
            rabbitmq_host=self.isb_mesh_service.host,
            rabbitmq_port=self.isb_mesh_service.port,
            rabbitmq_user=self.isb_username,
            rabbitmq_pass=self.isb_password,
            connection_name="dkist-processing-common-consumer",
        )

    @property
    def isb_connection_retryer(self) -> ConnectionRetryerFactory:
        """Return the connection retryer for the ISB connection."""
        return ConnectionRetryerFactory(
            delay_min=self.retry_config.retry_delay,
            delay_max=self.retry_config.retry_max_delay,
            backoff=self.retry_config.retry_backoff,
            jitter_min=self.retry_config.retry_jitter[0],
            jitter_max=self.retry_config.retry_jitter[1],
            attempts=self.retry_config.retry_tries,
        )


common_configurations = DKISTProcessingCommonConfiguration()
