"""
Paved Callbacks for LangChain Policy Enforcement.
"""
from typing import Any, Dict, List, Optional
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler
from pvd.sdk import Agent

class PavedCallbackHandler(BaseCallbackHandler):
    """
    Callback Handler that enforces Paved policies on LLM and Tool execution.
    """

    def __init__(self, agent: Agent):
        self.agent = agent

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        policies: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when LLM starts running."""
        model = kwargs.get("invocation_params", {}).get("model", "unknown")
        
        for prompt in prompts:
            self.agent.check("llm", {
                "text": prompt,
                "model": model,
                "framework": "langchain"
            }, policies=policies)

    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[Any]],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        policies: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when Chat Model starts running."""
        model = kwargs.get("invocation_params", {}).get("model", "unknown")
        
        # Flatten messages to text for policy check
        for message_list in messages:
            text_content = ""
            for msg in message_list:
                # Handle different message types (HumanMessage, AIMessage, etc.)
                if hasattr(msg, "content"):
                    text_content += f"{msg.type}: {msg.content}\n"
                else:
                    text_content += str(msg) + "\n"
            
            self.agent.check("llm", {
                "text": text_content,
                "model": model,
                "framework": "langchain",
                "messages": [m.dict() if hasattr(m, "dict") else str(m) for m in message_list]
            }, policies=policies)

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        policies: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when tool starts running."""
        tool_name = serialized.get("name", "unknown")
        
        self.agent.check("tool", {
            "tool_name": tool_name,
            "input": input_str,
            "framework": "langchain"
        }, policies=policies)
