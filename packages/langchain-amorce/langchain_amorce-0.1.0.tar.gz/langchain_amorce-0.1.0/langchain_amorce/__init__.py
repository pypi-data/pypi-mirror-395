"""
LangChain-Amorce Integration

Secure LangChain agents with Ed25519 signatures and HITL approvals.
"""

from langchain_amorce.agent import AmorceAgent
from langchain_amorce.tools import AmorceToolWrapper

__version__ = "0.1.0"
__all__ = ["AmorceAgent", "AmorceToolWrapper"]
