"""
Module: updater_tasks
This module defines the `updaterTasks` class, which is responsible for managing and creating update tasks for various OpenAI model prompt updaters. The class loads task configurations from a YAML file and validates the presence of required updater agents. It provides a method to retrieve configured updater tasks for different prompt update categories, such as senior, XPIA, groundedness, jailbreak, and harmful content.
Classes:
    updaterTasks:
        - Initializes with a dictionary of agents and loads task configurations from a YAML file.
        - Validates the presence of required updater agents in the provided dictionary.
        - Provides the `get_updater_tasks` method to return a dictionary of configured Task objects for each updater category.
Exceptions:
    Raises detailed exceptions for missing configuration files, missing agents, missing task configurations, and other runtime errors to aid in debugging and robust error handling.
"""

# Import necessary libraries

from crewai import Task 
# Import typing for type hinting
from typing import Optional
from ..config.updater_tasks_config import UPDATER_TASKS_CONFIG


class updaterTasks:
    """
    This class contains the tasks for updateing prompts for OpenAI models.
    """

    def __init__(self, agents_dict: Optional[dict] = None):
        """
        Initializes the updaterTasks class.
        """
        try:
            # Use Python config instead of YAML file
            self.update_tasks_config = UPDATER_TASKS_CONFIG
            self.agents_dict = agents_dict
            if not self.agents_dict:
                raise ValueError(
                    "No agents list provided. Please provide a list of agents."
                )
            if self.agents_dict.get("senior_prompt_updater") is None:
                raise ValueError(
                    "Senior Prompt updater agent not found in the provided agents list."
                )
            if self.agents_dict.get("xpia_prompt_updater") is None:
                raise ValueError(
                    "XPIA Prompt updater agent not found in the provided agents list."
                )
            if self.agents_dict.get("groundedness_prompt_updater") is None:
                raise ValueError(
                    "Groundedness Prompt updater agent not found in the provided agents list."
                )
            if self.agents_dict.get("jailbreak_prompt_updater") is None:
                raise ValueError(
                    "Jailbreak Prompt updater agent not found in the provided agents list."
                )
            if self.agents_dict.get("hc_prompt_updater") is None:
                raise ValueError(
                    "Harmful Content Prompt updater agent not found in the provided agents list."
                )
        except TypeError as te:
            raise TypeError(f"TypeError from updaterTasks: {te}") from te
        except ValueError as ve:
            raise ValueError(f"ValueError from updaterTasks: {ve}") from ve
        except AttributeError as ae:
            raise AttributeError(f"AttributeError from updaterTasks: {ae}") from ae
        except IndexError as ie:
            raise IndexError(f"IndexError from updaterTasks: {ie}") from ie
        except MemoryError as me:
            raise MemoryError(f"MemoryError from updaterTasks: {me}") from me
        except ImportError as ie:
            raise ImportError(
                f"Configuration import failed. Please ensure the config module exists: {ie}"
            ) from ie
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred while creating updaterTasks: {e}"
            ) from e

    def get_updater_tasks(self):
        """
        Returns a list of updater agents.
        """
        try:
            if "senior_prompt_update_task" not in self.update_tasks_config:
                raise ValueError(
                    "Senior Prompt update Task configuration not found in the YAML file."
                )
            senior_prompt_update_task = Task(
                name="Senior Prompt update Task",
                agent=self.agents_dict["senior_prompt_updater"],
                config=self.update_tasks_config["senior_prompt_update_task"],
                async_execution=False,
            )
            if "xpia_prompt_update_task" not in self.update_tasks_config:
                raise ValueError(
                    "XPIA Prompt update Task configuration not found in the YAML file."
                )
            xpia_prompt_update_task = Task(
                name="XPIA Prompt update Task",
                agent=self.agents_dict["xpia_prompt_updater"],
                config=self.update_tasks_config["xpia_prompt_update_task"],
                async_execution=False,
            )
            if "groundedness_prompt_update_task" not in self.update_tasks_config:
                raise ValueError(
                    "Groundedness Prompt update Task configuration not found in the YAML file."
                )
            groundedness_prompt_update_task = Task(
                name="Groundedness Prompt update Task",
                agent=self.agents_dict["groundedness_prompt_updater"],
                config=self.update_tasks_config["groundedness_prompt_update_task"],
                async_execution=False,
            )
            if "jailbreak_prompt_update_task" not in self.update_tasks_config:
                raise ValueError(
                    "Jailbreak Prompt update Task configuration not found in the YAML file."
                )
            jailbreak_prompt_update_task = Task(
                name="Jailbreak Prompt update Task",
                agent=self.agents_dict["jailbreak_prompt_updater"],
                config=self.update_tasks_config["jailbreak_prompt_update_task"],
                async_execution=False,
            )
            if "hc_prompt_update_task" not in self.update_tasks_config:
                raise ValueError(
                    "Harmful Content Prompt update Task configuration not found in the YAML file."
                )
            hc_prompt_update_task = Task(
                name="Harmful Content Prompt update Task",
                agent=self.agents_dict["hc_prompt_updater"],
                config=self.update_tasks_config["hc_prompt_update_task"],
                async_execution=False,
            )
            return {
                "senior_prompt_update_task": senior_prompt_update_task,
                "xpia_prompt_update_task": xpia_prompt_update_task,
                "groundedness_prompt_update_task": groundedness_prompt_update_task,
                "jailbreak_prompt_update_task": jailbreak_prompt_update_task,
                "hc_prompt_update_task": hc_prompt_update_task,
            }
        except TypeError as te:
            raise TypeError(f"TypeError from updaterTasks: {te}") from te
        except ValueError as ve:
            raise ValueError(f"ValueError from updaterTasks: {ve}") from ve
        except AttributeError as ae:
            raise AttributeError(f"AttributeError from updaterTasks: {ae}") from ae
        except IndexError as ie:
            raise IndexError(f"IndexError from updaterTasks: {ie}") from ie
        except MemoryError as me:
            raise MemoryError(f"MemoryError from updaterTasks: {me}") from me
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred while creating updaterTasks: {e}"
            ) from e
