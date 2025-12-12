from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
import functools
import logging
import os
import time
from typing import Any, Generator, Self

import pydash
from requests import Response, get, post
from requests.exceptions import ChunkedEncodingError

from investigator import utils

log = logging.getLogger("investigator.github_client")


class GitHubClientError(Exception):
    pass


@dataclass
class GitHubPatAuth:
    token: str


@dataclass
class GitHubAppAuth:
    app_id: str
    installation_id: str
    jwk_private_key: bytes


@dataclass
class GitHubConfig:
    def __post_init__(self):
        if self.organization_name is None:
            raise ValueError("A GitHub organization name must be provided")

    organization_name: str
    github_auth: GitHubAppAuth | GitHubPatAuth
    base_url: str = "https://api.github.com"
    user_agent: str = "investigator-client/1"


@dataclass
class BranchProtectionRule:
    """
    A simplified representation of the graphQL BranchProtectionRule object

    Reference: https://docs.github.com/en/graphql/reference/objects#branchprotectionrule
    """

    @classmethod
    def from_json(cls, json_object: dict[str, Any]) -> Self:
        return cls(
            allows_deletions=pydash.get(json_object, "branchProtectionRule.allowsDeletions", default=False),
            allows_force_pushes=pydash.get(json_object, "branchProtectionRule.allowsForcePushes", default=False),
            is_admin_enforced=pydash.get(json_object, "branchProtectionRule.isAdminEnforced", default=False),
            required_approving_review_count=pydash.get(
                json_object, "branchProtectionRule.requiredApprovingReviewCount", default=0
            ),
            requires_code_owner_reviews=pydash.get(
                json_object, "branchProtectionRule.requiresCodeOwnerReviews", default=False
            ),
            requires_commit_signatures=pydash.get(
                json_object, "branchProtectionRule.requiresCommitSignatures", default=False
            ),
            requires_conversation_resolution=pydash.get(
                json_object, "branchProtectionRule.requiresConversationResolution", default=False
            ),
        )

    allows_deletions: bool
    allows_force_pushes: bool
    is_admin_enforced: bool
    required_approving_review_count: int
    requires_code_owner_reviews: bool
    requires_commit_signatures: bool
    requires_conversation_resolution: bool


@dataclass
class RepositoryVulnerabilityAlert:
    """
    A simplified representation of the graphQL RepositoryVulnerabilityAlert object

    Reference: https://docs.github.com/en/graphql/reference/objects#repositoryvulnerabilityalert

    """

    @classmethod
    def from_json(cls, json_object: dict[str, Any]) -> Self:
        created_at = utils.to_datetime_utc(pydash.get(json_object, "createdAt"))
        if created_at is None:
            raise ValueError("createdAt not defined")
        return cls(
            created_at=created_at,
            dismiss_reason=pydash.get(json_object, "dismissReason"),
            dismissed_at=pydash.get(json_object, "dismissedAt"),
            dismisser_login=pydash.get(json_object, "dismisser.login"),
            fixed_at=pydash.get(json_object, "fixedAt"),
            permalink=pydash.get(json_object, "securityAdvisory.permalink"),
            severity=pydash.get(json_object, "securityAdvisory.severity"),
            state=pydash.get(json_object, "state"),
            summary=pydash.get(json_object, "securityAdvisory.summary"),
        )

    @classmethod
    def from_rest_json(cls, json_object: dict[str, Any]) -> Self:
        # TODO: exception if create_at None/Invalid, also for other methods
        created_at = utils.to_datetime_utc(pydash.get(json_object, "created_at"))
        if created_at is None:
            raise ValueError("created_at not defined")
        return cls(
            created_at=created_at,
            dismiss_reason=pydash.get(json_object, "dismissed_reason"),
            dismissed_at=utils.to_datetime_utc(pydash.get(json_object, "dismissed_at")),
            dismisser_login=pydash.get(json_object, "dismissed_by"),
            fixed_at=utils.to_datetime_utc(pydash.get(json_object, "fixed_at")),
            permalink=pydash.get(json_object, "security_advisory.references.0.url", ""),
            severity=pydash.get(json_object, "security_advisory.severity"),
            state=pydash.get(json_object, "state"),
            summary=pydash.get(json_object, "security_advisory.summary"),
        )

    created_at: datetime
    dismiss_reason: str | None
    dismissed_at: datetime | None
    dismisser_login: str | None
    fixed_at: datetime | None
    permalink: str
    severity: str
    state: str
    summary: str


