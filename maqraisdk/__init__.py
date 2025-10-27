"""
rai_agent package
This package provides tools and components for managing AI agent workflows, including connections to language models, agent definitions, task management, crew organization, and utility functions for prompt review and updates.
Modules imported:
- connections: Contains OpenAIClient for OpenAI API interactions and CustomLLM for enhanced language model functionality.
- utility: Offers PromptReviewer for reviewing prompts and PromptUpdater for updating prompts.

"""

from .connections import (
    OpenAIClient,  # Import OpenAIClient for OpenAI API interactions
)

from .utility import (
    PromptReviewer,  # Import PromptReviewer for reviewing prompts
    PromptUpdater,  # Import PromptUpdater for updating prompts
    promptTestcaseGenerator, 
)

__all__: list[str] = [
    "OpenAIClient",  # Specify OpenAIClient for export
    "PromptReviewer",  # Specify PromptReviewer for export
    "PromptUpdater",  # Specify PromptUpdater for export
    "promptTestcaseGenerator",  # Specify promptTestcaseGenerator for export
]  # Specify what is exported from this module
