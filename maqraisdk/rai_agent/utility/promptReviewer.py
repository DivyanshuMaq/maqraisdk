"""
This module provides the `PromptReviewer` class, which facilitates the review of prompts for Responsible AI (RAI) compliance using a reviewer crew powered by an OpenAI client.
Classes:
    PromptReviewer:
        A class that initializes with an OpenAI client and uses a reviewer crew to evaluate prompts for RAI compliance.
        Methods:
            __init__(openaiClient: Optional[OpenAIClient] = None):
                Initializes the PromptReviewer with the provided OpenAI client. Raises an error if the client is not provided or if reviewer crew initialization fails.
            review(prompt: str, verbose: bool = False, max_retries: int = 3) -> dict:
                Reviews the given prompt for RAI compliance using the reviewer crew. Returns the output of the senior prompt review task as a JSON-compatible dict, with automatic retry on policy validation error.
"""

# Import necessary libraries
import json
from typing import Optional  # Import typing for type hinting

# Import custom modules
from ..connections.open_ai import OpenAIClient
from ..crew.reviewer_crew import reviewerCrew


class PromptReviewer:
    def __init__(self, openaiClient: Optional[OpenAIClient] = None):
        """
        Initializes the PromptReviewer class.
        """
        try:
            # Check if the openaiClient is provided
            if openaiClient is None:
                raise ValueError("OpenAI client is required.")
            self.reviewer_crew = reviewerCrew(basic_openai_client=openaiClient)
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

    def review(self, prompt: str, verbose: bool = False, max_retries: int = 3) -> dict:
        """
        Reviews a prompt using the reviewer crew, with automatic retry on policy validation error.
        Returns the output as a JSON-compatible dict.
        """
        import time

        for attempt in range(max_retries):
            try:
                reviewer_crew = self.reviewer_crew.get_reviewer_crew(verbose=verbose)
                if not reviewer_crew:
                    return {"error": "Failed to retrieve the reviewer crew."}

                result = reviewer_crew.kickoff(
                    inputs={
                        "prompt": """Evaluate the following prompt, present between <`~`> and <"~"> for RAI compliance. 
Prompt to evaluate: <`~`>"""
                        + prompt
                        + """<"~">"""
                    },
                )
                for task_output in result.tasks_output:
                    if getattr(task_output, "name", None) == "Senior Prompt Review Task":
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