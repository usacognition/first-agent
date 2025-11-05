# Cognition Merge Lab: Building Your First Agent

A basic template for building an AI agent.

## How It Works

This implements a simple **agentic loop**:
1. User sends a query to the agent
2. The model receives the query + available tools
3. The model either:
   - Returns a final answer, OR
   - Calls one or more tools to gather information
4. If tools were called, their results are sent back to the model
5. Loop continues until the model provides a final answer or hits the max iteration limit.

- `agent.py`: Main agentic loop and conversation management
- `tools.py`: Tool definitions (each tool has a schema + execute method)

## Setup

1. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
   Or similar Python setup on Windows machines!

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your API key:**
Create a file called `.env` and add this line:
    ```
    ANTHROPIC_API_KEY='your-key-here'
    ```

4. **Run the demo:**
   ```bash
   python agent.py
   ```


## Building a Code Q&A Agent

To create an agent that can answer questions about codebases, add these two tools:

**1. ListDirectory Tool (`ls`)**
- Use Python's `os.listdir()` or `os.walk()` 
- Input: `path` (directory to list)
- Output: List of files/folders in that directory
- Tip: Return results as a formatted string with file names

**2. ReadFile Tool (`read_file`)**
- Use Python's `open().read()`
- Input: `file_path` (path to file)
- Output: The file's contents as a string
- Tip: Add error handling for files that don't exist or can't be read
- Bonus: Add `start_line` and `max_lines` parameters to limit large files

With these tools, the agent can explore directories and read files to answer questions like "What does the WeatherTool class do?" or "How many Python files are in this project?"


### Using it on your own codebases

Currently, the agent only works with the current directory. The simplest way to extend this:
1. First use `input()` to get the base path from the user
2. Provide this base path in the system prompt
3. Modify the `ls` and `read_file` tools to use absolute paths

_For a quick hack, you can also copy your repo into this directory to give the agent access to it!_

Refer to the `codebase-qna` branch for a complete implementation of this agent.


## Next Steps
1. Customize your system prompt! For example, add additional instructions to customize answer format.
2. Use different models - try `claude-sonnet-4-5` for smarter but slower responses.


## Bonus Challenges
1. Add multi-turn conversation to reply to your agent's answers
2. Add streaming to your agent to see the answer as it generates
3. Experiment with more tools! (e.g. `grep`, `find`)
