import pydantic

from classiq.interface.backend.provider_config.provider_config import ProviderConfig


class AliceBobConfig(ProviderConfig):
    """
    Configuration specific to Alice&Bob.

    Attributes:
        distance (int | None):
            The number of times information is duplicated in the repetition code.
            - **Tooltip**: Phase-flip probability decreases exponentially with this parameter, bit-flip probability increases linearly.
            - **Supported Values**: 3 to 300, though practical values are usually lower than 30.
            - **Default**: None.

        kappa_1 (float | None):
            The rate at which the cat qubit loses one photon, creating a bit-flip.
            - **Tooltip**: Lower values mean lower error rates.
            - **Supported Values**: 10 to 10^5. Current hardware is at ~10^3.
            - **Default**: None.

        kappa_2 (float | None):
            The rate at which the cat qubit is stabilized using two-photon dissipation.
            - **Tooltip**: Higher values mean lower error rates.
            - **Supported Values**: 100 to 10^9. Current hardware is at ~10^5.
            - **Default**: None.

        average_nb_photons (float | None):
            The average number of photons.
            - **Tooltip**: Bit-flip probability decreases exponentially with this parameter, phase-flip probability increases linearly.
            - **Supported Values**: 4 to 10^5, though practical values are usually lower than 30.
            - **Default**: None.
    """

    distance: int | None = pydantic.Field(
        default=None, description="Repetition code distance"
    )
    kappa_1: float | None = pydantic.Field(
        default=None, description="One-photon dissipation rate (Hz)"
    )
    kappa_2: float | None = pydantic.Field(
        default=None, description="Two-photon dissipation rate (Hz)"
    )
    average_nb_photons: float | None = pydantic.Field(
        default=None, description="Average number of photons"
    )
