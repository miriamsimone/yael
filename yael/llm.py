"""Ollama LLM client wrapper."""
from ollama import Client
from typing import Generator


class LLM:
    """Wrapper for Ollama chat completions."""

    def __init__(self, model: str = "llama3.1:8b", base_url: str = "http://localhost:11434"):
        self.model = model
        self.client = Client(host=base_url)

    def chat(self, messages: list[dict], stream: bool = True) -> Generator[str, None, None] | str:
        """Send chat completion request.

        Args:
            messages: List of {"role": "user"|"assistant"|"system", "content": "..."}
            stream: Whether to stream the response

        Yields/Returns:
            Token strings if streaming, else complete response
        """
        if stream:
            response = self.client.chat(
                model=self.model,
                messages=messages,
                stream=True,
            )
            for chunk in response:
                if chunk.get("message", {}).get("content"):
                    yield chunk["message"]["content"]
        else:
            response = self.client.chat(
                model=self.model,
                messages=messages,
                stream=False,
            )
            return response["message"]["content"]

    def is_available(self) -> bool:
        """Check if Ollama is running and model is available."""
        try:
            models = self.client.list()
            model_prefix = self.model.split(":")[0]
            # models.models is a list of Model objects with .model attribute
            return any(m.model.startswith(model_prefix) for m in models.models)
        except Exception:
            return False
