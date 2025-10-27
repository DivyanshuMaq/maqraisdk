"""
Module: reviewer_tasks
This module defines the `reviewerTasks` class, which is responsible for managing and instantiating various prompt review tasks for OpenAI models using the CrewAI framework. The class loads task configurations from a YAML file and ensures that all required reviewer agents are provided and correctly mapped. It provides a method to retrieve a dictionary of initialized reviewer tasks, each associated with a specific agent and configuration.
Classes:
    reviewerTasks:
        - Loads reviewer task configurations from a YAML file.
        - Validates the presence of required reviewer agents in the provided dictionary.
        - Provides the `get_reviewer_tasks` method to instantiate and return reviewer tasks for:
            * Senior Prompt Review
            * XPIA Prompt Review
            * Groundedness Prompt Review
            * Jailbreak Prompt Review
            * Harmful Content Prompt Review
        - Handles various exceptions related to configuration loading, agent validation, and task instantiation, providing informative error messages.
"""

# Import necessary libraries


from crewai import Task 
# Import typing for type hinting
from typing import Optional
from ..config.reviewer_tasks_config import REVIEWER_TASKS_CONFIG


class reviewerTasks:
    """
    This class contains the tasks for reviewing prompts for OpenAI models.
    """

    def __init__(self, agents_dict: Optional[dict] = None):
        """
        Initializes the reviewerTasks class.
        """
        try:
            # Use Python config instead of YAML file
            self.review_tasks_config = REVIEWER_TASKS_CONFIG
            self.agents_dict = agents_dict
            if not self.agents_dict:
                raise ValueError(
                    "No agents list provided. Please provide a list of agents."
                )
            if self.agents_dict.get("senior_prompt_reviewer") is None:
                raise ValueError(
                    "Senior Prompt Reviewer agent not found in the provided agents list."
                )
            if self.agents_dict.get("xpia_prompt_reviewer") is None:
                raise ValueError(
                    "XPIA Prompt Reviewer agent not found in the provided agents list."
                )
            if self.agents_dict.get("groundedness_prompt_reviewer") is None:
                raise ValueError(
                    "Groundedness Prompt Reviewer agent not found in the provided agents list."
                )
            if self.agents_dict.get("jailbreak_prompt_reviewer") is None:
                raise ValueError(
                    "Jailbreak Prompt Reviewer agent not found in the provided agents list."
                )
            if self.agents_dict.get("hc_prompt_reviewer") is None:
                raise ValueError(
                    "Harmful Content Prompt Reviewer agent not found in the provided agents list."
                )
        except TypeError as te:
            raise TypeError(f"TypeError from reviewerTasks: {te}") from te
        except ValueError as ve:
            raise ValueError(f"ValueError from reviewerTasks: {ve}") from ve
        except AttributeError as ae:
            raise AttributeError(f"AttributeError from reviewerTasks: {ae}") from ae
        except IndexError as ie:
            raise IndexError(f"IndexError from reviewerTasks: {ie}") from ie
        except MemoryError as me:
            raise MemoryError(f"MemoryError from reviewerTasks: {me}") from me
        except ImportError as ie:
            raise ImportError(
                f"Configuration import failed. Please ensure the config module exists: {ie}"
            ) from ie
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred while creating reviewerTasks: {e}"
            ) from e

    def get_reviewer_tasks(self):
        """
        Returns a list of reviewer agents.
        """
        try:
            if "senior_prompt_review_task" not in self.review_tasks_config:
                raise ValueError(
                    "Senior Prompt Review Task configuration not found in the YAML file."
                )
            senior_prompt_review_task = Task(
                name="Senior Prompt Review Task",
                agent=self.agents_dict["senior_prompt_reviewer"],
                config=self.review_tasks_config["senior_prompt_review_task"],
                async_execution=False,
            )
            if "xpia_prompt_review_task" not in self.review_tasks_config:
                raise ValueError(
                    "XPIA Prompt Review Task configuration not found in the YAML file."
                )
            xpia_prompt_review_task = Task(
                name="XPIA Prompt Review Task",
                agent=self.agents_dict["xpia_prompt_reviewer"],
                config=self.review_tasks_config["xpia_prompt_review_task"],
                async_execution=False,
            )
            if "groundedness_prompt_review_task" not in self.review_tasks_config:
                raise ValueError(
                    "Groundedness Prompt Review Task configuration not found in the YAML file."
                )
            groundedness_prompt_review_task = Task(
                name="Groundedness Prompt Review Task",
                agent=self.agents_dict["groundedness_prompt_reviewer"],
                config=self.review_tasks_config["groundedness_prompt_review_task"],
                async_execution=False,
            )
            if "jailbreak_prompt_review_task" not in self.review_tasks_config:
                raise ValueError(
                    "Jailbreak Prompt Review Task configuration not found in the YAML file."
                )
            jailbreak_prompt_review_task = Task(
                name="Jailbreak Prompt Review Task",
                agent=self.agents_dict["jailbreak_prompt_reviewer"],
                config=self.review_tasks_config["jailbreak_prompt_review_task"],
                async_execution=False,
            )
            if "hc_prompt_review_task" not in self.review_tasks_config:
                raise ValueError(
                    "Harmful Content Prompt Review Task configuration not found in the YAML file."
                )
            hc_prompt_review_task = Task(
                name="Harmful Content Prompt Review Task",
                agent=self.agents_dict["hc_prompt_reviewer"],
                config=self.review_tasks_config["hc_prompt_review_task"],
                async_execution=False,
            )
            return {
                "senior_prompt_review_task": senior_prompt_review_task,
                "xpia_prompt_review_task": xpia_prompt_review_task,
                "groundedness_prompt_review_task": groundedness_prompt_review_task,
                "jailbreak_prompt_review_task": jailbreak_prompt_review_task,
                "hc_prompt_review_task": hc_prompt_review_task,
            }
        except TypeError as te:
            raise TypeError(f"TypeError from reviewerTasks: {te}") from te
        except ValueError as ve:
            raise ValueError(f"ValueError from reviewerTasks: {ve}") from ve
        except AttributeError as ae:
            raise AttributeError(f"AttributeError from reviewerTasks: {ae}") from ae
        except IndexError as ie:
            raise IndexError(f"IndexError from reviewerTasks: {ie}") from ie
        except MemoryError as me:
            raise MemoryError(f"MemoryError from reviewerTasks: {me}") from me
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred while creating reviewerTasks: {e}"
            ) from e
