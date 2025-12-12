from typing import Any, List, Callable, TypeVar, Protocol, Sequence
from dataclasses import dataclass, field, InitVar
from functools import wraps
import inspect

# Default policy point constants
POINTS_LOW = 1
POINTS_MEDIUM = 3
POINTS_HIGH = 9

C = TypeVar("C")  # Context type variable

CheckFunction = Callable[..., bool]


class EvaluationContext(Protocol):
    """Protocol for evaluation context that can carry related data."""

    pass


class ContextValidationError(TypeError):
    """Raised when context validation fails for a check function."""

    def __init__(self, check_name: str, errors: list[str]):
        self.check_name = check_name
        self.errors = errors
        super().__init__(f"{check_name} context validation failed: {errors}")


def requires_context(**required_attrs: type | tuple[type, bool]):
    """Decorator that validates context has required attributes of specific types.

    This decorator ensures that a check function receives a context object with
    the required attributes, and that those attributes are instances of the
    specified types.

    Args:
        **required_attrs: Keyword arguments mapping attribute names to their
            expected types. Use a tuple (type, True) to mark an attribute as
            optional (can be None).

    Returns:
        A decorator function that wraps the check and validates context.

    Raises:
        ValueError: If context is None when required attributes are specified.
        ContextValidationError: If context validation fails (missing attributes,
            wrong types, or unexpected None values).

    Examples:
        # Required attribute (cannot be None)
        @requires_context(example_app=ExampleApplication)
        def check_has_type(app, context):
            return context.example_app.type is not None

        # Optional attribute (can be None)
        @requires_context(
            example_app=ExampleApplication,
            repositories=(list, True)  # Optional
        )
        def check_with_optional_repos(app, context):
            repos = context.repositories or []
            return len(repos) > 0

        # Multiple required attributes
        @requires_context(
            example_app=ExampleApplication,
            repositories=list,
            team=Team
        )
        def check_team_owns_repos(app, context):
            # All attributes guaranteed to exist and be correct type
            ...
    """

    def decorator(check_fn: CheckFunction) -> CheckFunction:
        @wraps(check_fn)
        def wrapper(obj: Any, context: Any = None) -> bool:
            if context is None and required_attrs:
                raise ValueError(f"{check_fn.__name__} requires context with: {list(required_attrs.keys())}")

            errors = []
            for attr, type_spec in required_attrs.items():
                # Parse optional flag: (type, True) means optional
                if isinstance(type_spec, tuple):
                    expected_type, optional = type_spec
                else:
                    expected_type, optional = type_spec, False

                if not hasattr(context, attr):
                    errors.append(f"missing attribute '{attr}'")
                    continue

                value = getattr(context, attr)
                if value is None:
                    if not optional:
                        errors.append(f"'{attr}' is None (expected {expected_type.__name__})")
                elif not isinstance(value, expected_type):
                    errors.append(f"'{attr}' is {type(value).__name__}, expected {expected_type.__name__}")

            if errors:
                raise ContextValidationError(check_fn.__name__, errors)

            return check_fn(obj, context)

        # Store metadata for introspection and documentation
        wrapper._required_context = required_attrs  # type: ignore
        wrapper._is_context_validated = True  # type: ignore
        return wrapper

    return decorator


def get_check_context_requirements(check: CheckFunction) -> dict[str, type | tuple[type, bool]] | None:
    """Get the context requirements for a check function.

    Args:
        check: A check function, possibly decorated with @requires_context.

    Returns:
        A dictionary mapping attribute names to their required types (or None
        if the check has no declared requirements). For optional attributes,
        the value is a tuple (type, True).

    Example:
        @requires_context(app=Application, extra=(ExtraData, True))
        def my_check(obj, context):
            ...

        reqs = get_check_context_requirements(my_check)
        # {'app': Application, 'extra': (ExtraData, True)}
    """
    return getattr(check, "_required_context", None)


