"""
Tool definitions for the agent.

To add a new tool:
1. Create a new class that inherits from BaseTool
2. Implement get_schema() to return the tool definition
3. Implement execute(params) to handle the tool logic
4. Add an instance to TOOL_LIST
"""
from typing import Any, Dict


class BaseTool:
    """Base class for all tools."""
    
    def get_schema(self) -> Dict[str, Any]:
        """Return the JSON tool schema."""
        raise NotImplementedError("Subclasses must implement get_schema()")
    
    def execute(self, params: Dict[str, Any]) -> str:
        """Execute the tool and return result as string."""
        raise NotImplementedError("Subclasses must implement execute()")


class WeatherTool(BaseTool):
    """Tool for getting weather information."""
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "name": "get_weather",
            "description": "Returns the weather for a given city.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city to get weather for"
                    }
                },
                "required": ["city"]
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> str:
        city = params.get("city", "Unknown")
        return f"Weather in {city}: Beautiful and sunny!"

"""
TODO: add more tools here!
"""
class ListDirectoryTool(BaseTool):
    """Tool to list the contents of a file directory."""
    def get_schema(self) -> Dict[str, Any]:
        pass

    def execute(self, params: Dict[str, Any]) -> str:
        pass

class ReadFileTool(BaseTool):
    """Tool to read the contents of a file."""
    def get_schema(self) -> Dict[str, Any]:
        pass

    def execute(self, params: Dict[str, Any]) -> str:
        pass


TOOL_LIST = [
    WeatherTool(),
]


class ToolHandler:
    """Handles tool registration and execution."""
    
    def __init__(self):
        self.tools = []
        self.tool_map = {}
        
        for tool_instance in TOOL_LIST:
            schema = tool_instance.get_schema()
            self.tools.append(schema)
            self.tool_map[schema["name"]] = tool_instance
    
    def handle_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """Execute a tool and return the result as a string."""
        tool = self.tool_map.get(tool_name)
        
        if tool is None:
            return f"Error: Unknown tool '{tool_name}'"
        
        try:
            return tool.execute(tool_input)
        except Exception as e:
            return f"Error executing tool '{tool_name}': {str(e)}"
