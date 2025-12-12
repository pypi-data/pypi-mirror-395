"""Environment controlled configurations for dkist_processing_core."""

from dkist_service_configuration import InstrumentedMeshServiceConfigurationBase
from dkist_service_configuration.settings import MeshService
from opentelemetry.sdk.resources import Resource
from pydantic import Field
from talus import ConnectionRetryerFactory
from talus import Exchange
from talus.models.connection_parameters import ConnectionParameterFactory


class DKISTProcessingCoreConfiguration(InstrumentedMeshServiceConfigurationBase):
    """Environment configurations for dkist_processing_core."""

    isb_username: str = Field(default="guest", description="Username for the interservice-bus.")
    isb_password: str = Field(default="guest", description="Password for the interservice-bus.")
    isb_exchange: str = Field(
        default="master.direct.x", description="Exchange for the interservice-bus."
    )
    isb_queue_type: str = Field(
        default="classic",
        description="Queue type for the interservice-bus.",
        examples=["quorum", "classic"],
    )
    build_version: str = Field(
        default="dev", description="Fallback build version for workflow tasks."
    )

    @property
    def isb_mesh_service(self) -> MeshService:
        """Return the mesh service details for the interservice-bus."""
        return self.service_mesh_detail(
            service_name="interservice-bus",
            default_mesh_service=MeshService(mesh_address="localhost", mesh_port=5672),
        )

    @property
    def isb_producer_connection_parameters(self) -> ConnectionParameterFactory:
        """Return the connection parameters for the ISB producer."""
        return ConnectionParameterFactory(
            rabbitmq_host=self.isb_mesh_service.host,
            rabbitmq_port=self.isb_mesh_service.port,
            rabbitmq_user=self.isb_username,
            rabbitmq_pass=self.isb_password,
            connection_name=f"{self.service_name}-producer",
        )

    @property
    def isb_connection_retryer(self) -> ConnectionRetryerFactory:
        """Return the connection retryer for the ISB connection."""
        return ConnectionRetryerFactory(
            delay_min=1,
            delay_max=5,
            backoff=1,
            jitter_min=1,
            jitter_max=3,
            attempts=3,
        )

    @property
    def isb_queue_arguments(self) -> dict:
        """Return the queue arguments for the ISB."""
        return {
            "x-queue-type": self.isb_queue_type,
        }

    @property
    def isb_publish_exchange(self) -> Exchange:
        """Return the exchange for the ISB."""
        return Exchange(name=self.isb_exchange)

    @property
    def otel_resource(self) -> Resource:
        """Open Telemetry resource attributes."""
        old = super().otel_resource
        updates = Resource(attributes={"service.name.alias": "dkist-processing"})
        new = old.merge(updates)
        return new


core_configurations = DKISTProcessingCoreConfiguration()
core_configurations.auto_instrument()
