import os
from anthropic import Anthropic
from dotenv import load_dotenv
from tools import ToolHandler

# Load API keys
load_dotenv()


class Agent:    
    def __init__(self):
        """
        Initialize the agent.
        """
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Please provide an API key or set ANTHROPIC_API_KEY environment variable")
        
        self.client = Anthropic(api_key=api_key)
        self.tool_handler = ToolHandler()
        self.system_prompt = "You are an AI agent. Use the available tools to respond to the user's query."
    
    def run(self, user_query: str, max_iterations: int = 10) -> str:
        """
        Run the agent with a user query.
        
        Args:
            user_query: The question or request from the user
            max_iterations: Maximum number of tool-use iterations (safety limit)
        
        Returns:
            The agent's final answer
        """
        messages = [
            {
                "role": "user",
                "content": user_query
            }
        ]
        
        # START OF AGENT LOOP
        iteration = 0
        while iteration < max_iterations:
            print(f"\n--- Iteration {iteration + 1} ---")
            
            # Call the LLM
            response = self.client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=1024,
                system=self.system_prompt,
                tools=self.tool_handler.tools,
                messages=messages
            )

            # response.content is a list of text blocks and tool_use blocks.
            # If there are no tool_use blocks, then the LLM is done thinking and wants to provide a final answer.
            
            # Check if any tools were called
            tool_use_blocks = [block for block in response.content if block.type == "tool_use"]
            
            if not tool_use_blocks:
                # No tools called, extract final answer
                text_blocks = [block.text for block in response.content if hasattr(block, "text")]
                final_answer = "\n".join(text_blocks)
                print(f"\n✓ Final answer received")
                return final_answer
            
            # The LLM wants to use a tool. Continue to the next iteration.
            messages.append({
                "role": "assistant",
                "content": response.content
            })
            
            # Execute each tool and collect results
            tool_results = []
            for tool_use in tool_use_blocks:
                tool_name = tool_use.name
                tool_input = tool_use.input
                
                print(f"  → Calling tool: {tool_name}")
                print(f"    Input: {tool_input}")
                
                # Execute the tool
                result = self.tool_handler.handle_tool(tool_name, tool_input)
                print(f"    Result: {result}")
                
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": result
                })
            
            # Add tool results to conversation
            messages.append({
                "role": "user",
                "content": tool_results
            })
            
            iteration += 1
        
        return "Error: Maximum iterations reached without final answer"


def main():    
    # TODO: get the user to input the base path to a local codebase
    # Pass it into Agent initialization as a parameter
    
    agent = Agent()

    query = input("Enter your query: ")
    answer = agent.run(query)
    print(f"\nAnswer: {answer}")


if __name__ == "__main__":
    main()