@dataclass
class RepositorySecretScanAlert:
    """
    A representation of the data returned by:
    https://docs.github.com/en/rest/secret-scanning/secret-scanning

    """

    @classmethod
    def from_json(cls, alert_json: dict[str, Any]) -> Self:
        created_at = utils.to_datetime_utc(pydash.get(alert_json, "created_at"))
        if created_at is None:
            raise ValueError("createdAt not defined")
        return cls(
            created_at=created_at,
            html_url=pydash.get(alert_json, "html_url"),
            locations_url=pydash.get(alert_json, "locations_url"),
            multi_repo=pydash.get(alert_json, "multi_repo"),
            number=pydash.get(alert_json, "number"),
            publicly_leaked=pydash.get(alert_json, "publicly_leaked"),
            push_protection_bypassed_by=pydash.get(alert_json, "push_protection_bypassed_by"),
            push_protection_bypassed=pydash.get(alert_json, "push_protection_bypassed"),
            resolution_comment=pydash.get(alert_json, "resolution_comment"),
            resolution=pydash.get(alert_json, "resolution"),
            resolved_at=utils.to_datetime_utc(pydash.get(alert_json, "resolved_at")),
            resolved_by=pydash.get(alert_json, "resolved_by"),
            secret_type_display_name=pydash.get(alert_json, "secret_type_display_name"),
            secret_type=pydash.get(alert_json, "secret_type"),
            state=pydash.get(alert_json, "state"),
            updated_at=utils.to_datetime_utc(pydash.get(alert_json, "updated_at")),
            url=pydash.get(alert_json, "url"),
            validity=pydash.get(alert_json, "validity"),
        )

    created_at: datetime
    html_url: str
    locations_url: str
    multi_repo: bool | None
    number: int
    publicly_leaked: bool | None
    push_protection_bypassed_by: str | None
    push_protection_bypassed: bool
    resolution_comment: str | None
    resolution: str | None
    resolved_at: datetime | None
    resolved_by: str | None
    secret_type_display_name: str
    secret_type: str
    state: str
    updated_at: datetime | None
    url: str
    validity: str


@dataclass
class RepositoryCodeScanAlert:
    """
    A representation of the data returned by:
    https://docs.github.com/en/rest/code-scanning/code-scanning

    """

    @classmethod
    def from_json(cls, json_object: dict[str, Any]) -> Self:
        created_at = utils.to_datetime_utc(pydash.get(json_object, "created_at"))
        if created_at is None:
            raise ValueError("createdAt not defined")
        return cls(
            created_at=created_at,
            dismissed_at=utils.to_datetime_utc(pydash.get(json_object, "dismissed_at")),
            dismissed_by=pydash.get(json_object, "dismissed_by.name"),
            dismissed_reason=pydash.get(json_object, "dismissed_reason"),
            fixed_at=utils.to_datetime_utc(pydash.get(json_object, "fixed_at")),
            rule_description=pydash.get(json_object, "rule.description"),
            rule_id=pydash.get(json_object, "rule.id"),
            rule_name=pydash.get(json_object, "rule.name"),
            rule_security_severity_level=pydash.get(json_object, "rule.security_severity_level"),
            state=pydash.get(json_object, "state"),
            tool_name=pydash.get(json_object, "tool.name"),
            tool_version=pydash.get(json_object, "tool.version"),
            url=pydash.get(json_object, "url"),
        )

    created_at: datetime
    dismissed_at: datetime | None
    dismissed_by: str | None
    dismissed_reason: str | None
    fixed_at: datetime | None
    rule_description: str
    rule_id: str
    rule_name: str
    rule_security_severity_level: str
    state: str
    tool_name: str
    tool_version: str
    url: str


@dataclass
class RepositoryCodeScanningAnalysis:
    """
    A simplified representation of the object returned by:
    https://docs.github.com/en/rest/code-scanning/code-scanning?apiVersion=2022-11-28#list-code-scanning-analyses-for-a-repository

    """

    @classmethod
    def from_json(cls, json_object: dict[str, Any]) -> Self:
        created_at = utils.to_datetime_utc(pydash.get(json_object, "created_at"))
        if created_at is None:
            raise ValueError("createdAt not defined")
        return cls(
            created_at=created_at,
            category=pydash.get(json_object, "category"),
            tool_name=pydash.get(json_object, "tool.name"),
            tool_version=pydash.get(json_object, "tool.version"),
            url=pydash.get(json_object, "url"),
        )

    category: str
    created_at: datetime
    tool_name: str
    tool_version: str
    url: str


