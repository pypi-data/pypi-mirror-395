import pydantic

from classiq.interface.backend.provider_config.provider_config import ProviderConfig


class AQTConfig(ProviderConfig):
    """
    Configuration specific to AQT (Alpine Quantum Technologies).

    Attributes:
        api_key: The API key required to access AQT's quantum computing services.
        workspace: The AQT workspace where the simulator/hardware is located.
    """

    api_key: str | None = pydantic.Field(default=None, description="AQT API key")
    workspace: str = pydantic.Field(description="AQT workspace")
