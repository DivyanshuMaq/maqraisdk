"""
This module defines the `testcaseGeneratorAgents` class, which is responsible for creating and managing various
test case generator agents for evaluating prompts intended for OpenAI models, with a focus on Responsible AI (RAI)
applications. The agents are configured using a YAML file and leverage a custom language model (CustomLLM) for their
operations. The module provides robust error handling for configuration loading and agent instantiation.

Classes:
    testcaseGeneratorAgents: Manages instantiation and retrieval of different test case generator agents,
    each specialized in generating RAI test prompts for dimensions such as XPIA, Groundedness, Jailbreak, and Harmful Content.

Dependencies:
    - yaml: For loading agent configurations from a YAML file.
    - crewai.Agent: For creating agent instances.
    - typing.Optional: For type hinting optional parameters.
    - ..connections.custom_llm.CustomLLM: For integrating a custom language model.
"""


import json

# Import necessary modules
from crewai import Agent 
# Import typing for type hinting
from typing import Optional

from ..connections.custom_llm import CustomLLM
from ..config.testcase_generator_agents_config import TESTCASE_GENERATOR_AGENTS_CONFIG


class testcaseGeneratorAgents:
    """
    This class contains the agents for generating test cases for RAI prompt evaluation.
    """

    def __init__(self, custom_llm: Optional[CustomLLM] = None,num_cases:int=5):
        """
        Initializes the testcaseGeneratorAgents class.
        """
        try:
            # Use Python config instead of YAML file
            self.testcase_config = TESTCASE_GENERATOR_AGENTS_CONFIG.copy()
            
            # Replace {{num_cases}} placeholder with actual value
            config_json = json.dumps(self.testcase_config).replace("{{num_cases}}", str(num_cases))
            self.testcase_config = json.loads(config_json)

            if custom_llm is None:
                raise ValueError("An instance of CustomLLM must be provided.")
            self.llm = custom_llm.llm
        except TypeError as te:
            raise TypeError(f"TypeError from testcaseGeneratorAgents: {te}") from te
        except ValueError as ve:
            raise ValueError(f"ValueError from testcaseGeneratorAgents: {ve}") from ve
        except AttributeError as ae:
            raise AttributeError(f"AttributeError from testcaseGeneratorAgents: {ae}") from ae
        except IndexError as ie:
            raise IndexError(f"IndexError from testcaseGeneratorAgents: {ie}") from ie
        except MemoryError as me:
            raise MemoryError(f"MemoryError from testcaseGeneratorAgents: {me}") from me
        except ImportError as ie:
            raise ImportError(
                f"Configuration import failed. Please ensure the config module exists: {ie}"
            ) from ie
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred while creating testcaseGeneratorAgents: {e}"
            ) from e

    def get_testcase_agents(self, verbose: bool = False):
        """
        Returns a dictionary of test case generator agents.
        """
        try:
            if "senior_testcase_generator_agent" not in self.testcase_config:
                raise ValueError("Senior Test Case Generator configuration not found.")
            senior_testcase_generator_agent = Agent(
                name="Senior Test Case Generator",
                description="Orchestrates RAI test case generation across all risk dimensions.",
                config=self.testcase_config["senior_testcase_generator_agent"],
                verbose=verbose,
                memory=True,
                llm=self.llm,
                allow_delegation=True,
            )
            
            if "xpia_testcase_generator_agent" not in self.testcase_config:
                raise ValueError("XPIA Test Case Generator configuration not found.")
            xpia_testcase_generator_agent = Agent(
                name="XPIA Test Case Generator",
                description="Generates adversarial prompts to test for XPIA compliance in OpenAI prompts.",
                config=self.testcase_config["xpia_testcase_generator_agent"],
                verbose=verbose,
                memory=True,
                llm=self.llm,
                allow_delegation=False,
            )

            if "groundedness_testcase_generator_agent" not in self.testcase_config:
                raise ValueError("Groundedness Test Case Generator configuration not found.")
            
            groundedness_testcase_generator_agent = Agent(
                name="Groundedness Test Case Generator",
                description="Generates prompts to test groundedness in OpenAI model responses.",
                config=self.testcase_config["groundedness_testcase_generator_agent"],
                verbose=verbose,
                memory=True,
                llm=self.llm,
                allow_delegation=False,
            )

            if "jailbreak_testcase_generator_agent" not in self.testcase_config:
                raise ValueError("Jailbreak Test Case Generator configuration not found.")
            jailbreak_testcase_generator_agent = Agent(
                name="Jailbreak Test Case Generator",
                description="Generates jailbreak attempts to test the robustness of prompt compliance.",
                config=self.testcase_config["jailbreak_testcase_generator_agent"],
                verbose=verbose,
                memory=True,
                llm=self.llm,
                allow_delegation=False,
            )

            if "harmful_testcase_generator_agent" not in self.testcase_config:
                raise ValueError("Harmful Content Test Case Generator configuration not found.")
            harmful_testcase_generator_agent = Agent(
                name="Harmful Content Test Case Generator",
                description="Generates prompts that test for potential harmful or biased content generation.",
                config=self.testcase_config["harmful_testcase_generator_agent"],
                verbose=verbose,
                memory=True,
                llm=self.llm,
                allow_delegation=False,
            )

            return {
                "senior_testcase_generator_agent": senior_testcase_generator_agent,
                "xpia_testcase_generator_agent": xpia_testcase_generator_agent,
                "groundedness_testcase_generator_agent": groundedness_testcase_generator_agent,
                "jailbreak_testcase_generator_agent": jailbreak_testcase_generator_agent,
                "harmful_testcase_generator_agent": harmful_testcase_generator_agent,
            }

        except TypeError as te:
            raise TypeError(f"TypeError from testcaseGeneratorAgents: {te}") from te
        except ValueError as ve:
            raise ValueError(f"ValueError from testcaseGeneratorAgents: {ve}") from ve
        except AttributeError as ae:
            raise AttributeError(f"AttributeError from testcaseGeneratorAgents: {ae}") from ae
        except IndexError as ie:
            raise IndexError(f"IndexError from testcaseGeneratorAgents: {ie}") from ie
        except MemoryError as me:
            raise MemoryError(f"MemoryError from testcaseGeneratorAgents: {me}") from me
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred while creating testcaseGeneratorAgents: {e}"
            ) from e
