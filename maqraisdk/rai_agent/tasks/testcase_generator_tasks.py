"""
Module: testcase_generator_tasks
This module defines the `testcaseGeneratorTasks` class, which manages and instantiates test case generation tasks
for OpenAI models using the CrewAI framework. It loads configurations from a YAML file and validates the presence
of required generator agents. It provides a method to retrieve a dictionary of initialized test case generator tasks:
    * Senior Test Case Generator
    * XPIA Test Case Generator
    * Groundedness Test Case Generator
    * Jailbreak Test Case Generator
    * Harmful Content Test Case Generator
"""

# Standard library imports
import json
from typing import Optional

# Third-party imports
from crewai import Task 
from ..config.testcase_generator_tasks_config import TESTCASE_GENERATOR_TASKS_CONFIG

class testcaseGeneratorTasks:
    """
    Handles test case generation tasks using CrewAI.
    """

    def __init__(self, agents_dict: Optional[dict] = None,num_cases: int=5, categories: Optional[list] = None):
        """
        Initialize the testcaseGeneratorTasks class and validate agents.
        """
        #  Always define attributes up front
        self.generator_tasks_config = {}
        self.generator_tasks_config_path = None
        self.agents_dict = agents_dict
        self.categories = categories or [ 
            "senior",
            "xpia",
            "groundedness",
            "jailbreak",
            "harmful"
        ]
        try:
            # Use Python config instead of YAML file
            config_copy = TESTCASE_GENERATOR_TASKS_CONFIG.copy()
            json_content = json.dumps(config_copy).replace("{{num_cases}}", str(num_cases))
            self.generator_tasks_config = json.loads(json_content)

            if not self.agents_dict:
                raise ValueError("No agents dictionary provided. Please provide test case generator agents.")

            category_agent_map = {
                "senior": "senior_testcase_generator_agent",
                "xpia": "xpia_testcase_generator_agent",
                "groundedness": "groundedness_testcase_generator_agent",
                "jailbreak": "jailbreak_testcase_generator_agent",
                "harmful": "harmful_testcase_generator_agent"
            }

            # Only check required agents for chosen categories
            for cat in self.categories:
                agent_key = category_agent_map.get(cat)
                if not agent_key or self.agents_dict.get(agent_key) is None:
                    raise ValueError(f"Agent for category '{cat}' not found in agents_dict.")
        except FileNotFoundError as fnf:
            raise FileNotFoundError(
                f"Configuration file not found: {self.generator_tasks_config_path}. Please ensure it exists."
            ) from fnf
        except json.JSONDecodeError as je:
            raise RuntimeError(f"JSON parsing error in configuration file: {je}") from je
        except ValueError as ve:
            raise ValueError(f"ValueError from testcaseGeneratorTasks: {ve}") from ve
        except Exception as e:
            raise RuntimeError(f"Unexpected error during initialization of testcaseGeneratorTasks: {e}") from e

    def get_testcase_generator_tasks(self,categories=None):
        """
        Returns a dictionary of initialized test case generator tasks.
        """
        try:
            category_task_map = {
                "senior": ("senior_testcase_generator_task", "Senior Test Case Generator Task"),
                "xpia": ("xpia_testcase_generator_task", "XPIA Test Case Generator Task"),
                "groundedness": ("groundedness_testcase_generator_task", "Groundedness Test Case Generator Task"),
                "jailbreak": ("jailbreak_testcase_generator_task", "Jailbreak Test Case Generator Task"),
                "harmful": ("harmful_testcase_generator_task", "Harmful Content Test Case Generator Task")
            }

            tasks_dict = {}
            selected_categories = categories or ["senior", "xpia", "groundedness", "jailbreak", "harmful"]

            for cat in selected_categories:
                task_key, task_name = category_task_map[cat]
                if task_key not in self.generator_tasks_config:
                    raise ValueError(f"Missing task configuration for: {task_key} in YAML file.")

                tasks_dict[task_key] = Task(
                    name=task_name,
                    agent=self.agents_dict[f"{cat}_testcase_generator_agent"],
                    config=self.generator_tasks_config[task_key],
                    async_execution=False,
                )

            return tasks_dict
        except KeyError as ke:
            raise KeyError(f"Missing agent or configuration key: {ke}") from ke
        except ValueError as ve:
            raise ValueError(f"ValueError from get_testcase_generator_tasks: {ve}") from ve
        except TypeError as te:
            raise TypeError(f"TypeError in get_testcase_generator_tasks: {te}") from te
        except AttributeError as ae:
            raise AttributeError(f"AttributeError in get_testcase_generator_tasks: {ae}") from ae
        except Exception as e:
            raise RuntimeError(f"Unexpected error in get_testcase_generator_tasks: {e}") from e
