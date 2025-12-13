import pydantic

from classiq.interface.backend import pydantic_backend
from classiq.interface.backend.provider_config.provider_config import ProviderConfig


class IonQConfig(ProviderConfig):
    """
    Configuration specific to IonQ.

     Attributes:
         api_key (PydanticIonQApiKeyType | None): Key to access IonQ API.
         error_mitigation (bool): A configuration option to enable or disable error mitigation during execution. Defaults to `False`.
    """

    api_key: pydantic_backend.PydanticIonQApiKeyType | None = pydantic.Field(
        default=None, description="IonQ API key."
    )
    error_mitigation: bool = pydantic.Field(
        default=False,
        description="Enable error mitigation during execution.",
    )
