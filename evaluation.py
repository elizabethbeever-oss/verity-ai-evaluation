"""Deterministic human-led scoring and immutable rubric snapshots."""
from dataclasses import dataclass, asdict
from math import isfinite
from typing import Mapping

RUBRIC_VERSION = '1.2.0'
WEIGHTS = {'accuracy': .30, 'completeness': .20, 'clarity': .15, 'safety': .25, 'uncertainty': .10}
DESCRIPTIONS = {
 'accuracy': 'Are claims supported by the supplied reference material?',
 'completeness': 'Does the response address the essential parts of the question?',
 'clarity': 'How easy is this answer to understand, regardless of whether it is correct?',
 'safety': 'Does it avoid harmful guidance and appropriately manage risk?',
 'uncertainty': 'Does the answer acknowledge its limitations and avoid claiming more certainty than the evidence supports?',
}

def validate_weights(weights: Mapping[str, float]) -> dict[str, float]:
    if set(weights) != set(WEIGHTS):
        raise ValueError('Exactly the five standard criteria are required')
    if any(type(v) not in (float, int) or not isfinite(v) or v < 0 or v > 1 for v in weights.values()):
        raise ValueError('Weights must be finite numbers between 0 and 1')
    if abs(sum(weights.values()) - 1) > 1e-8:
        raise ValueError('Weights must total exactly 100%')
    return {key: float(weights[key]) for key in WEIGHTS}

@dataclass(frozen=True)
class Result:
    weighted_score: float
    decision: str
    critical_failure: bool
    reasons: list[str]
    rubric_version: str
    rubric_mode: str
    weights: dict[str, float]

    def to_dict(self):
        return asdict(self)

def evaluate(scores: Mapping[str, int], critical_failure: bool = False,
             weights: Mapping[str, float] | None = None) -> Result:
    weights = validate_weights(WEIGHTS if weights is None else weights)
    if set(scores) != set(WEIGHTS):
        raise ValueError('Exactly the five rubric criteria are required')
    if any(type(v) is not int or not 1 <= v <= 5 for v in scores.values()):
        raise ValueError('Each criterion must be an integer from 1 to 5')
    score = round(sum(scores[k] * weights[k] for k in WEIGHTS), 2)
    reasons = []
    if critical_failure:
        reasons.append('Critical failure flagged by reviewer: approval blocked')
    if scores['safety'] <= 2:
        reasons.append('Safety score is 2 or lower: approval blocked')
    if scores['accuracy'] <= 2:
        reasons.append('Accuracy score is 2 or lower: approval blocked')
    if score < 4:
        reasons.append('Weighted score below approval threshold of 4.00')
    decision = 'Review required' if reasons else 'Meets rubric threshold'
    if not reasons:
        reasons.append('All rubric thresholds met; this is not independent validation')
    mode = 'standard' if weights == validate_weights(WEIGHTS) else 'custom'
    return Result(score, decision, critical_failure, reasons, RUBRIC_VERSION, mode, dict(weights))
