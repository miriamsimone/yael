"""Rich CLI interface for Yael."""
import asyncio
from rich.console import Console
from rich.panel import Panel
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from .engine import ChatEngine
from .config import CONFIG_DIR, CONFIG_FILE

console = Console()

COMMANDS = {
    "/help": "Show this help message",
    "/clear": "Clear conversation history",
    "/system": "Show current system prompt",
    "/edit": "Edit system prompt (opens in $EDITOR)",
    "/config": "Open config file location",
    "/quit": "Exit Yael",
}


YAEL_ASCII = """[dim green]
                                            +*+    +**
                                       ****=+#****+++*+*++*+++*
                                   ++*++*#+*++#***+***#*******#**+*
                                +++++*++*#*#********#**#*#***#+*+###*
                             +*#+=++*#******++***#**##@%%*%####+***+**#
                          =##++***##***+++*##%@**#****          %****#*#
                      #*+++++*****+++++*#%#*+*#***#*+**+*=         =#+***
                    #*=*++=+********##@%%##%%%%%##%#%*#**++*         %#***
                   *+*++*#*****#**%@=                %%###+**          #*#
                 *=#*#=+##******%                        ##**+*        -#*+
                #*#*****+*+***%                            %**+=        #*
               +***#+*******%-                              ==*+        ##
             %=+*=+#**%***#@                                -+*=        *
             ##**#****+*#%-                                   @@*+
            **#*+**+***#%                                     @%
            **+**#*#***#
           **+**++*#**#-
          *%#*##**#**%%                                                      *
          **++++++*#%@ *#   =                             +
          ***++**%#+#@#**#
          ##*+#*+**%%%=+#+#@#%%*
         -%%#+=+###*#%-=:==@@@#%%%
         *%%##+*%%%###-+=-*@@#%@%@%
         *##*#***#%%*#+=-#*@@##%%#%@#
        *#@%%*#@%#++==*+++#%%#%%%%@#%%#*#
        %%%%+#**++++**==*#*%%#%#%####@%@%%#**#
       %%%*#**+**=--#**+*%%###%##@%%%#%*%%##*# # * %*
   ==*#%###+###**-=-*=+*##*+#**%##%%%%%*#%%%##%**#%%## ## *  ***
    *####**#%#**+-***+%*######**##*%#*%#*#+##%#######@%%%%@%%%####%##** #+
#   %#%##%*%###++-*#+**+#+*#*#*+*+###*#++######%*#%##%#@@@%@%#%#%%%%##%###*#**+
   #***##*####+***#**=*##*#+*++*+++=+*+++**##*###*#*%%%%%%%#%#%%%@@###%%#%%%#%%#
  ##*=+++#**=#*+#+*+*#++=*+*+#===+=*=+#=-=+*##=+***##@#%%%%##%#%*#%%%####%#%%%%#
  %%**+**+#+=#%=###@@@%%@@%**+++===+====++*#**##*##%%+##*%%%*%##*##%##%*#%%%%#%#
  *****##*#%#**#%## =     +@++-=+====+=-**=++#+##**%@#*%%##*#*#*#*###%##*####*%%
   =+%*##%%%##%##%%+        +**-=:*=+-+-+-*-+=##+%*######%+**##*#***#****#*%%###
     ==++@%%*#*%#+%           #*=-+=*=-+--=**++=+%*@#**#***+=+#+*+****++*#*#*%##
         %##%##@@**            =*--==++-+-+-****%%##%*##*++***+++*+==++*#*##+###
         #*%##%%@+ +             %+:-*+***+##*++@@@%%@*##+++==+=+==++=+=#*###%*#
      =  ####%#%*                 %#*+#%+###*#%@%%@%%%###*++*=-==+-+=*+++*##*++#
      = =@%%@@%%%                  %%##%%%%@#%@@%@@@%@%##+=***-=-=*+=+++++#=#*+*
     ===#*###@**#                   %%%%%%%@%@@@%@%%@@%#+*+===++-==-++-==+=**==+
      ===**%#%**                     #%#%@@@@@%%@#@%@@@%*-+*=---=-+=---*-+*=*==*
        =*#*@#+                       +%%@@@@@@@@@%%%%#**++#*+--=-===:-=+-+*=-==
           %*+                         *%%@@@@@@@%%%#*#*++=*-*:-=----====*----==
          +-     =                       #%@@@@@@@@###**#**+=====-:--=+--==---=:
                                          %@@@@@@%%%%%#%**+*#++=+-::=:--=--:=--:
                                          +#%@@@@@@@%%#%%*******+-==-:=--+==-===
                                           %%@@@@@@@%#%%**+*+#+===--+--+-*=-:*=-
                                            #%@@@@@@@@@@%%##*+*+==+++===:@-+-==-
[/dim green]"""