def is_context_validated_check(check: CheckFunction) -> bool:
    """Check if a function is decorated with @requires_context.

    Args:
        check: A check function to inspect.

    Returns:
        True if the check is decorated with @requires_context, False otherwise.
    """
    return getattr(check, "_is_context_validated", False)


def _evaluate_checks(obj: Any, checks: Sequence[CheckFunction], context: Any = None) -> tuple[bool, dict[str, bool]]:
    """Evaluate checks with optional context support.

    Args:
        obj: The primary object being evaluated
        checks: List of check functions (may accept 1 or 2 parameters)
        context: Optional context object passed to checks that accept it

    Returns:
        Tuple of (all_passed, results_dict)
    """
    success = True
    results = {}
    for check in checks:
        # Determine if check accepts context by inspecting its signature
        try:
            sig = inspect.signature(check)
            accepts_context = len(sig.parameters) > 1
        except (ValueError, TypeError):
            # Fallback for built-ins or other callables without inspectable signatures
            accepts_context = False

        if accepts_context:
            result = check(obj, context)
        else:
            result = check(obj)

        success = success and result
        results[getattr(check, "__name__", str(check))] = result
    return success, results


def _calculate_score(points_sum: int, points_max: int, calculation_factor: float = 100) -> float:
    """Calculate percentage score, handling edge cases."""
    return (points_sum / points_max) * calculation_factor if points_max > 0 else 0


@dataclass
class EvaluatedPolicy:
    """Detailed information about a policy evaluation."""

    name: str
    points: int
    failed: bool
    qualified: bool
    check_results: dict[str, bool] = field(default_factory=dict)
    qualifier_results: dict[str, bool] = field(default_factory=dict)


@dataclass
class Policy:
    """A policy with qualifiers and checks for evaluation."""

    name: str
    points: int
    checks: list[CheckFunction]
    qualifiers: list[CheckFunction] = field(default_factory=list)

    def __post_init__(self):
        if not self.checks:
            raise ValueError("Policy must have at least one check")
        if self.points <= 0:
            raise ValueError("Points must be positive")

    def get_points(self, obj: Any, context: Any = None) -> int:
        """Get points if all checks pass, 0 otherwise.

        Args:
            obj: The object being evaluated
            context: Optional context object for context-aware checks
        """
        all_passed, _ = _evaluate_checks(obj, self.checks, context)
        return self.points if all_passed else 0

    def evaluate(self, obj_to_evaluate: Any, context: Any = None) -> EvaluatedPolicy:
        """Evaluate policy with optional context.

        Args:
            obj_to_evaluate: The object being evaluated
            context: Optional context object for context-aware checks
        """
        # Check if policy qualifies
        qualified, qualifier_results = _evaluate_checks(obj_to_evaluate, self.qualifiers, context)

        all_checks_pass, check_results = _evaluate_checks(obj_to_evaluate, self.checks, context)

        # Determine if policy failed (qualified but checks didn't all pass)
        failed = qualified and not all_checks_pass

        return EvaluatedPolicy(
            name=self.name,
            points=self.points,
            failed=failed,
            qualified=qualified,
            check_results=check_results,
            qualifier_results=qualifier_results,
        )


@dataclass
class GroupResult:
    name: str
    qualified: bool


@dataclass
class PolicyGroupResult(GroupResult):
    """Results of evaluating a PolicyGroup."""

    points_max: int
    points_sum: int
    evaluated_policies: List[EvaluatedPolicy] = field(default_factory=list)


@dataclass
class PolicyGroup:
    policies: list[Policy]
    name: str
    description: str = ""
    qualifiers: list[CheckFunction] = field(default_factory=list)

    def evaluate(self, obj_to_evaluate: Any, context: Any = None) -> PolicyGroupResult:
        """Evaluate policy group with optional context.

        Args:
            obj_to_evaluate: The object being evaluated
            context: Optional context object for context-aware checks
        """
        evaluated_policies = []
        points_max = 0
        points_sum = 0

        qualified, _ = _evaluate_checks(obj_to_evaluate, self.qualifiers, context)

        if qualified:
            for policy in self.policies:
                evaluated_policy = policy.evaluate(obj_to_evaluate, context)

                if evaluated_policy.qualified:  # Add to totals if qualified
                    points_max += policy.points
                    points_sum += evaluated_policy.points if not evaluated_policy.failed else 0

                evaluated_policies.append(evaluated_policy)

        return PolicyGroupResult(
            points_max=points_max,
            points_sum=points_sum,
            evaluated_policies=evaluated_policies,
            name=self.name,
            qualified=qualified,
        )


