"""
Tool definitions for the agent.

To add a new tool:
1. Create a new class that inherits from BaseTool
2. Implement get_schema() to return the tool definition
3. Implement execute(params) to handle the tool logic
4. Add an instance to TOOL_LIST
"""
import os
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
        return {
            "name": "list_directory",
            "description": "Lists all files and directories in a given directory path.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The directory path to list contents from"
                    }
                },
                "required": ["path"]
            }
        }

    def execute(self, params: Dict[str, Any]) -> str:
        path = params.get("path", ".")
        try:
            if not os.path.exists(path):
                return f"Error: Path '{path}' does not exist"
            if not os.path.isdir(path):
                return f"Error: Path '{path}' is not a directory"
            
            contents = os.listdir(path)
            if not contents:
                return f"Directory '{path}' is empty"
            
            # Add trailing slash to directories - so the LLM knows what to look deeper into!
            formatted_items = []
            for item in sorted(contents):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    formatted_items.append(f"  - {item}/")
                else:
                    formatted_items.append(f"  - {item}")
            
            return f"Contents of '{path}':\n" + "\n".join(formatted_items)
        except Exception as e:
            return f"Error listing directory '{path}': {str(e)}"

class ReadFileTool(BaseTool):
    """Tool to read the contents of a file."""
    def get_schema(self) -> Dict[str, Any]:
        return {
            "name": "read_file",
            "description": "Reads and returns the contents of a file.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to read"
                    }
                },
                "required": ["file_path"]
            }
        }

    def execute(self, params: Dict[str, Any]) -> str:
        file_path = params.get("file_path")
        if not file_path:
            return "Error: No file path provided"
        
        try:
            if not os.path.exists(file_path):
                return f"Error: File '{file_path}' does not exist"
            if not os.path.isfile(file_path):
                return f"Error: Path '{file_path}' is not a file"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return f"Contents of '{file_path}':\n{content}"
        except Exception as e:
            return f"Error reading file '{file_path}': {str(e)}"


TOOL_LIST = [
    # WeatherTool(),
    ListDirectoryTool(),
    ReadFileTool(),
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
