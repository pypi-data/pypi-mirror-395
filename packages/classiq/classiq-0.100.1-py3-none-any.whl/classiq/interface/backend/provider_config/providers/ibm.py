import pydantic

from classiq.interface.backend.provider_config.provider_config import ProviderConfig


class IBMConfig(ProviderConfig):
    """
    Configuration specific to IBM.

    Attributes:
        access_token (str | None): The IBM Cloud access token to be used with IBM Quantum hosted backends. Defaults to `None`.
        channel (str): Channel to use for IBM cloud backends. Defaults to `"ibm_cloud"`.
        instance_crn (str): The IBM Cloud instance CRN (Cloud Resource Name) for the IBM Quantum service.
    """

    access_token: str | None = pydantic.Field(
        default=None,
        description="IBM Cloud access token to be used"
        " with IBM Quantum hosted backends.",
    )
    channel: str = pydantic.Field(
        default="ibm_cloud", description="Channel to use for IBM cloud backends."
    )
    instance_crn: str | None = pydantic.Field(
        default=None, description="IBM Cloud instance CRN."
    )
