"""
Paved wrapper for Anthropic with policy enforcement.

This module provides a drop-in replacement for the Anthropic SDK that enforces
Paved policies while maintaining full API compatibility.
"""
from .wrapper import Anthropic, AsyncAnthropic

__all__ = ["Anthropic", "AsyncAnthropic"]
