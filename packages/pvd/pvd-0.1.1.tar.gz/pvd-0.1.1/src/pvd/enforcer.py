"""
Policy enforcement interface and HTTP client for Paved SDK.

All policy checks go through the Platform API
at POST /v1/policies/check. The platform authenticates, logs and forwards
to the Guard service.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class PolicyEnforcer(ABC):
    """Abstract base class for policy enforcement."""

    @abstractmethod
    def check_policy(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check a policy request and return the decision.

        Args:
            request: Policy check request containing action, payload, context, etc.

        Returns:
            Policy decision with 'decision' (allow/deny/redact), 'reasons', etc.
        """
        raise NotImplementedError


class MockPolicyEnforcer(PolicyEnforcer):
    """Mock policy enforcer for testing that always allows."""

    def check_policy(self, request: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "decision": "allow",
            "reasons": [],
            "trace_id": "mock",
            "policy_version": "mock",
            "policy_digest": "mock",
        }


class HTTPPolicyEnforcer(PolicyEnforcer):
    """HTTP-based policy enforcer (Platform policies endpoint)."""

    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def check_policy(self, request: Dict[str, Any]) -> Dict[str, Any]:
        import requests

        url = f"{self.base_url}/v1/policies/check"
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        # Forward policy if present to allow OPA to evaluate them
        check_request = {
            "agent_id": request.get("context", {}).get("agent_id"),
            "action": request["action"],
            "payload": request["payload"],
            "context": request.get("context"),
            "metrics": request.get("metrics", {}),
        }
        if "policies" in request:
            check_request["policies"] = request.get("policies") or []
        if "policy" in request:
            check_request["policy"] = request.get("policy") or {}

        try:
            response = requests.post(url, json=check_request, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            return {
                "decision": result.get("decision", "deny"),
                "reasons": result.get("reasons", []),
                "trace_id": result.get("trace_id", "unknown"),
                "policy_version": result.get("policy_version", "unknown"),
                "policy_digest": result.get("policy_digest", "unknown"),
            }
        except Exception as e:
            # Fail closed - deny by default if platform is unavailable
            return {
                "decision": "deny",
                "reasons": [{"msg": f"policy_check_error: {str(e)}"}],
                "trace_id": "error",
                "policy_version": "unknown",
                "policy_digest": "unknown",
            }


    
