"""
Module: promptUpdater
This module provides the `PromptUpdater` class, which is responsible for updating prompts to ensure Responsible AI (RAI) compliance using feedback and an OpenAI client. The class leverages an updater crew to review and update prompts based on provided feedback.
Classes:
    PromptUpdater:
        A class to update prompts for RAI compliance using an OpenAI client and feedback.
        Methods:
            __init__(openaiClient: Optional[OpenAIClient] = None):
                Initializes the PromptUpdater with a provided OpenAI client. Raises an error if the client is not provided.
            update(prompt: str, feedback: dict, verbose: bool = False, max_retries: int = 3) -> dict:
                Updates the given prompt using the updater crew and provided feedback. Returns the updated prompt as a JSON-compatible dict, with automatic retry on policy validation error.
"""

# Import necessary libraries
import json
from typing import Optional  # Import typing for type hinting

# Import custom modules
from ..connections.open_ai import OpenAIClient
from ..crew.updater_crew import updaterCrew


class PromptUpdater:
    def __init__(self, openaiClient: Optional[OpenAIClient] = None):
        """
        Initializes the PromptUpdater class.
        """
        try:
            # Check if the openaiClient is provided
            if openaiClient is None:
                raise ValueError("OpenAI client is required.")
            self.updater_crew = updaterCrew(basic_openai_client=openaiClient)
        except TypeError as te:
            raise TypeError(f"TypeError from PromptUpdater: {te}") from te
        except ValueError as ve:
            raise ValueError(f"ValueError from PromptUpdater: {ve}") from ve
        except AttributeError as ae:
            raise AttributeError(f"AttributeError from PromptUpdater: {ae}") from ae
        except IndexError as ie:
            raise IndexError(f"IndexError from PromptUpdater: {ie}") from ie
        except MemoryError as me:
            raise MemoryError(f"MemoryError from PromptUpdater: {me}") from me
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred while creating PromptUpdater: {e}"
            ) from e

    def update(self, prompt: str, feedback: dict, verbose: bool = False, max_retries: int = 3) -> dict:
        """
        Updates a prompt using the updater crew and provided feedback, with automatic retry on policy validation error.
        Returns the output as a JSON-compatible dict.
        """
        import time

        for attempt in range(max_retries):
            try:
                # Get the updater crew
                updater_crew = self.updater_crew.get_updater_crew(verbose=verbose)
                if not updater_crew:
                    return {"error": "Failed to retrieve the updater crew."}

                result = updater_crew.kickoff(
                    inputs={
                        "prompt": """Update the following prompt, present between <`~`> and <"~"> for RAI compliance. 
Prompt_to_update: <`~`>"""
                        + prompt
                        + """<"~">""",
                        "feedback": """Utilize the following feedback, present between <'~'> and <,~,> for updating the Prompt_to_update.
Prompt_Reviewer_feedback: <'~'>"""
                        + str(feedback)
                        + """<,~,>""",
                    },
                )
                # Get the output of senior_prompt_review_task
                for task_output in result.tasks_output:
                    if getattr(task_output, "name", None) == "Senior Prompt update Task":
                        try:
                            raw_result = task_output.raw
                            output = json.loads(raw_result)
                            return output
                        except json.JSONDecodeError as jde:
                            return {"error": f"JSON decoding error: {jde}", "raw": task_output.raw}
                return {"error": "Prompt Review output not found in the review."}
            except Exception as e:
                if "policy validation" in str(e).lower() and attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                return {"error": str(e)}