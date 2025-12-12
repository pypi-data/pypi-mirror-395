import os
import json
import time
import tempfile
import requests
from pathlib import Path
from openai import OpenAI
from openai import OpenAIError, BadRequestError, AuthenticationError
from typing import List, Dict
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

def log_retry_attempt(retry_state):
    if retry_state.outcome is None:
        exception_str = "Unknown error (no outcome)"
    else:
        exception = retry_state.outcome.exception()
        exception_str = (
            f"{type(exception).__name__}: {str(exception)}" 
            if exception 
            else "No exception info"
        )
    
    print(f"\nRetry attempt {retry_state.attempt_number}/{retry_state.retry_object.stop.max_attempt_number} "
          f"due to: {exception_str}", flush=True)
    # Add more detailed exception info if available
    if retry_state.outcome is not None and retry_state.outcome.exception() is not None:
        exception = retry_state.outcome.exception()
        print(f"Detailed error: {repr(exception)}", flush=True)

class OpenAIJudge:
    def __init__(
        self, 
        model: str = "gpt-4", 
        timeout: int = 10, 
        max_retries: int = 16, 
        url: str = None,
        temperature: float = 0.0,
        top_p: float = 0.0001,
        max_tokens: int = 1024,
        api_key: str = None,
    ):
        if timeout < 0:
            raise ValueError("'timeout' must be nonnegative")
        self._timeout = timeout

        if max_retries <= 0:
            raise ValueError("'max_retries' must be positive")
        self._max_retries = max_retries

        if url:
            print(f"Using URL: {url}")
            self.base_url = url
        elif os.environ.get("OPENAI_MODEL_URL"):
            print(f"Using URL from environment variable: OPENAI_MODEL_URL={os.environ.get('OPENAI_MODEL_URL')}")
            self.base_url = os.environ.get("OPENAI_MODEL_URL")
        elif "gpt" in model:
            print("Using default URL: https://prod.api.nvidia.com/llm/v1/azure/. You can provide url in the judge config or set the OPENAI_MODEL_URL environment variable to override this.")
            self.base_url = "https://prod.api.nvidia.com/llm/v1/azure/"
        else:
            raise ValueError(f"Endpoint for model {model} was not provided. Please provide url in the judge config or set the OPENAI_MODEL_URL environment variable.")

        if api_key:
            print(f"Using API key from environment variable {api_key}")
            if os.environ.get(api_key):
                self.api_key = os.environ.get(api_key)
            else:
                raise ValueError(f"The environment variable {api_key} was not found.")
        elif os.environ.get("OPENAI_API_KEY"):
            print(f"Using API key from environment variable: OPENAI_API_KEY")
            self.api_key = os.environ.get("OPENAI_API_KEY")
        else:
            print("No API key was provided.")
            #NOTE(edobrowolska): If api_key is a non-empty string, OpenAI raises an AuthenticationError and we can generate a token with the get_oauth_token method.
            # When api_key is None, we get an OpenAIError, and if it is an empty string, we get an APIConnectionError instead (regardless of URL)
            self.api_key = "dummy_key"

        self.gateway_token = None # could be populated by api_key
        self.expires_in = None # could be populated by api_key
        self._client = OpenAI(base_url=self.base_url, api_key=self.api_key)

        self._model = model
        if "azure-" in self._model:
            self._model = self._model[6:]

        # Store additional parameters
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens


    def single_completion(
        self, 
        conv: List[Dict[str, str]], 
        temperature: float = 0.0, 
        max_tokens: int = 1024, 
        top_p: float = 0.0001
    ) -> str:
        @retry(
            wait=wait_exponential(multiplier=1, min=self._timeout, max=self._timeout * 10),
            stop=stop_after_attempt(self._max_retries),
            retry=retry_if_exception_type(OpenAIError),
            before_sleep=log_retry_attempt,
        )
        def _completion_with_retry():
            try:
                response = self._client.chat.completions.create(
                    model=self._model,
                    messages=conv,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    stream=False,
                )
                return response.choices[0].message.content
            except AuthenticationError as e:
                if os.environ.get("OPENAI_CLIENT_ID") and os.environ.get("OPENAI_CLIENT_SECRET"):
                    print(f"Authentication error: {str(e)}")
                    print("Generating a new token with the provided OPENAI_CLIENT_ID and OPENAI_CLIENT_SECRET environment variables")
                    self.api_key = self.get_oauth_token(force=True)
                    self._client = OpenAI(base_url=self.base_url, api_key=self.api_key)
                    response = self._client.chat.completions.create(
                        model=self._model,
                        messages=conv,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        top_p=top_p,
                        stream=False,
                    )
                    return response.choices[0].message.content
                else:
                    print("Please provide the valid token in the OPENAI_API_KEY environment variable, or the OPENAI_CLIENT_ID and OPENAI_CLIENT_SECRET environment variables to generate a token.")
                    raise
            except (BadRequestError, KeyError) as e:
                print(f"Bad request error: {type(e).__name__}: {str(e)}")
                raise  # Re-raise without retry
            except OpenAIError as e:
                print(f"OpenAI error: {type(e).__name__}: {str(e)}")
                raise  # Re-raise to trigger retry

        return _completion_with_retry()

    async def __call__(self, messages: List[Dict[str, str]]) -> str:
        """Make the class callable, forwarding to chat_completions."""
        results = self.single_completion(
            messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p
        )
        return results

    def get_oauth_token(self, force: bool = False):
        p_token_url = os.environ.get("OPENAI_TOKEN_URL", "https://prod.api.nvidia.com/oauth/api/v1/ssa/default/token")
        p_client_id = os.environ.get("OPENAI_CLIENT_ID")
        p_client_secret = os.environ.get("OPENAI_CLIENT_SECRET")
        p_scope = os.environ.get("OPENAI_SCOPE", "azureopenai-readwrite")


        try:
            # Check if the token is cached
            if not force and self.gateway_token and self.expires_in:
                # Check if the token is expired
                if time.time() > self.expires_in:
                    # Token expired, force refresh
                    return self.get_oauth_token(force=True)
            else:
                # Get a new token from the OAuth server
                response = requests.post(
                    p_token_url,
                    data={
                        "grant_type": "client_credentials",
                        "client_id": p_client_id,
                        "client_secret": p_client_secret,
                        "scope": p_scope,
                    },
                    timeout=3600,
                )
                response.raise_for_status()
                self.gateway_token = response.json()
                self.expires_in = time.time() + self.gateway_token["expires_in"]
        except Exception as e:
            err = f"Error occurred while getting OAuth token: {e}"
            raise RuntimeError(err) from e

        return self.gateway_token["access_token"]

