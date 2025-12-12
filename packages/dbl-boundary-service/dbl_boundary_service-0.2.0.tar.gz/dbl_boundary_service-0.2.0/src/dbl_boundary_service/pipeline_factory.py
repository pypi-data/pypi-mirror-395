from __future__ import annotations

from typing import Callable, Optional

from dbl_main import Pipeline, Policy
from dbl_main.policies.rate_limit import RateLimitPolicy
from dbl_main.policies.content_safety import ContentSafetyPolicy


# ---------------------------------------------------------------------------
# Policy registry
# Maps policy names to their factory classes
# ---------------------------------------------------------------------------

KNOWN_POLICIES = {
    "content_safety": ContentSafetyPolicy,
    "rate_limit": RateLimitPolicy,
}


# ---------------------------------------------------------------------------
# Default blocked patterns for content safety
# ---------------------------------------------------------------------------

DEFAULT_BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "disregard all prior",
    "bypass security",
    "act as if",
    "pretend you are",
]

STRICT_BLOCKED_PATTERNS = [
    *DEFAULT_BLOCKED_PATTERNS,
    "jailbreak",
    "roleplay",
    "system prompt",
    "developer mode",
]


# ---------------------------------------------------------------------------
# Pipeline Modes with clear semantics
# 
# minimal: No policies (testing only)
# basic_safety: Light content safety only (DEFAULT)
# standard: Balanced safety + rate limiting
# enterprise: Strict safety, strict rate limiting, full audit mode
# ---------------------------------------------------------------------------

def create_pipeline(
    mode: str = "basic_safety",
    enabled_policies: Optional[list[str]] = None,
) -> Pipeline:
    """
    Creates a pipeline based on mode and optional policy override.
    
    Modes:
    - minimal: No policies applied (testing only)
    - basic_safety: Light content safety only (DEFAULT)
    - standard: Balanced safety + rate limiting
    - enterprise: Strict safety, strict rate limiting, full audit
    
    Args:
        mode: Preset mode (minimal, basic_safety, standard, enterprise)
        enabled_policies: Optional explicit list of policies (overrides preset)
    
    Returns:
        Configured Pipeline with appropriate policies
    """
    # If explicit policies provided, user override has priority
    if enabled_policies is not None:
        return build_pipeline_from_names(enabled_policies)
    
    # Preset pipelines based on mode
    if mode == "minimal":
        return Pipeline(name="minimal", policies=[])
    
    elif mode == "basic_safety":
        return Pipeline(
            name="basic_safety",
            policies=[
                ContentSafetyPolicy(
                    blocked_patterns=DEFAULT_BLOCKED_PATTERNS,
                    content_key="prompt",
                ),
            ],
        )
    
    elif mode == "standard":
        return Pipeline(
            name="standard",
            policies=[
                ContentSafetyPolicy(
                    blocked_patterns=DEFAULT_BLOCKED_PATTERNS,
                    content_key="prompt",
                ),
                RateLimitPolicy(
                    max_requests=100,
                    window_seconds=60,
                ),
            ],
        )
    
    elif mode == "enterprise":
        return Pipeline(
            name="enterprise",
            policies=[
                ContentSafetyPolicy(
                    blocked_patterns=STRICT_BLOCKED_PATTERNS,
                    content_key="prompt",
                ),
                RateLimitPolicy(
                    max_requests=10,
                    window_seconds=60,
                ),
                # TODO: Add AuditEnforcementPolicy when available
            ],
        )
    
    # Fallback: standard (safe default)
    return Pipeline(
        name="standard",
        policies=[
            ContentSafetyPolicy(
                blocked_patterns=DEFAULT_BLOCKED_PATTERNS,
                content_key="prompt",
            ),
            RateLimitPolicy(
                max_requests=100,
                window_seconds=60,
            ),
        ],
    )


def build_pipeline_from_names(
    policy_names: list[str],
    rate_checker: Optional[Callable[[str, int], int]] = None,
    blocked_patterns: Optional[list[str]] = None,
) -> Pipeline:
    """
    Builds a pipeline from a list of policy names.
    Used when user explicitly overrides with enabled_policies.
    
    Args:
        policy_names: List of policy identifiers (e.g. ["content_safety", "rate_limit"])
        rate_checker: Optional rate checker for rate_limit policy
        blocked_patterns: Optional patterns for content_safety policy
    """
    policies: list[Policy] = []
    
    for name in policy_names:
        policy_class = KNOWN_POLICIES.get(name)
        if policy_class is None:
            continue
        
        # Instantiate with appropriate config
        if name == "rate_limit":
            policies.append(RateLimitPolicy(
                max_requests=100,
                window_seconds=60,
                rate_checker=rate_checker,
            ))
        elif name == "content_safety":
            policies.append(ContentSafetyPolicy(
                blocked_patterns=blocked_patterns or DEFAULT_BLOCKED_PATTERNS,
                content_key="prompt",
            ))
        else:
            # Generic instantiation
            policies.append(policy_class())
    
    return Pipeline(name="custom", policies=policies)


# ---------------------------------------------------------------------------
# Legacy compatibility functions (deprecated)
# ---------------------------------------------------------------------------

def create_default_pipeline(
    max_requests: int = 100,
    window_seconds: int = 60,
    rate_checker: Optional[Callable[[str, int], int]] = None,
    blocked_patterns: Optional[list[str]] = None,
    content_key: str = "prompt",
) -> Pipeline:
    """
    Legacy function for backward compatibility.
    Use create_pipeline("standard") instead.
    """
    return create_pipeline("standard")


def create_minimal_pipeline() -> Pipeline:
    """
    Legacy function for backward compatibility.
    Use create_pipeline("minimal") instead.
    """
    return create_pipeline("minimal")


def create_strict_pipeline(
    blocked_patterns: Optional[list[str]] = None,
) -> Pipeline:
    """
    Legacy function for backward compatibility.
    Use create_pipeline("enterprise") instead.
    """
    return create_pipeline("enterprise")
