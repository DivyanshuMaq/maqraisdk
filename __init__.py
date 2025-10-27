"""
MAQ RAI SDK - A Python SDK for Responsible AI compliance in prompt engineering.

This package provides tools for reviewing, updating, and testing AI prompts
to ensure compliance with Responsible AI principles including:
- Groundedness
- XPIA (Cross-Prompt Injection Attack) prevention  
- Jailbreak prevention
- Harmful content prevention
"""

from .rai_agent.connections.open_ai import OpenAIClient
from .rai_agent.utility.promptReviewer import PromptReviewer
from .rai_agent.utility.promptUpdater import PromptUpdater
from .rai_agent.utility.promptTestcaseGenerator import promptTestcaseGenerator

__version__ = "0.1.0"

__all__ = [
    "OpenAIClient",
    "PromptReviewer", 
    "PromptUpdater",
    "promptTestcaseGenerator",
]
