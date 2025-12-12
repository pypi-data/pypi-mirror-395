from investigator.checks import github_checks
from investigator.policy_engine import Policy, POINTS_HIGH, PolicyGroup, TieredPolicyGroup, POINTS_MEDIUM, POINTS_LOW


def github_example_policy_group() -> PolicyGroup:
    return PolicyGroup(
        name="github_example_policy_group",
        policies=[
            Policy(
                name="github_repo_is_private",
                points=POINTS_LOW,
                qualifiers=[],
                checks=[github_checks.github_repo_is_private],
            ),
            Policy(
                name="github_repo_has_codeowners_file",
                points=POINTS_HIGH,
                qualifiers=[],
                checks=[github_checks.github_repo_has_codeowners_file],
            ),
        ],
    )


def github_example_tiered_policy_group() -> TieredPolicyGroup:
    return TieredPolicyGroup(
        name="dependency_scanning_policies",
        tiered_policies={
            1: [
                Policy(
                    name="github_repo_is_private",
                    points=POINTS_LOW,
                    qualifiers=[],
                    checks=[github_checks.github_repo_is_private],
                ),
                Policy(
                    name="github_repo_has_codeowners_file",
                    points=POINTS_HIGH,
                    qualifiers=[],
                    checks=[github_checks.github_repo_has_codeowners_file],
                ),
            ],
            2: [
                Policy(
                    name="has_no_high_dependencies",
                    points=POINTS_MEDIUM,
                    qualifiers=[],
                    checks=[github_checks.github_repo_branch_protection_enabled],
                )
            ],
            3: [
                Policy(
                    name="has_no_medium_or_low_dependencies",
                    points=POINTS_LOW,
                    qualifiers=[],
                    checks=[github_checks.github_repo_has_description],
                )
            ],
        },
    )
