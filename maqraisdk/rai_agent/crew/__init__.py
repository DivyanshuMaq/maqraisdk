"""
This module initializes the crew package by importing the main crew classes.

Imports:
  reviewerCrew (from .reviewer_crew): Handles review-related crew operations.
  updaterCrew (from .updater_crew): Handles update-related crew operations.
"""

from .reviewer_crew import reviewerCrew
from .updater_crew import updaterCrew


__all__: list[str] = (
    []
)  # Initialize __all__ to an empty list to control what is exported
