"""
Decorators for easy policy enforcement on functions.
"""
import functools
from typing import List, Optional
from pvd.sdk import Agent

def guard_tool(name: Optional[str] = None, policies: Optional[List[str]] = None, agent: Optional[Agent] = None):
    """
    Decorator to enforce policies on a tool function.
    
    If 'agent' is not provided, it expects the first argument of the function 
    to be an 'Agent' instance.
    """
    def decorator(func):
        tool_name = name or func.__name__
        tool_policies = policies or []
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_agent = agent
            if not current_agent and args and isinstance(args[0], Agent):
                current_agent = args[0]
            
            if not current_agent:
                raise ValueError("Paved: No agent instance found for guarded tool execution.")

            # Prepare payload
            payload = {
                "tool_name": tool_name,
                "args": args, 
                "kwargs": kwargs
            }
            
            # Enforce policy
            current_agent.check("tool", payload, policies=tool_policies)
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
