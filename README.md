```
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
   #***##*####+***#**=*##*#+*++*+++=+*+++**##*###*#*%%%%%%%#%#%%%@@###%%#%%%#%%
  ##*=+++#**=#*+#+*+*#++=*+*+#===+=*=+#=-=+*##=+***##@#%%%%##%#%*#%%%####%#%%%%
  %%**+**+#+=#%=###@@@%%@@%**+++===+====++*#**##*##%%+##*%%%*%##*##%##%*#%%%%#%
  *****##*#%#**#%## =     +@++-=+====+=-**=++#+##**%@#*%%##*#*#*#*###%##*####*%
   =+%*##%%%##%##%%+        +**-=:*=+-+-+-*-+=##+%*######%+**##*#***#****#*%%##
     ==++@%%*#*%#+%           #*=-+=*=-+--=**++=+%*@#**#***+=+#+*+****++*#*#*%#
         %##%##@@**            =*--==++-+-+-****%%##%*##*++***+++*+==++*#*##+##
         #*%##%%@+ +             %+:-*+***+##*++@@@%%@*##+++==+=+==++=+=#*###%*
      =  ####%#%*                 %#*+#%+###*#%@%%@%%%###*++*=-==+-+=*+++*##*++
      = =@%%@@%%%                  %%##%%%%@#%@@%@@@%@%##+=***-=-=*+=+++++#=#*+
     ===#*###@**#                   %%%%%%%@%@@@%@%%@@%#+*+===++-==-++-==+=**==
      ===**%#%**                     #%#%@@@@@%%@#@%@@@%*-+*=---=-+=---*-+*=*==
        =*#*@#+                       +%%@@@@@@@@@%%%%#**++#*+--=-===:-=+-+*=-=
           %*+                         *%%@@@@@@@%%%#*#*++=*-*:-=----====*----=
          +-     =                       #%@@@@@@@@###**#**+=====-:--=+--==---=
                                          %@@@@@@%%%%%#%**+*#++=+-::=:--=--:=--
                                          +#%@@@@@@@%%#%%*******+-==-:=--+==-==
                                           %%@@@@@@@%#%%**+*+#+===--+--+-*=-:*=
                                            #%@@@@@@@@@@%%##*+*+==+++===:@-+-==
```

# יָעֵל Yael

**Self-hosted LLM with graph memory that actually remembers.**

> A mountain goat that climbs impossible terrain

## Why Yael?

Current AI assistants (ChatGPT, Claude.ai) use keyword-based RAG for memory - they search your past conversations like a dumb search engine. Yael uses **graph-based memory**: it extracts entities, relationships, and temporal context from your conversations, building a knowledge graph that understands *meaning*, not just keywords.

**Example:**
- **Keyword RAG:** "Find messages containing 'project deadline'"
- **Graph RAG:** "What do I know about this person's work context, deadlines, and related projects?"

