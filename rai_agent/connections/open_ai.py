"""
OpenAIClient provides an interface for interacting with OpenAI services.
Parameters
----------
    The URL for the OpenAI service. Must be a non-empty string.
    The temperature for the OpenAI model. Must be a positive float. Defaults to 0.1.
    The top_p value for the OpenAI model. Must be a positive float. Defaults to 0.5.
Raises
------
    If any parameter is of an incorrect type.
    If any parameter has an invalid value.
    If an attribute error occurs during initialization.
    If an index error occurs during initialization.
    If a memory error occurs during initialization.
"""

# Importing necessary modules and classes
from typing import Optional, Union  # Type hinting utilities


class OpenAIClient:
    """
    A client for interacting with OpenAI services.

    Parameters:
    -----------
    deployment_name : Optional[str], default=None
        The name of the deployment.
    openai_endpoint : Optional[str], default=None
        The URL for the OpenAI service.
    key : Optional[str], default=None
        The API key for authentication.
    credential : Optional[Union[DefaultAzureCredential, ManagedIdentityCredential]], default=None
        The credential object for authentication.
    temperature : Optional[Union[float, int]], default=None
        The temperature for the OpenAI model.
    top_p : Optional[Union[float, int]], default=None
        The top_p value for the OpenAI model.

    Raises:
    -------
    ValueError
        If any of the provided parameters are invalid.
    TypeError
        If any of the provided parameters are of incorrect type.
    AttributeError
        If there is an attribute error during initialization.
    IndexError
        If there is an index error during initialization.
    MemoryError
        If there is a memory error during initialization.
    RuntimeError
        If an unexpected error occurs during initialization.
    """

    def __init__(
        self,
        deployment_name: Optional[str] = None,
        openai_endpoint: Optional[str] = None,
        key: Optional[str] = None,
        temperature: Optional[Union[float, int]] = None,
        top_p: Optional[Union[float, int]] = None,
    ):
        """
        Initializes the OpenAIClient with the provided parameters.

        Args:
            deployment_name (Optional[str]):
                The name of the deployment. Must be a non-empty string.
                Example: `"openai_deployment_v1"`

            openai_endpoint (Optional[str]):
                The URL for the OpenAI service.
                Either this or `apim_endpoint` must be provided.
                Example: `"https://api.openai.com/"`

            key (Optional[str]):
                The API key for authentication. Required if `apim_endpoint` is used.
                Example: `"my_api_key"`

            temperature (Optional[Union[float, int]]):
                The temperature for the model. Must be a positive float. Defaults to 0.2.
                Example: `0.7`

            top_p (Optional[Union[float, int]]):
                The top_p value for the model. Must be a positive float. Defaults to 0.7.
                Example: `0.9`

        Raises:
            TypeError: If any parameter is of an incorrect type.
            ValueError: If any parameter has an invalid value.
            AttributeError: If an attribute error occurs.
            IndexError: If an index error occurs.
            MemoryError: If a memory error occurs.
            RuntimeError: If an unexpected error occurs.

        Example:
            Here's an example of how to instantiate the `OpenAIClient`:

            client = OpenAIClient(
                deployment_name="openai_deployment_v1",
                openai_endpoint="https://api.openai.com/",
                key="my_api_key",
                temperature=0.7,
                top_p=0.9,
            )

            This creates an `OpenAIClient` instance with the specified parameters, which can be used for making API requests.
        """
        try:
            try:
                self.deployment_name = deployment_name
                self.openai_endpoint = openai_endpoint
                self.key = key
                # self.credential = credential
                self.temperature = temperature if temperature is not None else 0.1
                self.top_p = top_p if top_p is not None else 0.5
            except Exception as e:
                raise ValueError(
                    f"An error occurred while setting the parameters: {e}"
                ) from e
            try:
                if not isinstance(self.deployment_name, str):
                    raise TypeError("`deployment_name` must be a string.")
                if not self.deployment_name:
                    raise ValueError(
                        "The `deployment_name` must be a non-empty string."
                    )
                if self.deployment_name.isspace():
                    raise ValueError("The `deployment_name` contains only whitespace.")
                if not (
                    isinstance(self.openai_endpoint, str)
                    and self.openai_endpoint.strip()
                ):
                    raise ValueError(
                        "The `openai_endpoint` must be a non-empty string."
                    )
                if not isinstance(self.temperature, float):
                    raise TypeError("`temperature` must be a float.")
                if not self.temperature:
                    raise ValueError("The `temperature` must be a non-empty float.")
                if self.temperature < 0:
                    raise ValueError("The `temperature` must be a positive float.")
                if not isinstance(self.top_p, float):
                    raise TypeError("`top_p` must be a float.")
                if not self.top_p:
                    raise ValueError("The `top_p` must be a non-empty float.")
                if self.top_p < 0:
                    raise ValueError("The `top_p` must be a positive float.")
            except Exception as e:
                raise ValueError(
                    f"An error occurred while checking the parameters: {e}"
                ) from e
        except TypeError as te:
            raise TypeError(f"TypeError from OpenAIClient: {te}") from te
        except ValueError as ve:
            raise ValueError(f"ValueError from OpenAIClient: {ve}") from ve
        except AttributeError as ae:
            raise AttributeError(f"AttributeError from OpenAIClient: {ae}") from ae
        except IndexError as ie:
            raise IndexError(f"IndexError from OpenAIClient: {ie}") from ie
        except MemoryError as me:
            raise MemoryError(f"MemoryError from OpenAIClient: {me}") from me
        except Exception as e:
            raise RuntimeError(
                f"An unexpected error occurred while creating OpenAIClient: {e}"
            ) from e
