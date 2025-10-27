"""
This module defines the `reviewerAgents` class, which is responsible for creating and managing various reviewer agents
for evaluating prompts intended for OpenAI models, with a focus on Responsible AI (RAI) applications. The agents are
configured using a YAML file and leverage a custom language model (CustomLLM) for their operations. The module provides
robust error handling for configuration loading and agent instantiation.
Classes:
    reviewerAgents: Manages the instantiation and retrieval of different reviewer agents, each specialized in reviewing
    prompts for criteria such as seniority, XPIA, groundedness, jailbreak detection, and harmful content.
Dependencies:
    - yaml: For loading agent configurations from a YAML file.
    - crewai.Agent: For creating agent instances.
    - typing.Optional: For type hinting optional parameters.
    - ..connections.custom_llm.CustomLLM: For integrating a custom language model.
"""


# Import necessary modules
from crewai import Agent  

# Import typing for type hinting
from typing import Optional

from ..connections.custom_llm import CustomLLM
from ..config.reviewer_agents_config import REVIEWER_AGENTS_CONFIG


class reviewerAgents:
    """
    This class contains the agents for reviewing prompts for OpenAI models.
    """
    
    def __init__(self, custom_llm: Optional[CustomLLM] = None):
        """
        Initializes the reviewerAgents class.
        """
        try:
            # Use Python config instead of YAML file
            self.reviewer_config = REVIEWER_AGENTS_CONFIG
            if custom_llm is None:
                raise ValueError("An instance of CustomLLM must be provided.")
            self.llm = custom_llm.llm
        except TypeError as te:
            raise TypeError(f"TypeError from reviewerAgents: {te}") from te
        except ValueError as ve:
            raise ValueError(f"ValueError from reviewerAgents: {ve}") from ve
        except AttributeError as ae:
            raise AttributeError(f"AttributeError from reviewerAgents: {ae}") from ae
        except IndexError as ie:
            raise IndexError(f"IndexError from reviewerAgents: {ie}") from ie
        except MemoryError as me:
            raise MemoryError(f"MemoryError from reviewerAgents: {me}") from me
        except ImportError as ie:
            raise ImportError(
                f"Configuration import failed. Please ensure the config module exists: {ie}"
            ) from ie
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred while creating reviewerAgents: {e}"
            ) from e

    def get_reviewer_agents(self, verbose: bool = False):
        """
        Returns a list of reviewer agents.
        """
        try:
            if "senior_prompt_reviewer" not in self.reviewer_config:
                raise ValueError(
                    "Senior Prompt Reviewer configuration not found in the YAML file."
                )
            senior_prompt_reviewer = Agent(
                name="Senior Prompt Reviewer",
                description="A Senior Prompt Reviewer for OpenAI Prompts, with a focus on RAI(Responsible AI) applications.",
                config=self.reviewer_config["senior_prompt_reviewer"],
                verbose=verbose,
                memory=True,
                llm=self.llm,
                allow_delegation=True,
            )
            if "xpia_prompt_reviewer" not in self.reviewer_config:
                raise ValueError(
                    "XPIA Prompt Reviewer configuration not found in the YAML file."
                )
            xpia_prompt_reviewer = Agent(
                name="XPIA-based Prompt Reviewer",
                description="A XPIA-based Prompt Reviewer for OpenAI Prompts, with a focus on RAI(Responsible AI) applications.",
                config=self.reviewer_config["xpia_prompt_reviewer"],
                verbose=verbose,
                memory=True,
                llm=self.llm,
                allow_delegation=False,
            )
            if "groundedness_prompt_reviewer" not in self.reviewer_config:
                raise ValueError(
                    "Groundedness Prompt Reviewer configuration not found in the YAML file."
                )
            groundedness_prompt_reviewer = Agent(
                name="Groundedness-based Prompt Reviewer",
                description="A Groundedness-based Prompt Reviewer for OpenAI Prompts, with a focus on RAI(Responsible AI) applications.",
                config=self.reviewer_config["groundedness_prompt_reviewer"],
                verbose=verbose,
                memory=True,
                llm=self.llm,
                allow_delegation=False,
            )
            if "jailbreak_prompt_reviewer" not in self.reviewer_config:
                raise ValueError(
                    "Jailbreak Prompt Reviewer configuration not found in the YAML file."
                )
            jailbreak_prompt_reviewer = Agent(
                name="Jailbreak-based Prompt Reviewer",
                description="A Jailbreak-based Prompt Reviewer for OpenAI Prompts, with a focus on RAI(Responsible AI) applications.",
                config=self.reviewer_config["jailbreak_prompt_reviewer"],
                verbose=verbose,
                memory=True,
                llm=self.llm,
                allow_delegation=False,
            )
            if "hc_prompt_reviewer" not in self.reviewer_config:
                raise ValueError(
                    "Harmful Content Prompt Reviewer configuration not found in the YAML file."
                )
            hc_prompt_reviewer = Agent(
                name="HarmfulContent-based Prompt Reviewer",
                description="A HarmfulContent-based Prompt Reviewer for OpenAI Prompts, with a focus on RAI(Responsible AI) applications.",
                config=self.reviewer_config["hc_prompt_reviewer"],
                verbose=verbose,
                memory=True,
                llm=self.llm,
                allow_delegation=False,
            )
            return {
                "senior_prompt_reviewer": senior_prompt_reviewer,
                "xpia_prompt_reviewer": xpia_prompt_reviewer,
                "groundedness_prompt_reviewer": groundedness_prompt_reviewer,
                "jailbreak_prompt_reviewer": jailbreak_prompt_reviewer,
                "hc_prompt_reviewer": hc_prompt_reviewer,
            }
        except TypeError as te:
            raise TypeError(f"TypeError from reviewerAgents: {te}") from te
        except ValueError as ve:
            raise ValueError(f"ValueError from reviewerAgents: {ve}") from ve
        except AttributeError as ae:
            raise AttributeError(f"AttributeError from reviewerAgents: {ae}") from ae
        except IndexError as ie:
            raise IndexError(f"IndexError from reviewerAgents: {ie}") from ie
        except MemoryError as me:
            raise MemoryError(f"MemoryError from reviewerAgents: {me}") from me
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred while creating reviewerAgents: {e}"
            ) from e