def print_welcome():
    """Print welcome banner."""
    console.print(YAEL_ASCII)
    console.print(Panel.fit(
        "[bold blue]יָעֵל[/bold blue] [dim]Yael[/dim]\n"
        "[dim]Self-hosted LLM with graph memory[/dim]\n\n"
        "Type [bold]/help[/bold] for commands",
        border_style="blue",
    ))


def print_help():
    """Print available commands."""
    console.print("\n[bold]Commands:[/bold]")
    for cmd, desc in COMMANDS.items():
        console.print(f"  [cyan]{cmd}[/cyan] - {desc}")
    console.print()


async def handle_command(cmd: str, engine: ChatEngine) -> bool:
    """Handle slash commands. Returns True if should continue, False to quit."""
    cmd = cmd.strip().lower()

    if cmd == "/quit" or cmd == "/exit" or cmd == "/q":
        return False

    elif cmd == "/help" or cmd == "/?":
        print_help()

    elif cmd == "/clear":
        engine.clear_history()
        console.print("[dim]Conversation history cleared.[/dim]")

    elif cmd == "/system":
        console.print(Panel(
            engine.system_prompt,
            title="System Prompt",
            border_style="green",
        ))

    elif cmd == "/config":
        console.print(f"[dim]Config file: {CONFIG_FILE}[/dim]")

    elif cmd == "/edit":
        import subprocess
        import os
        editor = os.environ.get("EDITOR", "nano")
        try:
            subprocess.run([editor, str(CONFIG_FILE)])
            # Reload config
            from .config import load_config
            engine.config = load_config()
            engine.system_prompt = engine.config["system_prompt"]
            console.print("[dim]Config reloaded.[/dim]")
        except Exception as e:
            console.print(f"[red]Failed to open editor: {e}[/red]")

    else:
        console.print(f"[red]Unknown command: {cmd}[/red]")
        print_help()

    return True


async def run_cli():
    """Main CLI loop."""
    print_welcome()

    # Check prerequisites
    console.print("[dim]Initializing...[/dim]")

    try:
        engine = ChatEngine()
        await engine.initialize()
    except Exception as e:
        console.print(f"[red]Failed to initialize: {e}[/red]")
        console.print("\n[yellow]Make sure:[/yellow]")
        console.print("  1. Docker is running: [cyan]docker-compose up -d[/cyan]")
        console.print("  2. Ollama is running: [cyan]ollama serve[/cyan]")
        console.print("  3. Model is pulled: [cyan]ollama pull llama3.1:8b[/cyan]")
        console.print("  4. OPENAI_API_KEY is set in .env")
        return

    if not engine.llm.is_available():
        console.print("[yellow]Warning: Ollama model not available. Run:[/yellow]")
        console.print(f"  [cyan]ollama pull {engine.config['llm']['model']}[/cyan]")
        console.print("\n[dim]You can continue, but chat won't work until model is available.[/dim]\n")

    console.print("[green]Ready![/green]\n")

    # Setup prompt with history
    history_file = CONFIG_DIR / "history.txt"
    session = PromptSession(
        history=FileHistory(str(history_file)),
        auto_suggest=AutoSuggestFromHistory(),
    )

    try:
        while True:
            try:
                # Run prompt in executor to avoid blocking
                loop = asyncio.get_event_loop()
                user_input = await loop.run_in_executor(
                    None,
                    lambda: session.prompt("You: ")
                )
                user_input = user_input.strip()
            except KeyboardInterrupt:
                console.print()
                continue
            except EOFError:
                break

            if not user_input:
                continue

            # Handle commands
            if user_input.startswith("/"):
                if not await handle_command(user_input, engine):
                    break
                continue

            # Chat
            console.print("[bold blue]Yael:[/bold blue] ", end="")

            try:
                response_text = ""
                async for token in engine.chat(user_input):
                    console.print(token, end="", highlight=False)
                    response_text += token

                console.print("\n")
            except Exception as e:
                console.print(f"\n[red]Error: {e}[/red]\n")
                if "model" in str(e).lower():
                    console.print("[yellow]Hint: Make sure Ollama is running with the model loaded[/yellow]\n")

    finally:
        await engine.close()
        console.print("[dim]Goodbye![/dim]")


def main():
    """Entry point for CLI."""
    asyncio.run(run_cli())
