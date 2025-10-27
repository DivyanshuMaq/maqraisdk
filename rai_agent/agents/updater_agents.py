"""
Module: updater_agents
This module defines the `updaterAgents` class, which is responsible for managing and instantiating various updater agents for reviewing and updating prompts for OpenAI models, with a focus on Responsible AI (RAI) applications.
The agents are configured via a YAML configuration file and utilize a custom language model (CustomLLM) for their operations.
Classes:
    updaterAgents:
        - Initializes with a provided CustomLLM instance and loads agent configurations from a YAML file.
        - Handles exceptions related to configuration loading and agent instantiation.
        - Provides the `get_updater_agents` method to return a dictionary of configured updater agents, each tailored for specific prompt review tasks such as senior prompt updating, XPIA-based updating, groundedness, jailbreak detection, and harmful content detection.
Methods:
    __init__(self, custom_llm: Optional[CustomLLM] = None):
        Initializes the updaterAgents class, loads configuration, and sets up the language model.
    get_updater_agents(self, verbose: bool = False):
        Returns a dictionary of updater agent instances, each configured for a specific aspect of prompt review. Raises descriptive errors if configurations are missing or if instantiation fails.
Raises:
    TypeError: If incorrect types are provided.
    ValueError: If required configuration or parameters are missing.
    AttributeError: If expected attributes are missing.
    IndexError: If configuration indexing fails.
    MemoryError: If memory allocation fails.
    FileNotFoundError: If the configuration file is not found.
    RuntimeError: For any other unexpected errors during initialization or agent creation.
"""



# Import necessary modules
from crewai import Agent 

# Import typing for type hinting
from typing import Optional
from ..connections.custom_llm import CustomLLM
from ..config.updater_agents_config import UPDATER_AGENTS_CONFIG


class updaterAgents:
    """
    This class contains the agents for reviewing prompts for OpenAI models.
    """
    def __init__(self, custom_llm: Optional[CustomLLM] = None):
        """
        Initializes the updaterAgents class.
        """
        try:
            # Use Python config instead of YAML file
            self.updater_config = UPDATER_AGENTS_CONFIG
            if custom_llm is None:
                raise ValueError("An instance of CustomLLM must be provided.")
            self.llm = custom_llm.llm
        except TypeError as te:
            raise TypeError(f"TypeError from updaterAgents: {te}") from te
        except ValueError as ve:
            raise ValueError(f"ValueError from updaterAgents: {ve}") from ve
        except AttributeError as ae:
            raise AttributeError(f"AttributeError from updaterAgents: {ae}") from ae
        except IndexError as ie:
            raise IndexError(f"IndexError from updaterAgents: {ie}") from ie
        except MemoryError as me:
            raise MemoryError(f"MemoryError from updaterAgents: {me}") from me
        except ImportError as ie:
            raise ImportError(
                f"Configuration import failed. Please ensure the config module exists: {ie}"
            ) from ie
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred while creating updaterAgents: {e}"
            ) from e

    def get_updater_agents(self, verbose: bool = False):
        """
        Returns a list of updater agents.
        """
        try:
            if "senior_prompt_updater" not in self.updater_config:
                raise ValueError(
                    "Senior Prompt updater configuration not found in the YAML file."
                )
            senior_prompt_updater = Agent(
                name="Senior Prompt updater",
                description="A Senior Prompt updater for OpenAI Prompts, with a focus on RAI(Responsible AI) applications.",
                config=self.updater_config["senior_prompt_updater"],
                verbose=verbose,
                memory=True,
                llm=self.llm,
                allow_delegation=True,
            )
            if "xpia_prompt_updater" not in self.updater_config:
                raise ValueError(
                    "XPIA Prompt updater configuration not found in the YAML file."
                )
            xpia_prompt_updater = Agent(
                name="XPIA-based Prompt updater",
                description="A XPIA-based Prompt updater for OpenAI Prompts, with a focus on RAI(Responsible AI) applications.",
                config=self.updater_config["xpia_prompt_updater"],
                verbose=verbose,
                memory=True,
                llm=self.llm,
                allow_delegation=False,
            )
            if "groundedness_prompt_updater" not in self.updater_config:
                raise ValueError(
                    "Groundedness Prompt updater configuration not found in the YAML file."
                )
            groundedness_prompt_updater = Agent(
                name="Groundedness-based Prompt updater",
                description="A Groundedness-based Prompt updater for OpenAI Prompts, with a focus on RAI(Responsible AI) applications.",
                config=self.updater_config["groundedness_prompt_updater"],
                verbose=verbose,
                memory=True,
                llm=self.llm,
                allow_delegation=False,
            )
            if "jailbreak_prompt_updater" not in self.updater_config:
                raise ValueError(
                    "Jailbreak Prompt updater configuration not found in the YAML file."
                )
            jailbreak_prompt_updater = Agent(
                name="Jailbreak-based Prompt updater",
                description="A Jailbreak-based Prompt updater for OpenAI Prompts, with a focus on RAI(Responsible AI) applications.",
                config=self.updater_config["jailbreak_prompt_updater"],
                verbose=verbose,
                memory=True,
                llm=self.llm,
                allow_delegation=False,
            )
            if "hc_prompt_updater" not in self.updater_config:
                raise ValueError(
                    "Harmful Content Prompt updater configuration not found in the YAML file."
                )
            hc_prompt_updater = Agent(
                name="HarmfulContent-based Prompt updater",
                description="A HarmfulContent-based Prompt updater for OpenAI Prompts, with a focus on RAI(Responsible AI) applications.",
                config=self.updater_config["hc_prompt_updater"],
                verbose=verbose,
                memory=True,
                llm=self.llm,
                allow_delegation=False,
            )
            return {
                "senior_prompt_updater": senior_prompt_updater,
                "xpia_prompt_updater": xpia_prompt_updater,
                "groundedness_prompt_updater": groundedness_prompt_updater,
                "jailbreak_prompt_updater": jailbreak_prompt_updater,
                "hc_prompt_updater": hc_prompt_updater,
            }
        except TypeError as te:
            raise TypeError(f"TypeError from updaterAgents: {te}") from te
        except ValueError as ve:
            raise ValueError(f"ValueError from updaterAgents: {ve}") from ve
        except AttributeError as ae:
            raise AttributeError(f"AttributeError from updaterAgents: {ae}") from ae
        except IndexError as ie:
            raise IndexError(f"IndexError from updaterAgents: {ie}") from ie
        except MemoryError as me:
            raise MemoryError(f"MemoryError from updaterAgents: {me}") from me
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred while creating updaterAgents: {e}"
            ) from e
