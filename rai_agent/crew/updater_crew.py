"""
Module: updater_crew
This module defines the `updaterCrew` class, which is responsible for managing a crew of agents dedicated to updating prompts for OpenAI models. The crew leverages custom LLM clients and a set of specialized agents and tasks to review and update prompts in a structured, sequential manner.
Classes:
    updaterCrew:
        - Initializes with a required OpenAI client and sets up a custom LLM.
        - Provides the `get_updater_crew` method to instantiate and return a configured Crew object, which includes:
            - Multiple updater agents (senior, xpia, groundedness, jailbreak, and hc prompt updaters).
            - Corresponding updater tasks for each agent.
            - Sequential processing, caching, and rate limiting.
        - Handles various initialization and runtime errors with descriptive exceptions.
Dependencies:
    - crewai.Crew, crewai.Process
    - Custom modules for agents, LLM connections, and tasks
    - typing.Optional
Usage:
    Instantiate `updaterCrew` with a valid OpenAI client and call `get_updater_crew()` to obtain a ready-to-use Crew instance for prompt updating workflows.
"""

# Import necessary modules
from crewai import Crew, Process  
# Import typing for type hinting
from typing import Optional

# Import custom modules
from ..agents.updater_agents import updaterAgents
from ..connections.open_ai import OpenAIClient
from ..connections.custom_llm import CustomLLM
from ..tasks.updater_tasks import updaterTasks

class updaterCrew:
    """
    This class contains the crew for updating prompts for OpenAI models.
    """

    def __init__(self, basic_openai_client: Optional[OpenAIClient] = None):
        """
        Initializes the UpdaterCrew class.
        """
        try:
            # Check if the basic_openai_object is provided
            if basic_openai_client is None:
                raise ValueError("OpenAI client is required.")
            self.llm = CustomLLM(basic_openai_client)
            if not self.llm:
                raise RuntimeError("Failed to initialize LLM client.")
        except TypeError as te:
            raise TypeError(f"TypeError from UpdaterCrew: {te}") from te
        except ValueError as ve:
            raise ValueError(f"ValueError from UpdaterCrew: {ve}") from ve
        except AttributeError as ae:
            raise AttributeError(f"AttributeError from UpdaterCrew: {ae}") from ae
        except IndexError as ie:
            raise IndexError(f"IndexError from UpdaterCrew: {ie}") from ie
        except MemoryError as me:
            raise MemoryError(f"MemoryError from UpdaterCrew: {me}") from me
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred while creating UpdaterCrew: {e}"
            ) from e

    def get_updater_crew(self, verbose: bool = False):
        """
        Returns a Crew instance with updater agents.
        """
        try:
            # Initialize the updater agents
            updater_agents = updaterAgents(custom_llm=self.llm)
            updater_agents_dict = updater_agents.get_updater_agents(verbose=verbose)
            if not updater_agents_dict:
                raise ValueError(
                    "No updater agents found. Please check the configuration."
                )
            # Initialize the updater tasks
            updater_tasks = updaterTasks(agents_dict=updater_agents_dict)
            updater_tasks_dict = updater_tasks.get_updater_tasks()
            # Create the crew with the LLM
            crew = Crew(
                name="RAI updater Crew",
                description="A crew of RAI agents for reviewing prompts for OpenAI models.",
                agents=[
                    updater_agents_dict["senior_prompt_updater"],
                    updater_agents_dict["xpia_prompt_updater"],
                    updater_agents_dict["groundedness_prompt_updater"],
                    updater_agents_dict["jailbreak_prompt_updater"],
                    updater_agents_dict["hc_prompt_updater"],
                ],
                tasks=[
                    updater_tasks_dict["senior_prompt_update_task"],
                    updater_tasks_dict["xpia_prompt_update_task"],
                    updater_tasks_dict["groundedness_prompt_update_task"],
                    updater_tasks_dict["jailbreak_prompt_update_task"],
                    updater_tasks_dict["hc_prompt_update_task"],
                ],
                process=Process.sequential,  # Sequential process for task execution
                cache=True,  # Enable caching for performance
                max_rpm=50,  # Set maximum requests per minute
                share_crew=True,  # Allow sharing of the crew
            )
            return crew
        except TypeError as te:
            raise TypeError(f"TypeError from UpdaterCrew: {te}") from te
        except ValueError as ve:
            raise ValueError(f"ValueError from UpdaterCrew: {ve}") from ve
        except AttributeError as ae:
            raise AttributeError(f"AttributeError from UpdaterCrew: {ae}") from ae
        except IndexError as ie:
            raise IndexError(f"IndexError from UpdaterCrew: {ie}") from ie
        except MemoryError as me:
            raise MemoryError(f"MemoryError from UpdaterCrew: {me}") from me
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred while creating UpdaterCrew: {e}"
            ) from e
