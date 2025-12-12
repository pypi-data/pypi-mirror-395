import logging
from datetime import datetime, timedelta, timezone

from investigator.github_client import Repository, RepositoryVisibility

log = logging.getLogger(__name__)


def github_repo_vulnerability_alerts_no_critical_findings(repo: Repository) -> bool:
    """
    Checks if there are no critical dependabot security alerts in the GitHub repository.

    :param repo: Repository object
    :return: bool
    """
    return len([alert for alert in repo.vulnerability_alerts if alert.severity.upper() == "CRITICAL"]) == 0


def github_repo_vulnerability_alerts_no_high_findings(repo: Repository) -> bool:
    """
    Checks if there are no high dependabot security alerts in the GitHub repository.

    :param repo: Repository object
    :return: bool
    """
    return len([alert for alert in repo.vulnerability_alerts if alert.severity.upper() == "HIGH"]) == 0


def github_repo_vulnerability_alerts_no_medium_low_findings(repo: Repository) -> bool:
    """
    Checks if there are no medium or low dependabot security alerts in the GitHub repository.

    :param repo: Repository object
    :return: bool
    """
    medium_count = len([alert for alert in repo.vulnerability_alerts if alert.severity.upper() == "MEDIUM"])
    low_count = len([alert for alert in repo.vulnerability_alerts if alert.severity.upper() == "LOW"])
    return medium_count == 0 and low_count == 0


def github_repo_branch_protection_enabled(repo: Repository):
    """
    Checks that branch protection of default branch is enabled for a GitHub repository.

    :param repo: Repository object
    :return: bool
    """
    return repo.default_branch_protection_rules is not None


def github_repo_branch_protection_require_codeowner_review(repo: Repository):
    """
    Checks that default branch protection rule 'require code owners review' is enabled.

    :param repo: Repository object
    :return: bool
    """
    if repo.default_branch_protection_rules is None:
        return False
    return repo.default_branch_protection_rules.requires_code_owner_reviews


def github_repo_branch_protection_required_approving_review_count_1(repo: Repository):
    if repo.default_branch_protection_rules is None:
        return False
    try:
        return repo.default_branch_protection_rules.required_approving_review_count >= 1
    except TypeError:
        log.error(f"Repo '{repo.name}', required_approving_review_count not integer, returning False")
        return False


def github_repo_branch_protection_required_approving_review_count_2(repo: Repository):
    if repo.default_branch_protection_rules is None:
        return False
    try:
        return repo.default_branch_protection_rules.required_approving_review_count >= 2
    except TypeError:
        log.error(f"Repo '{repo.name}', required_approving_review_count not integer, returning False")
        return False


def github_repo_branch_protection_include_admins(repo: Repository):
    if repo.default_branch_protection_rules is None:
        return False
    return repo.default_branch_protection_rules.is_admin_enforced


def github_repo_branch_protection_require_signed_commits(repo: Repository):
    if repo.default_branch_protection_rules is None:
        return False
    return repo.default_branch_protection_rules.requires_commit_signatures


def github_repo_is_private(repo: Repository) -> bool:
    """
    Checks if the repository is private.

    :param repo: Repository object
    :return: bool
    """
    return repo.is_private


def github_repo_has_description(repo: Repository) -> bool:
    """
    Checks if the repository has a description.

    :param repo: Repository object
    :return: bool
    """
    return repo.description is not None and len(repo.description.strip()) > 0


def github_repo_has_license_visibility_public(repo: Repository) -> bool:
    """
    Checks if the repository has a license (only applicable for public repos).

    :param repo: Repository object
    :return: bool
    """
    # Only check license for public repositories
    if repo.visibility != RepositoryVisibility.PUBLIC:
        return True
    return repo.license_name is not None


def github_repo_recently_updated(repo: Repository, days: int = 90) -> bool:
    """
    Checks if the repository was updated within the specified number of days.

    :param repo: Repository object
    :param days: Number of days threshold (default: 90)
    :return: bool
    """
    if repo.updated_at is None:
        return False
    threshold = datetime.now(timezone.utc) - timedelta(days=days)
    return repo.updated_at >= threshold


def github_repo_has_recent_commits(repo: Repository, days: int = 90) -> bool:
    """
    Checks if the repository has commits within the specified number of days.

    :param repo: Repository object
    :param days: Number of days threshold (default: 90)
    :return: bool
    """
    if repo.pushed_at is None:
        return False
    threshold = datetime.now(timezone.utc) - timedelta(days=days)
    return repo.pushed_at >= threshold


def github_repo_has_codeowners_file(repo: Repository) -> bool:
    """
    Checks if the repository has a valid CODEOWNERS file (no errors).

    :param repo: Repository object
    :return: bool
    """
    # has_no_codeowners_errors will be True if no errors, False if errors, None if not checked
    if repo.has_no_codeowners_errors is None:
        return True  # If not checked, assume it's okay
    return repo.has_no_codeowners_errors


def github_repo_branch_protection_disallow_force_pushes(repo: Repository) -> bool:
    """
    Checks that force pushes are disallowed on the default branch.

    :param repo: Repository object
    :return: bool
    """
    if repo.default_branch_protection_rules is None:
        return False
    return not repo.default_branch_protection_rules.allows_force_pushes


def github_repo_branch_protection_disallow_deletions(repo: Repository) -> bool:
    """
    Checks that branch deletions are disallowed on the default branch.

    :param repo: Repository object
    :return: bool
    """
    if repo.default_branch_protection_rules is None:
        return False
    return not repo.default_branch_protection_rules.allows_deletions


def github_repo_branch_protection_require_conversation_resolution(repo: Repository) -> bool:
    """
    Checks that conversation resolution is required before merging.

    :param repo: Repository object
    :return: bool
    """
    if repo.default_branch_protection_rules is None:
        return False
    return repo.default_branch_protection_rules.requires_conversation_resolution


def github_repo_vulnerability_alerts_not_dismissed_without_reason(repo: Repository) -> bool:
    """
    Checks that all dismissed vulnerability alerts have a dismiss reason.

    :param repo: Repository object
    :return: bool
    """
    dismissed_alerts = [alert for alert in repo.vulnerability_alerts if alert.state != "OPEN"]
    alerts_without_reason = [alert for alert in dismissed_alerts if not alert.dismiss_reason]
    return len(alerts_without_reason) == 0


def github_repo_vulnerability_alerts_timely_fixed(
    repo: Repository, critical_days: int = 7, high_days: int = 30
) -> bool:
    """
    Checks that critical and high severity vulnerability alerts are not older than specified thresholds.

    :param repo: Repository object
    :param critical_days: Maximum age for critical alerts (default: 7)
    :param high_days: Maximum age for high alerts (default: 30)
    :return: bool
    """
    now = datetime.now(timezone.utc)
    critical_threshold = now - timedelta(days=critical_days)
    high_threshold = now - timedelta(days=high_days)

    # Check critical alerts
    old_critical_alerts = [
        alert
        for alert in repo.vulnerability_alerts
        if alert.state == "OPEN" and alert.severity.upper() == "CRITICAL" and alert.created_at < critical_threshold
    ]

    # Check high alerts
    old_high_alerts = [
        alert
        for alert in repo.vulnerability_alerts
        if alert.state == "OPEN" and alert.severity.upper() == "HIGH" and alert.created_at < high_threshold
    ]

    return len(old_critical_alerts) == 0 and len(old_high_alerts) == 0
