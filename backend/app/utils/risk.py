from dataclasses import dataclass


@dataclass
class RiskResult:
    screening_concern_level: str
    rationale: str


def assess_risk(calibrated_prob: float, uncertainty_score: float, quality_score: int) -> RiskResult:
    quality_factor = quality_score / 100.0
    adjusted = calibrated_prob * (1 - uncertainty_score) * quality_factor
    if adjusted > 0.6:
        level = "high"
    elif adjusted > 0.35:
        level = "moderate"
    else:
        level = "low"

    rationale = (
        "Screening concern is based on calibrated murmur probability, reduced by uncertainty and recording quality. "
        f"Adjusted score={adjusted:.2f}, quality={quality_score}/100, uncertainty={uncertainty_score:.2f}."
    )
    return RiskResult(level, rationale)
