import logging
from collections.abc import Callable

from investigator.base_models import ScoreComponent
from investigator.policy_engine import PolicyGroup, TieredPolicyGroup, TieredPolicyGroupResult, PolicyGroupResult
from investigator.github_client import Repository
from investigator.policies import github_example_policy_group, github_example_tiered_policy_group

log = logging.getLogger(__name__)


def score_policy_group_results(pg: PolicyGroupResult, weight_coefficient: float = 1) -> ScoreComponent:
    """Converts policy evaluation points to a score.

    Example: If a policy group has 80 out of 100 points, and a weight coefficient of 0.5, the score would be 40.

    The score range is 0-100
    Non-qualified policy group results automatically receive the maximum score.
    If you have multiple policy groups with different weights that you want to combine, you can use the weight_coefficient parameter.
    """
    max_score = round(100 * weight_coefficient)

    if not pg.qualified:
        return ScoreComponent(
            name=pg.name,
            score=max_score,
            max_score=max_score,
            compliant=True,
            qualified=False,
        )

    score = round((pg.points_sum / pg.points_max) * max_score) if pg.points_max > 0 else 0

    return ScoreComponent(
        name=pg.name,
        score=score,
        max_score=max_score,
        compliant=pg.points_sum == pg.points_max,
        evaluated_policies=pg.evaluated_policies,
        qualified=pg.qualified,
    )


def score_tiered_policy_group_results(
    tpg_result: TieredPolicyGroupResult, weight_coefficient: float = 1
) -> ScoreComponent:
    """Converts tiered policy evaluation points to a score.

    Example: If a tiered policy group has 150 out of 200 points, and a weight coefficient of 0.5, the score would be 37.5.

    The score range is 0-100
    If you have multiple policy groups with different weights that you want to combine, you can use the weight_coefficient parameter.
    """

    max_score = round(100 * weight_coefficient)

    if not tpg_result.qualified:
        return ScoreComponent(
            name=tpg_result.name,
            score=max_score,
            max_score=max_score,
            compliant=True,
            qualified=False,
        )

    tier_components: dict[int, ScoreComponent] = {}
    total_qualifying_points = sum(tier_result.points_max for tier_result in tpg_result.tier_results.values())

    total_score = 0
    for tier_num in sorted(tpg_result.tier_results.keys()):
        tier_result = tpg_result.tier_results[tier_num]

        if tier_num != tier_result.tier:
            raise ValueError(f"Tier number mismatch: expected {tier_num}, got {tier_result.tier}")

        tier_weight_coefficient = (
            (weight_coefficient * 100) / total_qualifying_points if total_qualifying_points > 0 else 0
        )

        tier_weighted_score = tier_result.points_sum * tier_weight_coefficient
        total_score += tier_weighted_score

        tier_components[tier_result.tier] = ScoreComponent(
            name=str(tier_result.tier),
            score=tier_weighted_score,
            max_score=tier_result.points_max * tier_weight_coefficient,
            compliant=tier_result.points_sum == tier_result.points_max,
            qualified=True,
            evaluated_policies=tier_result.evaluated_policies,
        )

    return ScoreComponent(
        name=tpg_result.name,
        score=round(total_score),
        max_score=max_score,
        compliant=tpg_result.qualified and tpg_result.points_sum == tpg_result.points_max,
        evaluated_policies=[],  # Tiered groups store details at tier level
        tiers=tier_components,
        qualified=tpg_result.qualified,
    )


def _evaluate_flat(group_factory: Callable[[], PolicyGroup], repo: Repository, weight: float) -> ScoreComponent:
    pg: PolicyGroupResult = group_factory().evaluate(repo)
    return score_policy_group_results(pg, weight)


def _evaluate_tiered(group_factory: Callable[[], TieredPolicyGroup], repo: Repository, weight: float) -> ScoreComponent:
    pg: TieredPolicyGroupResult = group_factory().evaluate(repo)
    return score_tiered_policy_group_results(pg, weight)


def example_repository_scoring(repo: Repository) -> dict[str, ScoreComponent]:
    """Return score components from evaluating example policy groups."""
    return {
        "flat_score": _evaluate_flat(github_example_policy_group, repo, 0.23),
        "tiered_score": _evaluate_tiered(github_example_tiered_policy_group, repo, 0.77),
    }
