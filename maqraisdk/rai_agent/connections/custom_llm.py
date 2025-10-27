"""
CustomLLM is a wrapper class for initializing and managing a custom Large Language Model (LLM) client using an instance of OpenAIClient.
It provides enhanced error handling and ensures that the LLM client is properly configured with the necessary parameters.
Attributes:
    openai_client (OpenAIClient): The OpenAIClient instance used for API calls.
    llm (LLM): The initialized LLM client.
Methods:
    __init__(openai_client: Optional[OpenAIClient] = None):
        Initializes the CustomLLM instance with the provided OpenAIClient.
        Raises a ValueError if no OpenAIClient is provided.
        Handles various exceptions during initialization, providing descriptive error messages.
"""

# Import necessary libraries and modules
from crewai import LLM 

# Import typing for type hinting
from typing import Optional

from .open_ai import OpenAIClient  # Import OpenAIClient from the openai module


class CustomLLM:
    """
    A custom LLM client that extends OpenAIClient with retry logic and error handling.
    """

    def __init__(self, openai_client: Optional[OpenAIClient] = None):
        """
        Initialize the custom LLM client with an OpenAIClient instance.

        Parameters:
        openai_client (Optional[OpenAIClient]): An instance of OpenAIClient to use for API calls.
        """
        try:
            # Ensure that an OpenAIClient instance is provided
            if openai_client is None:
                raise ValueError("An OpenAIClient instance must be provided.")
            # Assign the provided OpenAIClient to the instance variable
            if not isinstance(openai_client, OpenAIClient):
                raise TypeError(
                    "Expected openai_client to be an instance of OpenAIClient."
                )
            self.openai_client = openai_client
            self.llm = LLM(
                model="azure/" + str(self.openai_client.deployment_name).strip(),
                temperature=self.openai_client.temperature,
                top_p=self.openai_client.top_p,
                base_url=self.openai_client.openai_endpoint,
                api_key=self.openai_client.key,
            )
            if not self.llm:
                raise RuntimeError("Failed to initialize LLM client.")
        except TypeError as te:
            raise TypeError(f"TypeError from CustomLLM: {te}") from te
        except ValueError as ve:
            raise ValueError(f"ValueError from CustomLLM: {ve}") from ve
        except AttributeError as ae:
            raise AttributeError(f"AttributeError from CustomLLM: {ae}") from ae
        except IndexError as ie:
            raise IndexError(f"IndexError from CustomLLM: {ie}") from ie
        except MemoryError as me:
            raise MemoryError(f"MemoryError from CustomLLM: {me}") from me
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred while creating CustomLLM: {e}"
            ) from e
