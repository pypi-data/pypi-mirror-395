from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

from kl_kernel_logic import PsiDefinition
from dbl_core import BoundaryContext, BoundaryResult, PolicyDecision
from dbl_main import Pipeline

from .config import BoundaryConfig
from .llm_adapter import LlmPayload, LlmResult, call_openai_chat, dry_run_llm
from .pipeline_factory import create_pipeline, create_default_pipeline, create_minimal_pipeline, create_strict_pipeline


# ---------------------------------------------------------------------------
# BoundaryRequest / BoundaryResponse
# Typed structures for the /run endpoint.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class BoundaryRequest:
    """Incoming request to the boundary service."""
    prompt: str
    tenant_id: Optional[str] = None
    channel: Optional[str] = None
    max_tokens: int = 1024
    temperature: float = 0.7
    pipeline_mode: str = "basic_safety"  # minimal, basic_safety, standard, enterprise
    enabled_policies: Optional[list[str]] = None  # Explicit policy override


@dataclass(frozen=True)
class RequestEnvelope:
    """
    Envelope wrapping the LLM request for policy evaluation.
    Contains all information policies need to make decisions.
    """
    prompt: str
    model: str
    max_tokens: int
    temperature: float
    caller_id: str
    tenant_id: Optional[str]
    channel: Optional[str]
    
    def to_metadata(self) -> dict[str, Any]:
        """Convert to metadata dict for BoundaryContext."""
        return {
            "prompt": self.prompt,
            "prompt_length": len(self.prompt),
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }


@dataclass
class BoundarySnapshot:
    """
    Complete snapshot of a boundary execution.
    Used by the insights panel to show the full flow.
    """
    request_id: str
    timestamp: str
    
    # DBL layer
    boundary_context: dict[str, Any]
    policy_decisions: list[dict[str, Any]]
    dbl_outcome: str  # allow / modify / block
    
    # KL layer
    psi_definition: dict[str, Any]
    execution_trace_id: Optional[str] = None
    
    # LLM layer
    llm_payload: Optional[dict[str, Any]] = None
    llm_result: Optional[dict[str, Any]] = None
    
    # Meta
    was_blocked: bool = False
    block_reason: Optional[str] = None
    dry_run: bool = False


@dataclass
class BoundaryResponse:
    """Response from the boundary service."""
    content: str
    blocked: bool
    snapshot: BoundarySnapshot


# ---------------------------------------------------------------------------
# Pipeline selection
# ---------------------------------------------------------------------------

def _get_pipeline(mode: str, enabled_policies: Optional[list[str]] = None) -> Pipeline:
    """
    Select pipeline based on mode and optional policy override.
    
    Args:
        mode: Preset mode (minimal, basic_safety, standard, enterprise)
        enabled_policies: Optional explicit list of policies (overrides preset)
    """
    return create_pipeline(mode=mode, enabled_policies=enabled_policies)


# ---------------------------------------------------------------------------
# run_boundary_flow
# The main orchestration function that ties DBL, KL, and LLM together.
# ---------------------------------------------------------------------------

