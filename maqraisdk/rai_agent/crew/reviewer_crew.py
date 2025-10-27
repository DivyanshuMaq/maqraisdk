"""
Module: reviewer_crew
This module defines the `reviewerCrew` class, which is responsible for creating and managing a crew of agents for reviewing prompts intended for OpenAI models. The crew leverages custom LLM clients and is composed of specialized reviewer agents, each tasked with a specific aspect of prompt review, such as groundedness, jailbreak detection, and harmful content detection.
Classes:
    reviewerCrew:
        - Initializes with an OpenAI client and sets up a custom LLM.
        - Provides the `get_reviewer_crew` method to instantiate and return a configured Crew object with reviewer agents and tasks.
        - Handles various initialization and runtime errors with descriptive exception messages.
Methods:
    __init__(self, basic_openai_client: Optional[OpenAIClient] = None):
        Initializes the reviewerCrew instance with a provided OpenAI client, setting up the custom LLM for agent use.
    get_reviewer_crew(self, verbose: bool = False):
        Constructs and returns a Crew instance populated with reviewer agents and their corresponding tasks, configured for sequential processing and caching.
Dependencies:
    - crewai.Crew, crewai.Process
    - OpenAIClient, CustomLLM
    - reviewerAgents, reviewerTasks
Raises:
    - ValueError: If required clients or agents/tasks are missing.
    - TypeError, AttributeError, IndexError, MemoryError: For specific initialization errors.
    - RuntimeError: For unexpected errors during crew creation.
"""

# Import necessary libraries and modules
from crewai import Crew, Process  

# Import typing for type hinting
from typing import Optional

# Import custom modules for agents and tasks
from ..agents.reviewer_agents import reviewerAgents
from ..connections.open_ai import OpenAIClient
from ..connections.custom_llm import CustomLLM
from ..tasks.reviewer_tasks import reviewerTasks
class reviewerCrew:
    """
    This class contains the crew for reviewing prompts for OpenAI models.
    """

    def __init__(self, basic_openai_client: Optional[OpenAIClient] = None):
        """
        Initializes the reviewerCrew class.
        """
        try:
            # Check if the basic_openai_object is provided
            if basic_openai_client is None:
                raise ValueError("OpenAI client is required.")
            self.llm = CustomLLM(basic_openai_client)
            if not self.llm:
                raise RuntimeError("Failed to initialize LLM client.")
        except TypeError as te:
            raise TypeError(f"TypeError from reviewerCrew: {te}") from te
        except ValueError as ve:
            raise ValueError(f"ValueError from reviewerCrew: {ve}") from ve
        except AttributeError as ae:
            raise AttributeError(f"AttributeError from reviewerCrew: {ae}") from ae
        except IndexError as ie:
            raise IndexError(f"IndexError from reviewerCrew: {ie}") from ie
        except MemoryError as me:
            raise MemoryError(f"MemoryError from reviewerCrew: {me}") from me
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred while creating reviewerCrew: {e}"
            ) from e

    def get_reviewer_crew(self, verbose: bool = False):
        """
        Returns a Crew instance with reviewer agents.
        """
        try:
            # Initialize the reviewer agents
            reviewer_agents = reviewerAgents(custom_llm=self.llm)
            reviewer_agents_dict = reviewer_agents.get_reviewer_agents(verbose=verbose)
            if not reviewer_agents_dict:
                raise ValueError(
                    "No reviewer agents found. Please check the configuration."
                )
            # Initialize the reviewer tasks
            reviewer_tasks = reviewerTasks(agents_dict=reviewer_agents_dict)
            reviewer_tasks_dict = reviewer_tasks.get_reviewer_tasks()
            if not reviewer_tasks_dict:
                raise ValueError(
                    "No reviewer tasks found. Please check the configuration."
                )
            # Create the crew with the LLM
            crew = Crew(
                name="RAI Reviewer Crew",
                description="A crew of RAI agents for reviewing prompts for OpenAI models.",
                agents=[
                    reviewer_agents_dict["senior_prompt_reviewer"],
                    reviewer_agents_dict["xpia_prompt_reviewer"],
                    reviewer_agents_dict["groundedness_prompt_reviewer"],
                    reviewer_agents_dict["jailbreak_prompt_reviewer"],
                    reviewer_agents_dict["hc_prompt_reviewer"],
                ],
                tasks=[
                    reviewer_tasks_dict["senior_prompt_review_task"],
                    reviewer_tasks_dict["xpia_prompt_review_task"],
                    reviewer_tasks_dict["groundedness_prompt_review_task"],
                    reviewer_tasks_dict["jailbreak_prompt_review_task"],
                    reviewer_tasks_dict["hc_prompt_review_task"],
                ],
                process=Process.sequential,  # Sequential process for task execution
                cache=True,  # Enable caching for performance
                max_rpm=50,  # Set maximum requests per minute
                share_crew=True,  # Allow sharing of the crew
            )
            return crew
        except TypeError as te:
            raise TypeError(f"TypeError from reviewerCrew: {te}") from te
        except ValueError as ve:
            raise ValueError(f"ValueError from reviewerCrew: {ve}") from ve
        except AttributeError as ae:
            raise AttributeError(f"AttributeError from reviewerCrew: {ae}") from ae
        except IndexError as ie:
            raise IndexError(f"IndexError from reviewerCrew: {ie}") from ie
        except MemoryError as me:
            raise MemoryError(f"MemoryError from reviewerCrew: {me}") from me
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred while creating reviewerCrew: {e}"
            ) from e
