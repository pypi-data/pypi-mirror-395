import os
import asyncio
from typing import Any
from aiohttp import ClientSession
from tenacity import retry, stop_after_attempt, wait_exponential

from simple_evals.simple_evals_types import MessageList, SamplerBase

OPENAI_SYSTEM_MESSAGE_API = "You are a helpful assistant."
OPENAI_SYSTEM_MESSAGE_CHATGPT = (
    "You are ChatGPT, a large language model trained by OpenAI, based on the GPT-4 architecture."
    + "\nKnowledge cutoff: 2023-12\nCurrent date: 2024-04-01"
)


class ChatCompletionSampler(SamplerBase):
    """
    Asynchronous sampler for a chat completion API using aiohttp.
    """

    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        url: str = None,
        system_message: str | None = None,
        temperature: float = 0.5,
        top_p: float = 0.9,
        max_tokens: int = 1024,
        timeout: int = 10,
        max_retries: int = 5,
        api_key: str | None = None,
        max_concurrent_requests: int | None = None,
    ):
        self.url = url if url else "https://integrate.api.nvidia.com/v1/chat/completions"
        if api_key is None:
            self.api_key = None
        else:
            self.api_key = os.environ.get(api_key, "")
        self.model = model
        self.system_message = system_message
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.max_retries = max_retries
        self.semaphore = asyncio.Semaphore(max_concurrent_requests) if max_concurrent_requests is not None else None
        print(f"Using model: {model}, with url: {self.url}, and api_key from environment variable: {api_key}")

    def _pack_message(self, role: str, content: Any):
        return {"role": str(role), "content": content}

    async def _make_request(self, session: ClientSession, payload: dict) -> dict:
        """
        Sends the actual HTTP request to the chat completion API asynchronously.
        """
        headers = {
            "Content-Type": "application/json",
        }

        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        async with session.post(self.url, json=payload, headers=headers, timeout=self.timeout) as response:
            response.raise_for_status()
            return await response.json()

    async def _send_request(self, payload: dict) -> dict:
        """
        Retry logic with exponential backoff for asynchronous requests.
        """
        async def _log_retry(retry_state):
            exception = retry_state.outcome.exception()
            attempt = retry_state.attempt_number
            error_msg = f"{type(exception).__name__}: {str(exception)}" if exception else "Unknown error"
            print(f"Retry attempt {attempt}/{self.max_retries} due to: {error_msg}")

        retrying_logic = retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=2, min=2, max=120),
            after=_log_retry,
        )

        if self.semaphore is not None:
            async with self.semaphore:
                async with ClientSession() as session:
                    return await retrying_logic(self._make_request)(session, payload)
        else:
            async with ClientSession() as session:
                return await retrying_logic(self._make_request)(session, payload)

    async def __call__(self, message_list: MessageList, seed: int | None = None) -> str:
        if self.system_message:
            message_list = [self._pack_message("system", self.system_message)] + message_list
        payload = {
            "model": self.model,
            "messages": message_list,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
        }
        
        if seed is not None:
            payload["seed"] = seed   
        response_data = await self._send_request(payload)
        response_text = response_data["choices"][0]["message"]["content"]
        return response_text or ""