The graph extracts:
- **Entities**: People, projects, concepts, dates
- **Relationships**: "works on", "deadline is", "related to"
- **Temporal context**: When things were discussed, how they evolved

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- [Ollama](https://ollama.ai) (or use Docker - see below)
- OpenAI API key (for embeddings only - LLM runs locally)

### Setup

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/yael.git
cd yael

# Start Neo4j
docker-compose up -d

# Create virtual environment and install
python3 -m venv .venv
.venv/bin/pip install -e .

# Pull local LLM (option 1: native Ollama)
ollama pull llama3.1:8b

# OR option 2: use Docker Ollama (better for Linux servers)
docker-compose --profile with-ollama up -d
docker exec yael-ollama ollama pull llama3.1:8b

# Configure
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run
.venv/bin/yael
```

## Features

✅ **Local LLM** - Your conversations stay on your machine (via Ollama)
✅ **Graph Memory** - Entities and relationships, not keyword search
✅ **User Profile** - Builds personalized context from your conversation history at session start
✅ **Temporal Awareness** - Understands when things were discussed
✅ **Rich CLI** - Beautiful terminal interface with history
✅ **Import Claude History** - Bring your Claude conversations into Yael's memory
✅ **Configurable** - Edit system prompts, change models, etc.

## Usage

### Start Chatting

```bash
.venv/bin/yael
```

### CLI Commands

| Command | Description |
|---------|-------------|
| `/help` | Show commands |
| `/clear` | Clear session history |
| `/system` | Show system prompt |
| `/edit` | Edit config in $EDITOR |
| `/config` | Show config file location |
| `/quit` | Exit |

### Import Your Claude History

```bash
# 1. Export from claude.ai: Settings → Export Data
# 2. Extract the ZIP
# 3. Import:
.venv/bin/python scripts/import_claude.py path/to/conversations.json
```

Your Claude conversations will be imported into Yael's graph memory!

## Configuration

Edit `~/.yael/config.yml`:

```yaml
llm:
  model: "llama3.1:8b"  # or llama3.1:70b if you have the VRAM
  base_url: "http://localhost:11434"

embeddings:
  provider: "openai"
  model: "text-embedding-3-small"

graph:
  uri: "bolt://localhost:7688"
  user: "neo4j"
  password: "yaelgraph"
  database: "neo4j"

system_prompt: |
  You are Yael (יָעֵל), a personal AI assistant with persistent graph memory.
  Your name means "mountain goat" in Hebrew - you climb impossible terrain.

  ## Core Personality

  You are warm, direct, and genuinely helpful. You speak like a knowledgeable
  friend, not a corporate assistant. No hollow phrases like "Great question!"
  or "I'd be happy to help!" - just actually help.

  ... (3,135 character system prompt - edit ~/.yael/config.yml to customize)
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLI (yael)                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐ │
│  │   Ollama    │◄──►│    Core     │◄──►│    Graphiti     │ │
│  │  (LLM)      │    │   Engine    │    │  (Graph RAG)    │ │
│  └─────────────┘    └─────────────┘    └────────┬────────┘ │
│                            │                     │          │
│                            ▼                     ▼          │
│                     ┌─────────────┐       ┌───────────┐    │
│                     │   Config    │       │   Neo4j   │    │
│                     │ (system     │       │  (Docker) │    │
│                     │  prompt)    │       └───────────┘    │
│                     └─────────────┘              │          │
│                                                  ▼          │
│                                          [Volume Mount]     │
│                                          ~/.yael/neo4j/     │
└─────────────────────────────────────────────────────────────┘

External API: OpenAI Embeddings (text-embedding-3-small)
```

### Tech Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Local LLM | Ollama + Llama 3.1 8B | Best quality at 16GB RAM |
| Graph RAG | Graphiti | Built for conversational memory, temporal awareness |
| Graph DB | Neo4j (Docker) | Graphiti's native backend, mature, visualizable |
| Embeddings | OpenAI text-embedding-3-small | Fast, cheap, no local GPU needed |
| CLI | Python + rich + prompt_toolkit | Pretty output, readline support |
| Config | YAML | Human-editable system prompts |

## Development

### Running Tests

```bash
# Test Phase 1 (Infrastructure)
.venv/bin/python test_phase1.py

# Test Phase 2 (Core Engine)
.venv/bin/python test_phase2.py

# Test Phase 3 (CLI)
.venv/bin/python test_phase3.py

# Test Integration (full end-to-end)
.venv/bin/python test_integration.py
```

### Docker Options

**Development (macOS):** Native Ollama recommended (GPU acceleration via Metal)
```bash
brew install ollama
ollama serve
docker-compose up -d  # Just Neo4j
```

**Production (Linux server):** Docker Ollama with GPU support
```bash
docker-compose --profile with-ollama up -d  # Neo4j + Ollama
```


## v0.2+ Roadmap: Yael as Thinking Partner

The MVP is reactive - you talk, she responds. The vision is **proactive** - Yael thinks about you even when you're not there.

### Daemon Mode (Background Processing)

**Active Memory**
- `yael-daemon` runs on cron (every few hours)
- Queries graph: "what does this person care about?"
- Crawls configured sources: arxiv, HN, RSS feeds, specific blogs
- For each item: "would they find this interesting?" (LLM call)
- If yes → ingest to graph with tag `discovered`, include summary
- Next session: "I found something while you were away..."

**Morning Briefing**
- Runs once daily (configurable time)
- Pulls: calendar events, recent graph activity, any `discovered` items
- Generates: natural language summary of your day + what's on your mind
- Delivery: CLI on login, or push to email/notification

**Overnight Thinking**
- You end a session with `/think <problem>`
- Daemon picks it up, runs multiple reasoning passes
- Explores graph for related context
- Generates candidate approaches, counterarguments
- Next session: "I've been thinking about X. Here's where I landed..."

**Spaced Repetition**
- Track concepts/facts you've discussed
- Schedule resurfacing based on forgetting curve
- Gentle prompts: "Remember when we talked about Y? Still relevant?"
- Optional quiz mode for things you're trying to learn

### Tool Calling

**Web Search**
- Query the web mid-conversation
- Ingest results to graph for future reference
- "Let me look that up" → returns with context

**Calendar Integration**
- Read: "What do I have tomorrow?"
- Write: "Schedule a reminder to follow up with Klee next week"
- Context: Yael knows your schedule when reasoning about your time

### Implementation Notes

All daemon features share:
- Same graph backend (Neo4j)
- Same LLM (Ollama)
- Config in `~/.yael/daemon.yml`
- Logs to `~/.yael/logs/`

Tool calling via simple plugin interface:
```python
class Tool:
    name: str
    description: str  # for LLM to understand when to use
    def run(self, args: dict) -> str: ...
```

Yael decides when to call tools based on conversation context.


## License

MIT

## Contributing

PRs welcome! This is a weekend project. 🐐