@dataclass
class TierResult:
    """Holds the evaluation result for a single tier."""

    tier: int
    points_max: int
    points_sum: int
    evaluated_policies: List[EvaluatedPolicy] = field(default_factory=list)


@dataclass
class TieredPolicyGroupResult(GroupResult):
    """Results of evaluating a TieredPolicyGroup."""

    tier_results: dict[int, TierResult] = field(default_factory=dict)

    def points_max(self) -> int:
        return sum(r.points_max for r in self.tier_results.values())

    def points_sum(self) -> int:
        return sum(r.points_sum for r in self.tier_results.values())


@dataclass
class TieredPolicyGroup:
    """Evaluates policies in tiers where failure in one tier affects subsequent tiers."""

    name: str
    description: str = ""
    _tiered_policies: dict[int, list[Policy]] = field(default_factory=dict)
    tiered_policies: InitVar[dict[int, list[Policy]] | None] = None
    qualifiers: list[CheckFunction] = field(default_factory=list)

    def __post_init__(self, tiered_policies):
        if tiered_policies:
            self.add_tiers(tiered_policies)

    def add_tier(self, tier: int, policies: list[Policy]):
        if tier < 1:
            raise ValueError("Tier must be 1 or higher")
        if tier in self._tiered_policies:
            raise ValueError(f"Tier {tier} already exists")
        if self._tiered_policies and tier != max(self._tiered_policies.keys()) + 1:
            raise ValueError("Tier must increment by one from the previous highest tier")
        self._tiered_policies[tier] = policies

    def add_tiers(self, tiered_policies: dict[int, list[Policy]]):
        """Add multiple tiers at once."""
        if not tiered_policies:
            raise ValueError("Tiered policies cannot be empty")

        sorted_tiers = sorted(tiered_policies.keys())
        if sorted_tiers != list(range(1, len(sorted_tiers) + 1)):
            raise ValueError("Tier keys must form a complete sequence starting from 1 (e.g., 1, 2, 3)")

        for tier, policies in tiered_policies.items():
            self.add_tier(tier, policies)

    def evaluate(self, obj_to_evaluate: Any, context: Any = None) -> TieredPolicyGroupResult:
        """Evaluate tiers, where failure in one tier affects subsequent tiers.

        Args:
            obj_to_evaluate: The object being evaluated
            context: Optional context object for context-aware checks
        """
        results = {}
        tier_failed = False

        policy_group_qualified, _ = _evaluate_checks(obj_to_evaluate, self.qualifiers, context)

        if not policy_group_qualified:
            return TieredPolicyGroupResult(
                name=self.name,
                tier_results=results,
                qualified=policy_group_qualified,
            )

        for tier_num in sorted(self._tiered_policies.keys()):
            policy_group = PolicyGroup(name="temp", policies=self._tiered_policies[tier_num])
            policy_group_result = policy_group.evaluate(obj_to_evaluate, context)

            if tier_failed or policy_group_result.points_max == 0:
                points_sum = 0
            else:
                points_sum = policy_group_result.points_sum
                # Mark subsequent tiers as failed if this tier didn't achieve max points
                if policy_group_result.points_sum < policy_group_result.points_max:
                    tier_failed = True

            results[tier_num] = TierResult(
                tier=tier_num,
                points_max=policy_group_result.points_max,
                points_sum=points_sum,
                evaluated_policies=policy_group_result.evaluated_policies,
            )

        return TieredPolicyGroupResult(
            name=self.name,
            tier_results=results,
            qualified=policy_group_qualified,
        )
