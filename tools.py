"""
Example tool definitions for Yael agent.

Tools are configured in the ElevenLabs web app dashboard.
This file contains the Python implementation of those tools.

To use tools:
1. Define tools in ElevenLabs dashboard (https://elevenlabs.io/app/conversational-ai)
2. Implement the corresponding functions here
3. Register them with the conversation (see cli_agent.py)
"""

import datetime
import json
from typing import Dict, Any


class ToolRegistry:
    """Registry for tool functions that the agent can call"""

    def __init__(self):
        self.tools = {}

    def register(self, name: str):
        """Decorator to register a tool function"""
        def decorator(func):
            self.tools[name] = func
            return func
        return decorator

    def execute(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """Execute a registered tool"""
        if tool_name not in self.tools:
            return {"error": f"Tool {tool_name} not found"}

        try:
            return self.tools[tool_name](**parameters)
        except Exception as e:
            return {"error": str(e)}


# Global tool registry
registry = ToolRegistry()


# Example Tools
# -------------

@registry.register("get_current_time")
def get_current_time() -> Dict[str, str]:
    """Get the current time"""
    now = datetime.datetime.now()
    return {
        "time": now.strftime("%H:%M:%S"),
        "date": now.strftime("%Y-%m-%d"),
        "day_of_week": now.strftime("%A")
    }


@registry.register("get_weather")
def get_weather(location: str) -> Dict[str, Any]:
    """
    Get weather for a location (mock implementation)

    In production, you would call a real weather API here
    """
    # This is a mock response - integrate with real weather API
    return {
        "location": location,
        "temperature": 72,
        "conditions": "sunny",
        "humidity": 45,
        "note": "This is mock data. Integrate with a real weather API."
    }


@registry.register("calculate")
def calculate(expression: str) -> Dict[str, Any]:
    """
    Safely evaluate a mathematical expression

    Args:
        expression: A mathematical expression like "2 + 2" or "10 * 5"
    """
    try:
        # Only allow basic math operations for safety
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return {"error": "Invalid characters in expression"}

        result = eval(expression, {"__builtins__": {}}, {})
        return {
            "expression": expression,
            "result": result
        }
    except Exception as e:
        return {"error": f"Calculation error: {str(e)}"}


@registry.register("take_note")
def take_note(note: str) -> Dict[str, str]:
    """
    Save a note to a file

    Args:
        note: The note content to save
    """
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("notes.txt", "a") as f:
            f.write(f"[{timestamp}] {note}\n")
        return {
            "status": "success",
            "message": "Note saved successfully"
        }
    except Exception as e:
        return {"error": str(e)}


# Add more tools as needed
# Example template:
#
# @registry.register("tool_name")
# def tool_name(param1: str, param2: int) -> Dict[str, Any]:
#     """Tool description"""
#     # Implementation
#     return {"result": "value"}