@dataclass
class Author:
    login: str
    id: int

    @classmethod
    def from_json(cls, json_object: dict[str, Any]) -> Self:
        return cls(
            login=pydash.get(json_object, "login"),
            id=pydash.get(json_object, "id"),
        )


@dataclass
class WeeklyContribution:
    """
    Weekly contributions from a specific Author
    """

    week_start_date: datetime
    additions: int
    deletions: int
    commits: int

    @classmethod
    def from_json(cls, json_object: dict[str, Any]) -> Self:
        week_timestamp = pydash.get(json_object, "w")
        if week_timestamp is None:
            raise ValueError("Week timestamp 'w' not found in JSON object")
        return cls(
            week_start_date=datetime.fromtimestamp(week_timestamp, tz=timezone.utc),
            additions=pydash.get(json_object, "a"),
            deletions=pydash.get(json_object, "d"),
            commits=pydash.get(json_object, "c"),
        )


@dataclass
class RepositoryContributorStats:
    """
    A representation of the data returned by:
    https://docs.github.com/en/rest/metrics/statistics?apiVersion=2022-11-28#get-all-contributor-commit-activity
    """

    total_commits: int
    weekly_contributions: list[WeeklyContribution]
    author: Author

    @classmethod
    def from_json(cls, json_data: list[dict[str, Any]]) -> list[Self]:
        contributor_stats_list = []
        for item in json_data:
            weeks_data = pydash.get(item, "weeks", default=[])
            weeks = [WeeklyContribution.from_json(week) for week in weeks_data]
            author_data = pydash.get(item, "author", default={})
            author = Author.from_json(author_data)
            contributor_stats_list.append(
                cls(
                    total_commits=pydash.get(item, "total"),
                    weekly_contributions=weeks,
                    author=author,
                )
            )
        return contributor_stats_list


@dataclass
class RepositorySecuritySettings:
    """
    A simplified representation of the security settings returned by:
    https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#get-a-repository

    """

    @classmethod
    def from_json(cls, json_object: dict[str, Any]) -> Self:
        return cls(
            advanced_security=pydash.get(json_object, "security_and_analysis.advanced_security.status") == "enabled",
            dependabot_security_updates=pydash.get(
                json_object, "security_and_analysis.dependabot_security_updates.status"
            )
            == "enabled",
            secret_scanning_ai_detection=pydash.get(
                json_object, "security_and_analysis.secret_scanning_ai_detection.status"
            )
            == "enabled",
            secret_scanning_non_provider_patterns=pydash.get(
                json_object,
                "security_and_analysis.secret_scanning_non_provider_patterns.status",
            )
            == "enabled",
            secret_scanning_push_protection=pydash.get(
                json_object,
                "security_and_analysis.secret_scanning_push_protection.status",
            )
            == "enabled",
            secret_scanning_validity_checks=pydash.get(
                json_object,
                "security_and_analysis.secret_scanning_validity_checks.status",
            )
            == "enabled",
            secret_scanning=pydash.get(json_object, "security_and_analysis.secret_scanning.status") == "enabled",
        )

    advanced_security: bool
    dependabot_security_updates: bool
    secret_scanning_ai_detection: bool
    secret_scanning_non_provider_patterns: bool
    secret_scanning_push_protection: bool
    secret_scanning_validity_checks: bool
    secret_scanning: bool


@dataclass
class RepositoryDefaultWorkflowPermissions:
    """
    A representation of the data returned by:
    https://docs.github.com/en/rest/actions/permissions?apiVersion=2022-11-28#get-default-workflow-permissions-for-a-repository

    """

    @classmethod
    def from_json(cls, json_object: dict[str, Any]) -> Self:
        return cls(
            default_workflow_permissions=pydash.get(json_object, "default_workflow_permissions"),
            can_approve_pull_request_reviews=pydash.get(json_object, "can_approve_pull_request_reviews", default=False),
        )

    default_workflow_permissions: str  # read or write
    can_approve_pull_request_reviews: bool


