"""
This module provides the `PromptTestcaseGenerator` class, which facilitates the generation of RAI-aligned test cases 
using a generator crew powered by an OpenAI client.

Classes:
    PromptTestcaseGenerator:
        A class that initializes with an OpenAI client and uses a generator crew to create adversarial or compliance-based
        test cases for Responsible AI (RAI) evaluations.
        
        Methods:
            __init__(openaiClient: Optional[OpenAIClient] = None):
                Initializes the PromptTestcaseGenerator with the provided OpenAI client. Raises an error if the client is 
                not provided or if crew creation fails.
            
            generate(prompt: str, verbose: bool = False, max_retries: int = 3) -> dict:
                Generates test cases based on the provided prompt using the generator crew. Returns parsed JSON output from 
                the senior test case generation task, with automatic retry on policy validation error.
"""
import time
import json
import re
import logging
import json
from typing import Optional
import logging,re

# Custom module imports
from ..connections.open_ai import OpenAIClient
from ..crew.testcase_generator_crew import TestcaseGeneratorCrew


class promptTestcaseGenerator:
    def __init__(self, openaiClient: Optional[OpenAIClient] = None):
        """
        Initializes the promptTestcaseGenerator class.
        """
        try:
            if openaiClient is None:
                raise ValueError("OpenAI client is required.")
            self.generator_crew = TestcaseGeneratorCrew(basic_openai_client=openaiClient)
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

    def generate(self, prompt: str, num_cases: int, categories: Optional[list] = None,
             verbose: bool = False, max_retries: int = 3) -> dict:
        """
        Generates test cases using the generator crew based on the given prompt.
        Retries up to `max_retries` times if the Crew output is not valid JSON.
        Returns a parsed JSON-compatible dict or an error message.
        """
    

        for crew_attempt in range(max_retries):  # Outer retry loop for Crew call
            try:
                logging.info(f"Attempt {crew_attempt + 1}/{max_retries}: Initializing generator crew...")
                crew = self.generator_crew.get_testcase_crew(
                    verbose=verbose, num_cases=num_cases, categories=categories
                )
                if not crew:
                    return {"error": "Failed to retrieve the generator crew."}

                logging.info("Kicking off Crew AI generation...")
                result = crew.kickoff(
                    inputs={
                        "prompt": (
                            f"Generate {num_cases} RAI stress test prompts for categories {categories or 'all'}, "
                            f"for the following system prompt, enclosed between <`~`> and <\"~\">.\n\n"
                            f"System Prompt: <`~`>{prompt}<\"~\">"
                        )
                    }
                )

                results = {}
                parse_success = True  # Track if at least one task parsed successfully

                for task_output in result.tasks_output:
                    raw_output = task_output.raw
                    parsed = None

                    # Inner retry loop for JSON parsing
                    for parse_attempt in range(3):
                        try:
                            if isinstance(raw_output, dict):
                                parsed = raw_output
                                break
                            parsed = json.loads(raw_output)
                            break
                        except json.JSONDecodeError as jde:
                            logging.warning(
                                f"Attempt {parse_attempt + 1}/3: JSON decoding error for "
                                f"task '{task_output.name}' — {jde}"
                            )

                            # Try extracting JSON with regex
                            match = re.search(r'\{.*\}', raw_output, re.DOTALL)
                            if match:
                                try:
                                    parsed = json.loads(match.group(0))
                                    break
                                except json.JSONDecodeError:
                                    pass
                            time.sleep(0.5)
                    else:
                        # Inner loop failed for this task
                        logging.error(
                            f"Failed to parse JSON for task '{task_output.name}' after retries.\nRaw output:\n{raw_output}"
                        )
                        parse_success = False
                        results[task_output.name] = {
                            "error": "JSON decoding error after retries",
                            "raw_output": raw_output,
                        }

                    if parsed:
                        results[task_output.name] = parsed

                #  If at least one task succeeded, return results
                if parse_success:
                    return results
                else:
                    logging.warning(
                        f"All tasks failed to return valid JSON on attempt {crew_attempt + 1}. Retrying Crew AI..."
                    )
                    time.sleep(2)

            except Exception as e:
                if "policy validation" in str(e).lower() and crew_attempt < max_retries - 1:
                    logging.warning(f"Policy validation error, retrying... ({e})")
                    time.sleep(1)
                    continue
                return {"error": str(e)}

        #  After max_retries of Crew calls, still failed
        return {
            "error": f"Failed to generate valid JSON after {max_retries} Crew AI attempts.",
            "raw_output": results if 'results' in locals() else None,
        }
