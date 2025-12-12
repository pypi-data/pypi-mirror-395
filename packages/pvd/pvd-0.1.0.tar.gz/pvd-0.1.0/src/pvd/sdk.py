"""
Paved SDK for policy-enforced agent execution (remote-only).
"""
import os
import uuid
import time
import logging
import functools
import atexit
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable, Union

try:
    import tiktoken  # optional, token counting
except Exception:  # pragma: no cover
    tiktoken = None

from .enforcer import PolicyEnforcer, HTTPPolicyEnforcer, MockPolicyEnforcer


class PolicyDeniedError(Exception):
    """Exception raised when a policy denies an action."""

    def __init__(self, decision: Dict[str, Any]):
        self.decision = decision
        reasons = [r.get("msg", str(r)) for r in decision.get("reasons", [])]
        super().__init__(f"Policy denied: {', '.join(reasons)}")


class Agent:
    """
    Paved Agent SDK.

    Provides policy-enforced access to LLMs and tools. Default mode is
    SDK-remote: policy checks and telemetry go to the Platform API.
    """

    def __init__(
        self,
        agent_id: str,
        task_id: Optional[str] = None,
        policies: Optional[List[str]] = None,
        policy_bundle: str = "default",
        policy_config: Optional[Dict[str, Any]] = None,
        context_configs: Optional[Dict[str, Any]] = None,
        enforcer: Optional[PolicyEnforcer] = None,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        execution_mode: Optional[str] = None,  # sdk_remote or platform_hosted
    ):
        self.agent_id = agent_id
        self.task_id = task_id or str(uuid.uuid4())
        self.policies = policies or []
        self.policy_bundle = policy_bundle
        self.policy_config = policy_config or {}
        self.logger = logging.getLogger(f"paved.agent.{agent_id}")
        self.context_configs = context_configs or {}

        # Track all policy decisions for governance reporting
        self._policy_decisions: List[Dict[str, Any]] = []
        self._flagged_decisions: List[Dict[str, Any]] = []  # NEW: Track flagged decisions separately

        # Determine execution mode (default to sdk_remote)
        if execution_mode:
            self.execution_mode = execution_mode
        elif os.getenv("PAVED_RUNTIME") == "vm":
            self.execution_mode = "platform_hosted"
        else:
            self.execution_mode = "sdk_remote"

        # Platform API base URL (default to hosted cloud API)
        raw_base = base_url or os.getenv("PAVED_API_URL", "https://app.hipaved.com")
        raw_base = raw_base.rstrip('/')
        if raw_base.endswith('/v1'):
            raw_base = raw_base[:-3]
        elif raw_base.endswith('/v1/'):
            raw_base = raw_base[:-4]
        self.base_url = raw_base
        self.api_key = api_key or os.getenv("PAVED_API_KEY")

        # SDK‑remote invocation tracking
        if self.execution_mode == "sdk_remote":
            self._invocation_id = str(uuid.uuid4())
            self._started_at = datetime.utcnow()
            self._completed_at: Optional[datetime] = None
            self._status = "running"
            self._result = None
            self._error = None

            atexit.register(self._report_telemetry)

        # Set up policy enforcer
        if enforcer:
            self.enforcer = enforcer
        elif self.execution_mode == "sdk_remote":
            # Route through Platform policies endpoint
            self.enforcer = HTTPPolicyEnforcer(self.base_url, self.api_key)
        else:
            # Placeholder for platform_hosted; keep mock to avoid network deps here
            self.enforcer = MockPolicyEnforcer()
            self.logger.warning("Using MockPolicyEnforcer - no actual policy enforcement")

        # Initialize token counting
        try:
            self.tokenizer = tiktoken.get_encoding("cl100k_base") if tiktoken else None
        except Exception:  # pragma: no cover
            self.tokenizer = None
            self.logger.warning("Failed to initialize tokenizer")

    def _count_tokens(self, text: str, model: str = "gpt-4") -> int:
        if not self.tokenizer or not text:
            return 0
        try:
            return len(self.tokenizer.encode(text))
        except Exception:  # pragma: no cover
            return max(1, len(text) // 4)

    def _estimate_cost(self, tokens_in: int, tokens_out: int, model: str) -> float:
        # Simplified cost estimation
        costs_per_1k = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "gpt-3.5-turbo": {"input": 0.001, "output": 0.002},
            "gpt-4o": {"input": 0.005, "output": 0.015},
            "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
        }
        model_cost = costs_per_1k.get(model, costs_per_1k["gpt-4"])
        return (tokens_in / 1000) * model_cost["input"] + (tokens_out / 1000) * model_cost["output"]

    def _check_policy(
        self,
        action: str,
        payload: Dict[str, Any],
        estimated_tokens: int = 0,
        estimated_cost: float = 0.0,
        policies: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        request = {
            "action": action,
            "payload": payload,
            "context": {
                "project_id": "default",
                "agent_id": self.agent_id,
                "task_id": self.task_id,
                "user": "agent",
                "configs": self.context_configs,
            },
            "policies": policies if policies is not None else self.policies,
            "config": self.policy_config,
            "metrics": {"tokens_in": estimated_tokens, "estimated_cost_usd": estimated_cost},
        }

        decision = self.enforcer.check_policy(request)

        # Record decision for governance tracking
        decision_record = {
            "action": action,
            "decision": decision.get("decision", "unknown"),
            "reasons": decision.get("reasons", []),
            "timestamp": time.time(),
            "payload_summary": self._safe_payload_summary(action, payload),
            "policies": policies if policies is not None else self.policies,
            "trace_id": decision.get("trace_id"),
        }
        self._policy_decisions.append(decision_record)

        # NEW: Track flagged decisions separately
        if decision.get("decision") == "flag":
            self._flagged_decisions.append(decision_record)
            self.logger.warning(f"🚩 Policy flagged {action}: {decision.get('reasons', [])}")

        return decision

    def check(self, action: str, payload: Dict[str, Any], policies: Optional[List[str]] = None) -> None:
        """
        Explicitly check if an action is allowed.
        Raises PolicyDeniedError if denied.
        Flags are logged but do not raise an exception.
        """
        decision = self._check_policy(action, payload, policies=policies)
        # NEW: Only raise exception on "deny", not "flag"
        if decision["decision"] == "deny":
            raise PolicyDeniedError(decision)


    def _safe_payload_summary(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        summary: Dict[str, Any] = {"action": action, "keys": list(payload.keys()) if isinstance(payload, dict) else []}
        if action == "llm" and isinstance(payload, dict):
            summary["model"] = payload.get("model", "unknown")
            summary["max_tokens"] = payload.get("max_tokens", 0)
            summary["prompt_length"] = len(str(payload.get("text", "")))
        elif action == "email" and isinstance(payload, dict):
            summary["recipients_count"] = len(payload.get("to", []))
            summary["has_attachments"] = len(payload.get("attachments", [])) > 0
        elif action == "http" and isinstance(payload, dict):
            summary["method"] = payload.get("method", "unknown")
            summary["host"] = payload.get("host", "unknown")
        return summary

    def get_policy_decisions(self) -> List[Dict[str, Any]]:
        return self._policy_decisions

    def get_governance_summary(self) -> Dict[str, Any]:
        total_checks = len(self._policy_decisions)
        denied = [d for d in self._policy_decisions if d["decision"] == "deny"]
        flagged = [d for d in self._policy_decisions if d["decision"] == "flag"]
        allowed = [d for d in self._policy_decisions if d["decision"] == "allow"]
        return {
            "total_checks": total_checks,
            "allowed_actions": len(allowed),
            "denied_actions": len(denied),
            "flagged_actions": len(flagged),  # NEW
            "decisions": self._policy_decisions,
            "violations": [
                {
                    "action": d["action"],
                    "reasons": d["reasons"],
                    "timestamp": d["timestamp"],
                    "payload_summary": d["payload_summary"],
                    "policies": d["policies"],
                }
                for d in denied
            ],
            "flagged_decisions": [  # NEW
                {
                    "action": d["action"],
                    "reasons": d["reasons"],
                    "timestamp": d["timestamp"],
                    "payload_summary": d["payload_summary"],
                    "policies": d["policies"],
                }
                for d in flagged
            ],
            "overall_decision": "deny" if denied else "flag" if flagged else "allow",  # NEW: Three-way decision
        }

    def _report_telemetry(self):
        if self.execution_mode != "sdk_remote":
            return
        if not self.api_key:
            self.logger.warning("Cannot report telemetry: no API key configured")
            return
        try:
            import requests

            if not self._completed_at:
                self._completed_at = datetime.utcnow()
                if self._status == "running":
                    self._status = "completed"

            duration_ms = int((self._completed_at - self._started_at).total_seconds() * 1000)
            governance = self.get_governance_summary()
            telemetry = {
                "invocation_id": getattr(self, "_invocation_id", str(uuid.uuid4())),
                "started_at": self._started_at.isoformat(),
                "completed_at": self._completed_at.isoformat(),
                "duration_ms": duration_ms,
                "status": self._status,
                "result": self._result,
                "error": self._error,
                "policies_applied": [d["action"] for d in self._policy_decisions],
                "policy_violations": governance["violations"],
                "flagged_decisions": governance["flagged_decisions"],  # NEW: Send flagged decisions
                "governance_decision": governance["overall_decision"],
            }

            url = f"{self.base_url}/v1/agents/{self.agent_id}/telemetry"
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            response = requests.post(url, json=telemetry, headers=headers, timeout=10)
            response.raise_for_status()
            self.logger.info("Telemetry reported successfully")
        except Exception as e:  # pragma: no cover
            self.logger.warning(f"Failed to report telemetry: {e}")

    def complete(self, result: Any = None, error: Optional[str] = None, status: Optional[str] = None):
        if self.execution_mode == "sdk_remote":
            self._completed_at = datetime.utcnow()
            self._result = result
            self._error = error
            self._status = status or ("failed" if error else "completed")
            self._report_telemetry()

    def __del__(self):  # pragma: no cover
        if self.execution_mode == "sdk_remote" and not getattr(self, "_completed_at", None):
            self._report_telemetry()

    # ---- Governed operations ----
    def llm(
        self,
        prompt: str,
        model: str = "gpt-4o-mini",
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs,
    ) -> str:
        input_tokens = self._count_tokens(prompt, model)
        estimated_cost = self._estimate_cost(input_tokens, max_tokens, model)
        payload = {"text": prompt, "model": model, "max_tokens": max_tokens, "temperature": temperature, **kwargs}
        decision = self._check_policy("llm", payload, input_tokens, estimated_cost)
        # NEW: Only block on "deny", allow "flag" and "allow" to proceed
        if decision["decision"] == "deny":
            raise PolicyDeniedError(decision)
        self.logger.info(f"LLM call approved for model {model}, {input_tokens} tokens")
        return f"Mock LLM response for: {prompt[:50]}..."

    def http_request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        data: Any = None,
        **kwargs,
    ) -> Dict[str, Any]:
        from urllib.parse import urlparse

        parsed = urlparse(url)
        payload = {
            "method": method,
            "url": url,
            "host": parsed.netloc,
            "path": parsed.path,
            "headers": headers or {},
            "data": data,
        }
        decision = self._check_policy("http", payload)
        # NEW: Only block on "deny", allow "flag" and "allow" to proceed
        if decision["decision"] == "deny":
            raise PolicyDeniedError(decision)
        self.logger.info(f"HTTP {method} request approved for {url}")
        return {"status": 200, "data": "Mock HTTP response"}

    def send_email(
        self,
        to: Union[str, List[str]],
        subject: str,
        body: str,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
        attachments: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        payload = {
            "to": to if isinstance(to, list) else [to],
            "subject": subject,
            "body": body,
            "cc": cc if isinstance(cc, list) else ([cc] if cc else []),
            "bcc": bcc if isinstance(bcc, list) else ([bcc] if bcc else []),
            "attachments": attachments or [],
        }
        decision = self._check_policy("email", payload)
        # NEW: Only block on "deny", allow "flag" and "allow" to proceed
        if decision["decision"] == "deny":
            raise PolicyDeniedError(decision)
        self.logger.info(f"Email send approved to {payload['to']}")
        return {"status": "sent", "message_id": str(uuid.uuid4())}


def tool(name: Optional[str] = None, policies: Optional[List[str]] = None):
    """Decorator for policy‑enforced tool functions."""

    def decorator(func: Callable) -> Callable:
        tool_name = name or func.__name__
        _tool_policies = policies or []

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not args or not isinstance(args[0], Agent):
                raise ValueError("Agent instance required for tool calls")
            agent: Agent = args[0]
            payload = {"tool_name": tool_name, "args": args[1:], "kwargs": kwargs}
            decision = agent._check_policy("tool", payload)
            # NEW: Only block on "deny", allow "flag" and "allow" to proceed
            if decision["decision"] == "deny":
                raise PolicyDeniedError(decision)
            agent.logger.info(f"Tool call approved: {tool_name}")
            return func(*args, **kwargs)

        wrapper._paved_tool = True  # type: ignore[attr-defined]
        wrapper._paved_tool_name = tool_name  # type: ignore[attr-defined]
        wrapper._paved_tool_policies = _tool_policies  # type: ignore[attr-defined]
        return wrapper

    return decorator
