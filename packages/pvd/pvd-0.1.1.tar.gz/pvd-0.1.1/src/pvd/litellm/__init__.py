"""
Paved wrapper for LiteLLM with policy enforcement.

This module provides a drop-in wrapper for LiteLLM that enforces Paved policies
while providing access to 100+ LLM providers through a unified interface.
"""
from .wrapper import LiteLLM

__all__ = ["LiteLLM"]
