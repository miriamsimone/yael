#!/usr/bin/env python3
"""
Yael - ElevenLabs CLI Conversational Agent
"""

import os
import sys
import asyncio
import signal
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

# Load environment variables
load_dotenv()

console = Console()


class YaelAgent:
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.agent_id = os.getenv("ELEVENLABS_AGENT_ID")

        if not self.api_key:
            console.print("[red]Error: ELEVENLABS_API_KEY not found in .env file[/red]")
            sys.exit(1)

        if not self.agent_id:
            console.print("[red]Error: ELEVENLABS_AGENT_ID not found in .env file[/red]")
            sys.exit(1)

        self.client = ElevenLabs(api_key=self.api_key)
        self.conversation = None
        self.audio_interface = None

    async def start(self):
        """Start the conversational agent"""
        console.print(Panel.fit(
            "[bold cyan]Yael - ElevenLabs CLI Agent[/bold cyan]\n"
            "Press Ctrl+C to exit",
            border_style="cyan"
        ))

        try:
            # Initialize audio interface
            self.audio_interface = DefaultAudioInterface()

            # Create conversation
            console.print("[yellow]Connecting to ElevenLabs...[/yellow]")
            self.conversation = Conversation(
                client=self.client,
                agent_id=self.agent_id,
                requires_auth=True,
                audio_interface=self.audio_interface,
                callback_agent_response=self.on_agent_response,
                callback_agent_response_correction=self.on_agent_response_correction,
                callback_user_transcript=self.on_user_transcript,
                callback_latency_measurement=self.on_latency_measurement,
            )

            console.print("[green]Connected! Start speaking...[/green]\n")

            # Start conversation - runs in background thread
            self.conversation.start_session()

            # Wait for conversation to end
            await self.conversation.wait_for_session_end()

        except KeyboardInterrupt:
            console.print("\n[yellow]Shutting down...[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
        finally:
            await self.cleanup()

    async def cleanup(self):
        """Clean up resources"""
        if self.conversation:
            try:
                await self.conversation.end_session()
            except Exception as e:
                # Ignore cleanup errors
                pass
        console.print("[green]Goodbye![/green]")

    def on_user_transcript(self, transcript):
        """Callback when user speech is transcribed"""
        console.print(f"[blue]You:[/blue] {transcript}")

    def on_agent_response(self, response):
        """Callback when agent responds"""
        console.print(f"[green]Agent:[/green] {response}")

    def on_agent_response_correction(self, original, corrected):
        """Callback when agent response is corrected"""
        console.print(f"[yellow]Correction:[/yellow] {original} -> {corrected}")

    def on_latency_measurement(self, latency_ms):
        """Callback for latency measurements"""
        # Optionally log latency for debugging
        pass


async def main():
    agent = YaelAgent()

    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        console.print("\n[yellow]Received interrupt signal...[/yellow]")
        asyncio.create_task(agent.cleanup())
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    await agent.start()


if __name__ == "__main__":
    asyncio.run(main())