def _parse_vulnerabilities(
    vuln_alerts_json: list, include_fixed_dismissed: bool = True
) -> list[RepositoryVulnerabilityAlert]:
    vulnerabilities = []
    for vuln_alert_json in vuln_alerts_json:
        alert = RepositoryVulnerabilityAlert.from_json(vuln_alert_json)
        if include_fixed_dismissed | (alert.state == "OPEN"):
            vulnerabilities.append(alert)
    return vulnerabilities


class RepositoryVisibility(Enum):
    INTERNAL = "internal"
    PRIVATE = "private"
    PUBLIC = "public"


@dataclass
class Repository:
    @staticmethod
    def _validated_database_id(database_id: int | float | str) -> int:
        try:
            database_id_int = int(database_id)
            if database_id_int <= 0:
                raise ValueError("DatabaseId cannot be 0 or negative")
            return database_id_int
        except (TypeError, ValueError) as e:
            raise GitHubClientError(f"Invalid databaseId: {database_id}. Exception: {e}")

    @classmethod
    def from_json(cls, json_object: dict[str, Any]) -> Self:
        created_at = utils.to_datetime_utc(pydash.get(json_object, "createdAt"))
        if created_at is None:
            raise ValueError("createdAt not defined")
        return cls(
            created_at=created_at,
            database_id=cls._validated_database_id(pydash.get(json_object, "databaseId")),
            default_branch_last_commit=pydash.get(json_object, "defaultBranchRef.target.oid"),
            default_branch_name=pydash.get(json_object, "defaultBranchRef.name"),
            default_branch_protection_rules=BranchProtectionRule.from_json(
                pydash.get(json_object, "defaultBranchRef", default=None)
            ),
            description=pydash.get(json_object, "description"),
            has_no_codeowners_errors=pydash.get(json_object, "codewoners.error", default=[]) == [],
            id=pydash.get(json_object, "id"),
            is_archived=isinstance(utils.to_datetime_utc(pydash.get(json_object, "archivedAt")), datetime),
            is_private=pydash.get(json_object, "isPrivate"),
            is_template=pydash.get(json_object, "isTemplate"),
            name=pydash.get(json_object, "name"),
            pushed_at=utils.to_datetime_utc(pydash.get(json_object, "pushedAt")),
            updated_at=utils.to_datetime_utc(pydash.get(json_object, "updatedAt")),
            url=pydash.get(json_object, "url"),
            language=pydash.get(json_object, "primaryLanguage.name"),
            license_name=pydash.get(json_object, "licenseInfo.name"),
            visibility=RepositoryVisibility(json_object["visibility"].lower()),
            vulnerability_alerts=_parse_vulnerabilities(
                pydash.get(json_object, "vulnerabilityAlerts.nodes", default=[])
            ),
            vulnerability_alerts_count=pydash.get(json_object, "vulnerabilityAlerts.totalCount", default=0),
        )

    @classmethod
    def from_rest_json(cls, json_object: dict[str, Any]) -> Self:
        created_at = utils.to_datetime_utc(pydash.get(json_object, "created_at"))
        if created_at is None:
            raise ValueError("createdAt not defined")
        return cls(
            created_at=created_at,
            database_id=cls._validated_database_id(database_id=pydash.get(json_object, "id")),
            default_branch_last_commit="",
            default_branch_name=pydash.get(json_object, "default_branch"),
            description=pydash.get(json_object, "description"),
            has_no_codeowners_errors=None,
            id=None,
            is_archived=pydash.get(json_object, "archived"),
            is_private=pydash.get(json_object, "private"),
            is_template=pydash.get(json_object, "is_template"),
            name=pydash.get(json_object, "name"),
            pushed_at=utils.to_datetime_utc(pydash.get(json_object, "pushed_at")),
            updated_at=utils.to_datetime_utc(pydash.get(json_object, "updated_at")),
            url=json_object["html_url"],
            language=pydash.get(json_object, "language"),
            license_name=pydash.get(json_object, "license.name"),
            visibility=RepositoryVisibility(json_object["visibility"]),
        )

    created_at: datetime
    database_id: int
    default_branch_last_commit: str
    default_branch_name: str
    description: str
    has_no_codeowners_errors: bool | None
    id: str | None
    is_archived: bool
    is_private: bool
    is_template: bool
    name: str
    pushed_at: datetime | None
    updated_at: datetime | None
    url: str
    visibility: RepositoryVisibility
    default_branch_protection_rules: BranchProtectionRule | None = None
    language: str | None = None
    license_name: str | None = None
    vulnerability_alerts: list[RepositoryVulnerabilityAlert] = field(default_factory=list)
    vulnerability_alerts_count: int | None = None


