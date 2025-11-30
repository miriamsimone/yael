# Yael - ElevenLabs CLI Conversational Agent

A command-line interface for ElevenLabs Conversational AI with support for real-time speech-to-text, text-to-speech, and tool calling.

## Features

- Real-time voice conversations with ElevenLabs Agent
- Built-in speech-to-text (STT) and text-to-speech (TTS)
- Tool calling support for extending agent capabilities
- Extensible architecture for adding intelligence layers
- Rich CLI output with transcripts

## Prerequisites

- Python 3.8 or higher
- ElevenLabs API key
- Microphone and speakers
- ElevenLabs Agent created in the web dashboard

## Setup

### 1. Clone or navigate to the project

```bash
cd yael
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```
ELEVENLABS_API_KEY=your_api_key_here
ELEVENLABS_AGENT_ID=your_agent_id_here
```

**Getting your credentials:**

1. **API Key**: Get from https://elevenlabs.io/app/settings/api-keys
2. **Agent ID**:
   - Go to https://elevenlabs.io/app/conversational-ai
   - Create a new agent or use an existing one
   - Copy the Agent ID from the agent settings

### 5. Configure tools (optional)

If you want your agent to use tools:

1. Go to your agent in the ElevenLabs dashboard
2. Add tools in the agent configuration (JSON schema format)
3. Implement the corresponding functions in `tools.py`

Example tools are already provided in `tools.py`:
- `get_current_time` - Returns current time and date
- `get_weather` - Mock weather data (integrate real API as needed)
- `calculate` - Basic calculator
- `take_note` - Save notes to a file

## Usage

### Basic usage

```bash
python cli_agent.py
```

The agent will:
1. Connect to ElevenLabs
2. Start listening to your microphone
3. Display transcripts of your speech
4. Respond with voice and text

### Exiting

Press `Ctrl+C` to gracefully exit the conversation.

## Project Structure

```
yael/
├── cli_agent.py          # Main CLI application
├── tools.py              # Tool definitions and implementations
├── requirements.txt      # Python dependencies
├── .env.example         # Example environment configuration
├── .env                 # Your actual configuration (gitignored)
└── README.md           # This file
```

## Architecture

Current architecture:
```
User (Microphone) → CLI Agent → ElevenLabs API → Speaker
```

Future extensibility:
```
User → CLI Agent → [Classifier/Router] → ElevenLabs Agent
                        ↓
                   Custom LLM layer
```

## Adding Custom Tools

1. **Define the tool in ElevenLabs dashboard**:
   ```json
   {
     "name": "my_tool",
     "description": "What the tool does",
     "parameters": {
       "type": "object",
       "properties": {
         "param1": {
           "type": "string",
           "description": "Parameter description"
         }
       },
       "required": ["param1"]
     }
   }
   ```

2. **Implement in `tools.py`**:
   ```python
   @registry.register("my_tool")
   def my_tool(param1: str) -> Dict[str, Any]:
       """Tool implementation"""
       return {"result": "value"}
   ```

3. **The agent will automatically call your tool when needed**

## Troubleshooting

### Audio issues

If you encounter audio problems:

- **macOS**: Grant microphone permissions in System Preferences → Security & Privacy
- **Linux**: Ensure ALSA or PulseAudio is configured
- **Windows**: Check microphone settings in Windows settings

### Dependencies

If PyAudio installation fails:

**macOS**:
```bash
brew install portaudio
pip install pyaudio
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

**Windows**: Download from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

### API errors

- Verify your API key is correct
- Check your ElevenLabs account has API access
- Ensure the Agent ID matches an existing agent

## Next Steps

- Add custom tools for your use case
- Integrate intelligence layers (classifiers, routers)
- Add conversation history/memory
- Implement custom audio processing
- Add support for multiple agents

## License

MIT
# yael
