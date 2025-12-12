from dataclasses import dataclass, field
from typing import Dict, List

from investigator.policy_engine import EvaluatedPolicy


@dataclass
class ScoreComponent:
    """Unified component score (flat or tiered).

    tiers: optional mapping of tier number -> ScoreComponent for tiered policy groups.
    qualified: indicates whether the entity qualified for evaluation
    """

    name: str
    score: float
    max_score: float
    compliant: bool
    evaluated_policies: List[EvaluatedPolicy] = field(default_factory=list)
    tiers: Dict[int, "ScoreComponent"] = field(default_factory=dict)
    qualified: bool | None = None
