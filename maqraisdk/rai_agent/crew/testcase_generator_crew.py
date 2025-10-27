"""
Module: testcase_generator_crew
This module defines the `TestcaseGeneratorCrew` class, which is responsible for creating and managing a crew of agents
for generating adversarial test cases across Responsible AI (RAI) dimensions including XPIA, Groundedness, Jailbreak, and Harmful Content.

Classes:
    TestcaseGeneratorCrew:
        - Initializes with an OpenAI client and sets up a custom LLM.
        - Provides the `get_testcase_crew` method to instantiate and return a configured Crew object.

Dependencies:
    - crewai.Crew, crewai.Process
    - OpenAIClient, CustomLLM
    - testcaseCreatorAgents, testcaseCreatorTasks
Raises:
    - ValueError, TypeError, AttributeError, IndexError, MemoryError: For specific initialization and runtime errors.
    - RuntimeError: For any unexpected error.
"""

from crewai import Crew, Process 
from typing import Optional

from ..connections.open_ai import OpenAIClient
from ..connections.custom_llm import CustomLLM
from ..agents.testcase_generator_agents import testcaseGeneratorAgents
from ..tasks.testcase_generator_tasks import testcaseGeneratorTasks

class TestcaseGeneratorCrew:
    """
    This class defines and manages the crew responsible for generating RAI test cases.
    """

    def __init__(self, basic_openai_client: Optional[OpenAIClient] = None):
        """
        Initializes the TestcaseGeneratorCrew with a custom LLM using the provided OpenAI client.
        """
        try:
            if basic_openai_client is None:
                raise ValueError("OpenAI client is required to initialize the test case generator crew.")
            self.llm = CustomLLM(basic_openai_client)
            if not self.llm:
                raise RuntimeError("Failed to initialize custom LLM.")
        except TypeError as te:
            raise TypeError(f"TypeError from TestcaseGeneratorCrew: {te}") from te
        except ValueError as ve:
            raise ValueError(f"ValueError from TestcaseGeneratorCrew: {ve}") from ve
        except AttributeError as ae:
            raise AttributeError(f"AttributeError from TestcaseGeneratorCrew: {ae}") from ae
        except IndexError as ie:
            raise IndexError(f"IndexError from TestcaseGeneratorCrew: {ie}") from ie
        except MemoryError as me:
            raise MemoryError(f"MemoryError from TestcaseGeneratorCrew: {me}") from me
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred while initializing TestcaseGeneratorCrew: {e}"
            ) from e

    def get_testcase_crew(self, verbose: bool = False,num_cases: int=5,categories: Optional[list] = None):
        """
        Returns a Crew instance populated with test case generator agents and their tasks.
        """
        try:
            # Instantiate agents
            agents_ts = testcaseGeneratorAgents(custom_llm=self.llm,num_cases=num_cases)
            agents_dict = agents_ts.get_testcase_agents(verbose=verbose)
            if not agents_dict:
                raise ValueError("No test case generator agents found. Check configuration.")

            # Instantiate tasks
            tasks = testcaseGeneratorTasks(agents_dict=agents_dict,num_cases=num_cases)
            tasks_dict = tasks.get_testcase_generator_tasks()
            if not tasks_dict:
                raise ValueError("No test case generator tasks found. Check configuration.")
            category_map = {
                "senior": ("senior_testcase_generator_agent", "senior_testcase_generator_task"),
                "xpia": ("xpia_testcase_generator_agent", "xpia_testcase_generator_task"),
                "groundedness": ("groundedness_testcase_generator_agent", "groundedness_testcase_generator_task"),
                "jailbreak": ("jailbreak_testcase_generator_agent", "jailbreak_testcase_generator_task"),
                "harmful": ("harmful_testcase_generator_agent", "harmful_testcase_generator_task"),
            }

        # If no categories provided → take all
            selected_categories = categories or list(category_map.keys())

            selected_agents = []
            selected_tasks = []
            for cat in selected_categories:
                if cat not in category_map:
                    raise ValueError(f"Invalid category: {cat}")
                agent_key, task_key = category_map[cat]
                if agent_key not in agents_dict:
                    raise ValueError(f"Missing agent: {agent_key}")
                if task_key not in tasks_dict:
                    raise ValueError(f"Missing task: {task_key}")

                selected_agents.append(agents_dict[agent_key])
                selected_tasks.append(tasks_dict[task_key])
            # Create and return the crew
            return Crew(
                name="RAI Test Case Generator Crew",
                description="A crew of agents generating adversarial test prompts to validate Responsible AI dimensions.",
                agents=selected_agents,
                tasks=selected_tasks,
                process=Process.sequential,
                cache=True,
                max_rpm=50,
                share_crew=True,
            )
        except TypeError as te:
            raise TypeError(f"TypeError from TestcaseGeneratorCrew: {te}") from te
        except ValueError as ve:
            raise ValueError(f"ValueError from TestcaseGeneratorCrew: {ve}") from ve
        except AttributeError as ae:
            raise AttributeError(f"AttributeError from TestcaseGeneratorCrew: {ae}") from ae
        except IndexError as ie:
            raise IndexError(f"IndexError from TestcaseGeneratorCrew: {ie}") from ie
        except MemoryError as me:
            raise MemoryError(f"MemoryError from TestcaseGeneratorCrew: {me}") from me
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred while creating TestcaseGeneratorCrew: {e}"
            ) from e
