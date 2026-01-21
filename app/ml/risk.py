from __future__ import annotations

from typing import List, Tuple


def triage_rules(confidence: float, quality_pass: bool) -> Tuple[str, str]:
    if not quality_pass:
        return "Needs re-record", "Quality gate failed"
    if confidence < 0.4:
        return "Low", "Confidence < 0.40"
    if confidence < 0.7:
        return "Medium", "0.40 <= Confidence < 0.70"
    return "High", "Confidence >= 0.70"


def murmur_timing_proxy(segments: List[dict]) -> str:
    if not segments:
        return "mid"
    top = max(segments, key=lambda s: s["score"])
    midpoint = (top["start"] + top["end"]) / 2
    if midpoint < 2.0:
        return "early"
    if midpoint > 4.0:
        return "late"
    return "mid"


def urgency_score(confidence: float, triage_level: str, timing: str, quality_pass: bool) -> Tuple[float, str, List[str]]:
    score = confidence * 60
    breakdown = [f"+{confidence * 60:.1f} from confidence"]
    if triage_level == "High":
        score += 20
        breakdown.append("+20 high triage")
    elif triage_level == "Medium":
        score += 10
        breakdown.append("+10 medium triage")
    else:
        score += 0
        breakdown.append("+0 low triage")

    if timing == "late":
        score += 10
        breakdown.append("+10 late timing proxy")
    elif timing == "early":
        score += 5
        breakdown.append("+5 early timing proxy")

    if not quality_pass:
        score -= 15
        breakdown.append("-15 quality penalty")

    score = max(0.0, min(100.0, score))
    if score >= 75:
        category = "Urgent review"
    elif score >= 50:
        category = "Soon"
    else:
        category = "Monitor"
    return score, category, breakdown
