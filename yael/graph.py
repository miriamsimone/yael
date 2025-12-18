"""Graphiti graph memory wrapper."""
import os
from datetime import datetime
from typing import Any
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType


class GraphMemory:
    """Wrapper for Graphiti knowledge graph."""

    def __init__(
        self,
        neo4j_uri: str,
        neo4j_user: str,
        neo4j_password: str,
        neo4j_database: str,
        openai_api_key: str,
        embedding_model: str = "text-embedding-3-small",
    ):
        # Set OpenAI API key in environment for Graphiti to use
        os.environ["OPENAI_API_KEY"] = openai_api_key

        # Initialize Graphiti (will use OpenAI clients by default via env var)
        self.graphiti = Graphiti(
            neo4j_uri,
            neo4j_user,
            neo4j_password,
        )

    async def initialize(self) -> None:
        """Initialize the graph schema."""
        await self.graphiti.build_indices_and_constraints()

    async def add_episode(
        self,
        content: str,
        source: str = "conversation",
        timestamp: datetime | None = None,
    ) -> None:
        """Add a conversation episode to the graph.

        This extracts entities and relationships automatically.
        """
        ref_time = timestamp or datetime.now()
        await self.graphiti.add_episode(
            name=f"episode_{ref_time.isoformat()}",
            episode_body=content,
            source=EpisodeType.text,
            source_description=source,
            reference_time=ref_time,
        )

    async def search(self, query: str, num_results: int = 10) -> list[dict[str, Any]]:
        """Search the graph for relevant context.

        Returns entities and relationships relevant to the query.
        """
        results = await self.graphiti.search(query, num_results=num_results)

        # Format results for context injection
        context_items = []
        for result in results:
            # Extract human-readable content from Graphiti objects
            if hasattr(result, "fact"):
                # Edge (relationship) - has .fact attribute
                content = result.fact
            elif hasattr(result, "name"):
                # EntityNode - has .name and .summary
                content = f"{result.name}: {getattr(result, 'summary', '')}"
            else:
                # Fallback
                content = str(result)

            context_items.append({
                "type": result.__class__.__name__,
                "content": content,
                "score": getattr(result, "score", None),
            })

        return context_items

    async def get_context_string(self, query: str, max_items: int = 5) -> str:
        """Get formatted context string for prompt injection."""
        results = await self.search(query, num_results=max_items)

        if not results:
            return ""

        context_parts = ["Relevant context from memory:"]
        for item in results:
            context_parts.append(f"- {item['content']}")

        return "\n".join(context_parts)

    async def close(self) -> None:
        """Close connections."""
        await self.graphiti.close()