async def run_boundary_flow(
    request: BoundaryRequest,
    config: BoundaryConfig,
    dry_run: bool = False,
) -> BoundaryResponse:
    """
    Executes the full boundary flow:
    
    1. Build PsiDefinition for the LLM operation
    2. Build BoundaryContext for DBL
    3. Run DBL pipeline (policies)
    4. If allowed: run KL execution with LLM effector
    5. Return response + snapshot
    """
    request_id = str(uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()
    
    # -------------------------------------------------------------------------
    # Step 1: Build RequestEnvelope
    # Contains all information for policy evaluation.
    # -------------------------------------------------------------------------
    envelope = RequestEnvelope(
        prompt=request.prompt,
        model=config.model,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        caller_id="boundary_service",
        tenant_id=request.tenant_id,
        channel=request.channel,
    )
    
    # -------------------------------------------------------------------------
    # Step 2: Build PsiDefinition
    # This defines WHAT we want to execute (an LLM chat completion).
    # -------------------------------------------------------------------------
    psi = PsiDefinition(
        psi_type="llm",
        name="openai_chat",
        metadata={
            "model": config.model,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "prompt_preview": request.prompt[:100] if len(request.prompt) > 100 else request.prompt,
        },
    )
    
    # -------------------------------------------------------------------------
    # Step 3: Build BoundaryContext for DBL
    # This is what the policies will evaluate.
    # The 'prompt' key is required by ContentSafetyPolicy.
    # -------------------------------------------------------------------------
    boundary_ctx = BoundaryContext(
        psi=psi,
        caller_id=envelope.caller_id,
        tenant_id=envelope.tenant_id,
        channel=envelope.channel,
        metadata=envelope.to_metadata(),
    )
    
    # -------------------------------------------------------------------------
    # Step 4: Select and run DBL pipeline
    # Policies decide: allow / modify / block
    # User can override with enabled_policies
    # -------------------------------------------------------------------------
    pipeline = _get_pipeline(request.pipeline_mode, request.enabled_policies)
    dbl_result: BoundaryResult = pipeline.evaluate(boundary_ctx)
    
    policy_decisions = [
        {
            "policy": d.details.get("policy", "unknown"),
            "outcome": d.outcome,
            "reason": d.reason,
            "details": dict(d.details),
        }
        for d in dbl_result.decisions
    ]
    
    # -------------------------------------------------------------------------
    # Prepare snapshot (partial, before LLM)
    # -------------------------------------------------------------------------
    snapshot = BoundarySnapshot(
        request_id=request_id,
        timestamp=timestamp,
        boundary_context={
            "psi_type": psi.psi_type,
            "psi_name": psi.name,
            "tenant_id": request.tenant_id,
            "channel": request.channel,
            "metadata": dict(boundary_ctx.metadata),
        },
        policy_decisions=policy_decisions,
        dbl_outcome=dbl_result.final_outcome,
        psi_definition={
            "psi_type": psi.psi_type,
            "name": psi.name,
            "metadata": dict(psi.metadata),
        },
        dry_run=dry_run,
    )
    
    # -------------------------------------------------------------------------
    # Step 4: Check DBL decision
    # -------------------------------------------------------------------------
    if dbl_result.final_outcome == "block":
        snapshot.was_blocked = True
        snapshot.block_reason = dbl_result.decisions[-1].reason if dbl_result.decisions else "Blocked by policy"
        
        return BoundaryResponse(
            content=f"Request blocked: {snapshot.block_reason}",
            blocked=True,
            snapshot=snapshot,
        )
    
    # -------------------------------------------------------------------------
    # Step 5: Apply modifications from DBL (if any)
    # -------------------------------------------------------------------------
    effective_max_tokens = dbl_result.effective_metadata.get("max_tokens", request.max_tokens)
    
    llm_payload = LlmPayload(
        model=config.model,
        prompt=request.prompt,
        max_tokens=effective_max_tokens,
        temperature=request.temperature,
    )
    
    snapshot.llm_payload = {
        "model": llm_payload.model,
        "prompt_length": len(llm_payload.prompt),
        "max_tokens": llm_payload.max_tokens,
        "temperature": llm_payload.temperature,
    }
    
    # -------------------------------------------------------------------------
    # Step 6: Execute LLM
    # The LLM call is the KL effector operation.
    # Note: Full KL Kernel integration (Kernel.execute) is synchronous.
    # For async LLM calls, we trace manually here.
    # -------------------------------------------------------------------------
    if dry_run:
        llm_result = await dry_run_llm(llm_payload)
    else:
        llm_result = await call_openai_chat(llm_payload)
    
    # Generate trace ID (KL-style)
    trace_id = str(uuid4())
    
    snapshot.execution_trace_id = trace_id
    snapshot.llm_result = {
        "content_preview": llm_result.content[:200] if len(llm_result.content) > 200 else llm_result.content,
        "model": llm_result.model,
        "usage": llm_result.usage,
    }
    
    return BoundaryResponse(
        content=llm_result.content,
        blocked=False,
        snapshot=snapshot,
    )

