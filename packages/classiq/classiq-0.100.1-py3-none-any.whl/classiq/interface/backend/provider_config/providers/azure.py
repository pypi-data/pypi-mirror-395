import pydantic

from classiq.interface.backend import pydantic_backend
from classiq.interface.backend.provider_config.provider_config import ProviderConfig


class AzureConfig(ProviderConfig):
    """
    Configuration specific to Azure.

    Attributes:
        location (str): Azure region. Defaults to `"East US"`.
        tenant_id (str | None): Azure Tenant ID used to identify the directory in which the application is registered.
        client_id (str | None): Azure Client ID, also known as the application ID, which is used to authenticate the application.
        client_secret (str | None): Azure Client Secret associated with the application, used for authentication.
        resource_id (str | None): Azure Resource ID, including the subscription ID, resource group, and workspace, typically used for personal resources.
        ionq_error_mitigation (bool): Should use error mitigation when running on IonQ through Azure. Defaults to `False`.
    """

    location: str = pydantic.Field(
        default="East US", description="Azure personal resource region"
    )

    tenant_id: str | None = pydantic.Field(default=None, description="Azure Tenant ID")
    client_id: str | None = pydantic.Field(default=None, description="Azure Client ID")
    client_secret: str | None = pydantic.Field(
        default=None, description="Azure Client Secret"
    )
    resource_id: pydantic_backend.PydanticAzureResourceIDType | None = pydantic.Field(
        default=None,
        description="Azure Resource ID (including Azure subscription ID, resource "
        "group and workspace), for personal resource",
    )
    ionq_error_mitigation: bool = pydantic.Field(
        default=False,
        description="Error mitigation configuration upon running on IonQ through Azure.",
    )