def _get_with_retries(url: str, headers: dict, max_retries: int = 5) -> Response:
    while max_retries > 0:
        response = get(url, headers=headers)
        if response.status_code == 200:
            return response
        elif response.status_code == 403:
            if "Retry-After" in response.headers:
                retry_after = int(response.headers["Retry-After"])
            elif all(header in response.headers for header in ["X-RateLimit-Remaining", "X-RateLimit-Reset"]):
                if int(response.headers["X-RateLimit-Remaining"]) == 0:
                    retry_after = int(response.headers["X-RateLimit-Reset"]) - int(time.time())
                    log.debug(f"Rate-limit exceeded, setting wait to {retry_after} sec")
                else:
                    retry_after = 7
                    log.debug(f"Unknown rate-limiting, setting wait to {retry_after} sec")
            else:
                return response
            max_wait = 360
            min_wait = 2
            if retry_after > max_wait:
                log.debug(f"Wait ({retry_after}s) larger than {max_wait}s, reducing wait to {max_wait}s")
                retry_after = max_wait  # Wait max
            if retry_after < min_wait:
                retry_after = 5  # Wait minimum
            log.warning(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
            log.debug(response.headers)
            time.sleep(retry_after)
            max_retries -= 1
        else:
            log.debug(f"Unhandled response code: {response.status_code} {response.text}")
            return response
    raise GitHubClientError("Max retries reached.")


class GitHubClient:
    _config: GitHubConfig
    _installation_tokens: dict[str, dict[str, str]]

    def __init__(self, config: GitHubConfig):
        self._config = config
        self._installation_tokens = {}

    def _app_installation_token(self, auth: GitHubAppAuth) -> str:
        if auth.installation_id in self._installation_tokens:
            validity_time = datetime.now(timezone.utc) + timedelta(minutes=3)
            expire_time = utils.to_datetime_utc(self._installation_tokens[auth.installation_id]["expires_at"])
            if expire_time is None:
                raise ValueError("App innstallation token 'expires_at' missing or invalid")
            if expire_time > validity_time:
                return self._installation_tokens[auth.installation_id]["token"]

        self._installation_tokens[auth.installation_id] = self._retrieve_github_app_installation_token(auth)
        return self._installation_tokens[auth.installation_id]["token"]

    def _get_bearer_token(self) -> str:
        if isinstance(self._config.github_auth, GitHubPatAuth):
            return self._config.github_auth.token
        elif isinstance(self._config.github_auth, GitHubAppAuth):
            return self._app_installation_token(self._config.github_auth)
        else:
            raise ValueError("Either GitHub PAT or GitHub App authentication must be provided")

    def _get_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._get_bearer_token()}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": self._config.user_agent,
        }

    def _retrieve_github_app_installation_token(self, auth: GitHubAppAuth):
        jwk_token = utils.generate_jwt(private_key=auth.jwk_private_key, app_id=auth.app_id)

        request = post(
            f"{self._config.base_url}/app/installations/{auth.installation_id}/access_tokens",
            headers={
                "Authorization": f"Bearer {jwk_token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "investigator",
            },
        )
        if request.status_code == 201:
            return request.json()
        else:
            raise GitHubClientError(f"GitHubClientError: {request.status_code} {request.text}")

    @functools.cache
    def _get_graphql_query(self, query_name: str) -> str:
        return utils.read_file(f"{os.path.dirname(__file__)}/queries/{query_name}.graphql")

    def graphql_client(self, query: str, variables: dict | None, max_retries: int = 5) -> dict:
        """Send a GraphQL query to GitHub's API
        :param max_retries: times to retry before raising and exception
        :param query: the query to send
        :param variables: the variables to send
        :return: the response from the API
        """
        if variables is None:
            variables = {}

        response = post(
            url=self._config.base_url + "/graphql",
            headers=self._get_headers(),
            json={
                "query": query,
                "variables": variables,
            },
        )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403 and ["Retry-After"] in response.headers:
            retry_after = int(response.headers["Retry-After"])
            log.warning(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
            if retry_after > 15:
                retry_after = 60  # Wait max
            if retry_after < 2:
                retry_after = 5  # Wait minimum
            time.sleep(retry_after)
            max_retries -= 1
            if max_retries > 0:
                return self.graphql_client(query, variables, max_retries)
            else:
                raise GitHubClientError("Max retries limit reached")
        elif response.status_code in [502, 504]:
            wait_sec = 5
            log.warning(f"GH error, waiting {wait_sec}s and trying {max_retries} more time(s).")
            time.sleep(wait_sec)
            max_retries -= 1
            if max_retries > 0:
                return self.graphql_client(query, variables, max_retries)
            else:
                raise GitHubClientError(f"Max retries reached.\nGitHub error: {response.status_code} {response.text}")
        else:
            raise GitHubClientError(f"Error while executing query: {response.status_code} {response.text}")

    def rest_v3_client(self, path: str) -> Response:
        return _get_with_retries(
            url=f"{self._config.base_url}/{path}",
            headers=self._get_headers(),
        )

    def rest_v3_client_paging(self, path: str) -> Generator[Any, Any, Any]:
        def get_next_page(page):
            return page if page.headers.get("link") is not None else None

        headers = self._get_headers()

        first_page = _get_with_retries(
            url=f"{self._config.base_url}/{path}",
            headers=headers,
        )
        yield first_page

        next_page = first_page
        while get_next_page(next_page) is not None:
            try:
                next_page_url = next_page.links["next"]["url"]
                next_page = _get_with_retries(url=next_page_url, headers=headers)
                yield next_page

            except KeyError:
                log.debug("No more Github pages, returning")
                break

    def get_repository(self, repository_id: str) -> Repository | None:
        """
        Retrieves a single non-archived github repository
        """

        query = self._get_graphql_query("gh_query_repo")

        variables = {"name": repository_id, "owner": self._config.organization_name, "after": ""}
        log.debug(f"Query variables: {variables}")
        response = self.graphql_client(query=query, variables=variables)

        repository_resp = pydash.get(response, "data.repository", default=None)
        if repository_resp is None:
            errors = pydash.get(response, "errors", default=[])
            if len(errors) > 0:
                log.error(f"Errors occured for {repository_id}")
                for error in errors:
                    log.error(error)
            else:
                log.info(f"No repositories found for {repository_id}")
            return None

        repository = Repository.from_json(json_object=repository_resp)

        vuln_has_pages = pydash.get(repository_resp, "vulnerabilityAlerts.pageInfo.hasNextPage", default=False)
        if vuln_has_pages:
            log.warning(f"Repository '{repository_id}' has more than 100 open vulnerable dependencies.")

            variables["after"] = pydash.get(repository_resp, "vulnerabilityAlerts.pageInfo.endCursor")

            while True:
                vuln_response = self.graphql_client(query=query, variables=variables)
                repository.vulnerability_alerts += _parse_vulnerabilities(
                    pydash.get(vuln_response, "data.repository.vulnerabilityAlerts.nodes", default=[])
                )
                vulnerabilities_page = pydash.get(
                    repository_resp, "data.repository.vulnerabilityAlerts.pageInfo.hasNextPage", default=False
                )

                if not vulnerabilities_page:
                    break

                variables["after"] = pydash.get(
                    repository_resp, "data.repository.vulnerabilityAlerts.pageInfo.endCursor"
                )

        return repository

    def get_org_repositories_graphql(
        self, entries_per_page: int = 50, max_repos_retrieved: int = 10000, parial_results_on_error: bool = False
    ) -> list[Repository]:
        """
        Retrieves all non-archived repositories for the organization
        """

        if max_repos_retrieved < entries_per_page:
            count = max_repos_retrieved
        else:
            count = entries_per_page
        max_repos_retrieved -= count

        query = self._get_graphql_query("gh_query_org_repos")
        variables = {"owner": self._config.organization_name, "count": count, "cursor": ""}

        response = self.graphql_client(query, variables=variables)

        repositories = pydash.get(response, "data.repositoryOwner.repositories.nodes", default=[])

        if len(repositories) == 0:
            errors = pydash.get(response, "errors", default=[])
            if len(errors) > 0:
                log.error(f"Error when retrieving repositories from owner {self._config.organization_name}")
                for error in errors:
                    log.error(error)
            else:
                log.info(f"No repositories found for organization {self._config.organization_name}")
            return []

        org_has_pages = pydash.get(response, "data.repositoryOwner.repositories.pageInfo.hasNextPage", default=False)
        if org_has_pages:
            cursor = pydash.get(response, "data.repositoryOwner.repositories.pageInfo.endCursor", default="")

            try:
                while max_repos_retrieved >= 0:
                    max_repos_retrieved -= count
                    log.debug(f"Org results are paged, retrieving next batch of repos. Cursor: {cursor}")
                    variables["cursor"] = cursor
                    paged_response = self.graphql_client(query=query, variables=variables)
                    repositories += pydash.get(paged_response, "data.repositoryOwner.repositories.nodes", default=[])

                    org_page = pydash.get(
                        paged_response, "data.repositoryOwner.repositories.pageInfo.hasNextPage", default=False
                    )

                    if not org_page or not cursor:
                        break

                    cursor = pydash.get(
                        paged_response, "data.repositoryOwner.repositories.pageInfo.endCursor", default=""
                    )
            except (GitHubClientError, ChunkedEncodingError) as e:
                if parial_results_on_error:
                    log.error(f"Exception occurred while retrieving org repositories. Returning partial results. {e}")
                    log.exception(e)
                else:
                    raise e

        return [Repository.from_json(json_object=repo) for repo in repositories]

    def get_org_repositories_rest(
        self,
        per_page: int = 100,
        skip_archived: bool = True,
    ) -> list[Repository]:
        """
        Retrieves all non-archived repositories for a given organization
        """

        repositories = []
        for response in self.rest_v3_client_paging(f"orgs/{self._config.organization_name}/repos?per_page={per_page}"):
            if response.status_code == 200:
                if response.json():
                    for repo_json in response.json():
                        repository = Repository.from_rest_json(repo_json)
                        if repository.is_archived and skip_archived:
                            continue
                        repositories.append(repository)
                else:
                    continue
            else:
                raise GitHubClientError(
                    pydash.get(response.content, "message", default="")
                    + f"get_org_repositories_rest, org '{self._config.organization_name}': {response.status_code} {response.text}"
                )

        return repositories

    def get_team_repositories(self, team_slug: str, role_filter=None, per_page: int = 100) -> list[Repository]:
        """
        Retrieves all non-archived repositories for a given team
        """

        if role_filter is None:
            role_filter = ["admin", "maintain"]
        team_repos = []
        for response in self.rest_v3_client_paging(
            f"orgs/{self._config.organization_name}/teams/{team_slug}/repos?per_page={per_page}"
        ):
            if response.status_code == 200:
                if response.json():
                    for repo in response.json():
                        if pydash.get(repo, "role_name") in role_filter:
                            team_repos.append(Repository.from_rest_json(repo))
                else:
                    continue
            else:
                raise GitHubClientError(
                    pydash.get(response.content, "message", default="")
                    + f"GitHubClientError for team '{team_slug}': {response.status_code} {response.text}"
                )

        return team_repos

    def get_repo_security_settings(self, repo_name: str) -> RepositorySecuritySettings:
        reponse = self.rest_v3_client(f"repos/{self._config.organization_name}/{repo_name}")

        if reponse.status_code == 200 and reponse.json():
            return RepositorySecuritySettings.from_json(reponse.json())
        else:
            raise GitHubClientError(f"GitHubClientError: {reponse.status_code} {reponse.text}")

    def get_repo_workflow_permissions(self, repo_name: str) -> RepositoryDefaultWorkflowPermissions:
        reponse = self.rest_v3_client(
            f"repos/{self._config.organization_name}/{repo_name}/actions/permissions/workflow"
        )
        if reponse.status_code == 200 and reponse.json():
            return RepositoryDefaultWorkflowPermissions.from_json(reponse.json())
        else:
            raise GitHubClientError(f"GitHubClientError: {reponse.status_code} {reponse.text}")

    def get_repo_last_code_ql_analysis(
        self, repo_name: str, per_page: int = 10
    ) -> RepositoryCodeScanningAnalysis | None:
        # There's a risk of this reporting wrong if a codeql analysis is not in the most recent 'per page' results
        response = self.rest_v3_client(
            f"repos/{self._config.organization_name}/{repo_name}/code-scanning/analyses?per_page={per_page}"
        )
        if response.status_code == 200 and response.json():
            for analysis in response.json():
                if pydash.get(analysis, "tool.name") == "CodeQL":
                    return RepositoryCodeScanningAnalysis.from_json(analysis)
        elif response.status_code == 404 and "no analysis found" in response.json()["message"]:
            return None
        else:
            raise GitHubClientError(f"GitHubClientError: {response.status_code} {response.text}")

    def get_repo_dependency_scanning_alerts(
        self, repo_name: str, per_page: int = 100, state: str = "open"
    ) -> tuple[list[RepositoryVulnerabilityAlert], bool]:
        alert_list = []
        dependabot_alerts_enabled = False
        for response in self.rest_v3_client_paging(
            f"repos/{self._config.organization_name}/{repo_name}/dependabot/alerts?per_page={per_page}&state={state}"
        ):
            if response.status_code == 200:
                dependabot_alerts_enabled = True
                if response.json():
                    for alert in response.json():
                        alert_list.append(RepositoryVulnerabilityAlert.from_rest_json(alert))
                else:
                    continue
            elif response.text.startswith('{"message":"Dependabot alerts are disabled'):
                dependabot_alerts_enabled = False
            else:
                raise GitHubClientError(
                    pydash.get(response.content, "message", default="")
                    + f"GitHubClientError for repo '{repo_name}': {response.status_code} {response.text}"
                )

        return alert_list, dependabot_alerts_enabled

    def get_repo_code_scanning_alerts(
        self, repo_name: str, per_page: int = 100, state: str = "open"
    ) -> tuple[list[RepositoryCodeScanAlert], bool]:
        alert_list = []
        code_scan_enabled = False
        for response in self.rest_v3_client_paging(
            f"repos/{self._config.organization_name}/{repo_name}/code-scanning/alerts?per_page={per_page}&state={state}&tool_name=CodeQL"
        ):
            if response.status_code == 200:
                code_scan_enabled = True
                if response.json():
                    for alert in response.json():
                        alert_list.append(RepositoryCodeScanAlert.from_json(alert))
                else:
                    continue
            elif response.text.startswith('{"message":"Code scanning is not enabled'):
                code_scan_enabled = False
            elif response.status_code == 404 and "no analysis found" in response.json()["message"]:
                code_scan_enabled = False
            else:
                raise GitHubClientError(
                    pydash.get(response.content, "message", default="")
                    + f"GitHubClientError for repo '{repo_name}': {response.status_code} {response.text}"
                )

        return alert_list, code_scan_enabled

    def get_repo_secret_scanning_alerts(
        self, repo_name: str, per_page: int = 100, state: str = "open"
    ) -> tuple[list[RepositorySecretScanAlert], bool]:
        alert_list = []
        secret_scan_enabled = False
        for response in self.rest_v3_client_paging(
            f"repos/{self._config.organization_name}/{repo_name}/secret-scanning/alerts?per_page={per_page}&state={state}"
        ):
            if response.status_code == 200:
                secret_scan_enabled = True
                if response.json():
                    for alert in response.json():
                        alert_list.append(RepositorySecretScanAlert.from_json(alert))
                else:
                    continue
            elif response.text.startswith('{"message":"Secret scanning is disabled'):
                secret_scan_enabled = False
            else:
                raise GitHubClientError(f"GitHubClientError for {repo_name}: {response.status_code} {response.text}")

        return alert_list, secret_scan_enabled

    def has_no_codeowners_errors(
        self,
        repo_name: str,
    ) -> bool:
        response = self.rest_v3_client(f"repos/{self._config.organization_name}/{repo_name}/codeowners/errors")
        if response.status_code == 200:
            return pydash.get(response.json(), "errors") == []
        else:
            raise GitHubClientError(f"GitHubClientError for {repo_name}: {response.status_code} {response.text}")

    def get_repo_contributor_stats(self, repo_name: str) -> list[RepositoryContributorStats]:
        """
        Retrieves the contributors stats for a repository.
        """
        response = self.rest_v3_client(f"repos/{self._config.organization_name}/{repo_name}/stats/contributors")
        if response.status_code == 200:
            # The API can return an empty response with status 200 if the stats are being computed.
            # In this case, the response.json() will raise an error.
            try:
                return RepositoryContributorStats.from_json(response.json())
            except Exception as e:
                log.error(f"Error when parsing contributors stats for {repo_name}. Error: {e}")
                raise GitHubClientError(
                    f"GitHubClientError for {repo_name} contributors stats: {response.status_code} {response.text}"
                )
        else:
            raise GitHubClientError(
                f"GitHubClientError for {repo_name} contributors stats: {response.status_code} {response.text}"
            )
