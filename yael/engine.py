"""Core chat engine orchestrating LLM and graph memory."""
import asyncio
from typing import AsyncGenerator
from .llm import LLM
from .graph import GraphMemory
from .config import load_config, get_openai_key
from .profile import build_user_profile, inject_profile


class ChatEngine:
    """Orchestrates conversation with memory-augmented context."""

    def __init__(self):
        self.config = load_config()

        # Initialize LLM
        self.llm = LLM(
            model=self.config["llm"]["model"],
            base_url=self.config["llm"]["base_url"],
        )

        # Initialize graph memory (will be set up async)
        self.graph = GraphMemory(
            neo4j_uri=self.config["graph"]["uri"],
            neo4j_user=self.config["graph"]["user"],
            neo4j_password=self.config["graph"]["password"],
            neo4j_database=self.config["graph"]["database"],
            openai_api_key=get_openai_key(),
            embedding_model=self.config["embeddings"]["model"],
        )

        # Conversation history (current session)
        self.history: list[dict] = []
        self.base_system_prompt = self.config["system_prompt"]
        self.system_prompt = self.base_system_prompt  # Will be enriched with profile
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize graph schema and build user profile."""
        if not self._initialized:
            await self.graph.initialize()

            # Build user profile from graph
            profile = await build_user_profile(self.graph, max_per_query=3)

            # Inject profile into system prompt
            self.system_prompt = inject_profile(self.base_system_prompt, profile)

            self._initialized = True

    async def chat(self, user_message: str) -> AsyncGenerator[str, None]:
        """Process user message and generate response.

        1. Search graph for relevant context
        2. Build prompt with context + history
        3. Stream response from LLM
        4. Store exchange in graph
        """
        # Ensure initialized
        if not self._initialized:
            await self.initialize()

        # 1. Get relevant context from graph
        context = await self.graph.get_context_string(user_message)

        # 2. Build messages
        messages = [{"role": "system", "content": self.system_prompt}]

        if context:
            messages.append({
                "role": "system",
                "content": context,
            })

        # Add conversation history
        messages.extend(self.history)

        # Add current message
        messages.append({"role": "user", "content": user_message})

        # 3. Stream response
        full_response = []
        for token in self.llm.chat(messages, stream=True):
            full_response.append(token)
            yield token

        response_text = "".join(full_response)

        # 4. Update history
        self.history.append({"role": "user", "content": user_message})
        self.history.append({"role": "assistant", "content": response_text})

        # 5. Store in graph (background task - don't block prompt)
        episode = f"User: {user_message}\nAssistant: {response_text}"
        asyncio.create_task(self.graph.add_episode(episode))

    def update_system_prompt(self, new_prompt: str) -> None:
        """Update the system prompt."""
        self.system_prompt = new_prompt
        self.config["system_prompt"] = new_prompt

    def clear_history(self) -> None:
        """Clear current session history."""
        self.history = []

    async def close(self) -> None:
        """Clean up resources."""
        # Wait a moment for any pending graph writes to complete
        await asyncio.sleep(0.5)
        await self.graph.close()
