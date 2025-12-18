#!/usr/bin/env python3
"""Import Claude conversation export into Yael's graph memory."""
import json
import sys
import asyncio
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

# Load environment
load_dotenv()

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from yael.graph import GraphMemory
from yael.config import load_config, get_openai_key

console = Console()


def parse_claude_export(export_path: Path) -> list[dict]:
    """Parse Claude's conversations.json export.

    Claude export format:
    [
        {
            "uuid": "...",
            "name": "Conversation Title",
            "created_at": "2024-...",
            "updated_at": "2024-...",
            "chat_messages": [
                {
                    "uuid": "...",
                    "text": "message content",
                    "sender": "human" | "assistant",
                    "created_at": "...",
                }
            ]
        }
    ]
    """
    with open(export_path) as f:
        data = json.load(f)

    episodes = []

    for convo in data:
        messages = convo.get("chat_messages", [])
        if not messages:
            continue

        # Group into exchanges
        convo_title = convo.get("name", "Untitled")
        created = convo.get("created_at", "")

        # Build episode from full conversation
        episode_parts = [f"# {convo_title}"]

        for msg in messages:
            sender = msg.get("sender", "human")
            text = msg.get("text", "")

            if sender == "human":
                episode_parts.append(f"User: {text}")
            else:
                episode_parts.append(f"Assistant: {text}")

        # Parse timestamp
        try:
            if created:
                timestamp = datetime.fromisoformat(created.replace("Z", "+00:00"))
            else:
                timestamp = datetime.now()
        except Exception:
            timestamp = datetime.now()

        episodes.append({
            "content": "\n\n".join(episode_parts),
            "timestamp": timestamp,
            "source": f"claude_export:{convo.get('uuid', 'unknown')}",
        })

    return episodes


async def import_episodes(graph: GraphMemory, episodes: list[dict]) -> int:
    """Import episodes into graph."""
    imported = 0

    for episode in episodes:
        try:
            await graph.add_episode(
                content=episode["content"],
                source=episode["source"],
                timestamp=episode["timestamp"],
            )
            imported += 1
        except Exception as e:
            console.print(f"[yellow]Warning: Failed to import episode: {e}[/yellow]")

    return imported


async def main_async():
    if len(sys.argv) < 2:
        console.print("[red]Usage: python import_claude.py <path_to_conversations.json>[/red]")
        console.print("\nTo export from Claude:")
        console.print("  1. Go to claude.ai → Settings → Export Data")
        console.print("  2. Download and extract the ZIP")
        console.print("  3. Run: python scripts/import_claude.py path/to/conversations.json")
        return 1

    export_path = Path(sys.argv[1])
    if not export_path.exists():
        console.print(f"[red]File not found: {export_path}[/red]")
        return 1

    console.print(f"[dim]Loading export from {export_path}...[/dim]")

    # Parse export
    try:
        episodes = parse_claude_export(export_path)
        console.print(f"[green]Found {len(episodes)} conversations[/green]")
    except Exception as e:
        console.print(f"[red]Failed to parse export: {e}[/red]")
        return 1

    if not episodes:
        console.print("[yellow]No conversations to import.[/yellow]")
        return 0

    # Initialize graph
    try:
        config = load_config()
        graph = GraphMemory(
            neo4j_uri=config["graph"]["uri"],
            neo4j_user=config["graph"]["user"],
            neo4j_password=config["graph"]["password"],
            neo4j_database=config["graph"]["database"],
            openai_api_key=get_openai_key(),
            embedding_model=config["embeddings"]["model"],
        )

        await graph.initialize()
        console.print("  [green]✓ Connected to graph database[/green]")
    except Exception as e:
        console.print(f"[red]Failed to connect to graph: {e}[/red]")
        console.print("\n[yellow]Make sure:[/yellow]")
        console.print("  1. Neo4j is running: [cyan]docker-compose up -d[/cyan]")
        console.print("  2. OPENAI_API_KEY is set in .env")
        return 1

    # Import with progress
    console.print(f"\n[bold]Importing {len(episodes)} conversations...[/bold]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Processing conversations...", total=len(episodes))

        imported = 0
        for episode in episodes:
            try:
                await graph.add_episode(
                    content=episode["content"],
                    source=episode["source"],
                    timestamp=episode["timestamp"],
                )
                imported += 1
            except Exception as e:
                console.print(f"[yellow]Warning: {e}[/yellow]")

            progress.advance(task)

    await graph.close()

    console.print(f"\n[green]✓ Imported {imported}/{len(episodes)} conversations into Yael[/green]")
    console.print("[dim]Your Claude conversation history is now part of Yael's memory![/dim]")

    return 0


def main():
    """Entry point."""
    sys.exit(asyncio.run(main_async()))


if __name__ == "__main__":
    main()
