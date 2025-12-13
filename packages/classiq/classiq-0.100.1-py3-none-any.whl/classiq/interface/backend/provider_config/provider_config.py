from pydantic import BaseModel


class ProviderConfig(BaseModel):
    """
    Provider-specific configuration data for execution, such as API keys and
    machine-specific parameters.
    """
