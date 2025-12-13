import pydantic


class SynthesisStepDurations(pydantic.BaseModel):
    preprocessing: float
    solving: float
    conversion_to_circuit: float
    postprocessing: float

    def total_time(self) -> float:
        return sum(
            time if time is not None else 0
            for time in (
                self.preprocessing,
                self.solving,
                self.conversion_to_circuit,
                self.postprocessing,
            )
        )

    def __repr__(self) -> str:
        return (
            f"Preprocessing: {self.preprocessing:.2f}s, "
            f"Solving: {self.solving:.2f}s, "
            f"Conversion to Circuit: {self.conversion_to_circuit:.2f}s, "
            f"Postprocessing: {self.postprocessing:.2f}s, "
            f"Total: {self.total_time():.2f}s"
        )
