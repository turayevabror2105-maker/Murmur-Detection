import math


class TemperatureScaler:
    def __init__(self, temperature: float = 1.4):
        self.temperature = temperature

    def calibrate_probability(self, logit: float) -> float:
        scaled_logit = logit / self.temperature
        return 1.0 / (1.0 + math.exp(-scaled_logit))


CALIBRATION_EXPLANATION = (
    "Calibrated probability is adjusted so that, over many samples, 0.8 means correct about 80% of the time."
)
