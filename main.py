import openai
import os
from nsepython import nsefetch
from typing import Any, Optional, List, Dict
import json
from pydantic import BaseModel, Field

from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

base_url = "https://api.mistral.ai/v1"
# base_url = "https://generativelanguage.googleapis.com/v1beta/openai/" ##Comment out if using gemini API


def fetch_security_data(symbol: str):
    """
    Get the price, percent_change, pe_ratio and industry for a security, just pass in the ticker symbol.
    """
    try:
        # Get quote from NSE directly
        url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
        data = nsefetch(url)

        price, percent_change, pe_ratio,industry = (
            data["priceInfo"]["lastPrice"],
            data["priceInfo"]["pChange"],
            data['metadata']['pdSymbolPe'],
            data['info']['industry']
        )
        return round(price, 2), round(percent_change, 2),pe_ratio,industry
    except Exception as e:
        print(f"Error: {e}")
        return None


class GetFetchPriceArgs(BaseModel):
    symbol: str = Field(
        ...,
        description="The ticker symbol of the security being fetched, just pass in the ticker symbol and not the full name e.g. INFY, RELIANCE ",
    )


TOOLS = [
    {
        "schema": {
            "type": "function",
            "function": {
                "name": "fetch_security_data",
                "description": "Get the price, percent_change, pe_ratio and industry for a security, just pass in the ticker symbol.",
                "parameters": GetFetchPriceArgs.model_json_schema(),
            },
        },
        "function": fetch_security_data,
    }
]


class Agent:
    def __init__(
        self, client, system: str = "", tools: Optional[List[Dict[str, Any]]] = None
    ) -> None:
        self.client = client
        self.system = system
        self.messages: list = []
        if tools:
            self.tools = [tool["schema"] for tool in tools]
            self.function_map = {
                tool["schema"]["function"]["name"]: tool["function"] for tool in tools
            }
        else:
            self.tools = []
            self.function_map = {}
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message="", *args: Any, **kwargs: Any) -> Any:
        if message:
            self.messages.append({"role": "user", "content": message})

        final_assistant_content = self.execute()

        if message:
            self.messages.append(
                {"role": "assistant", "content": final_assistant_content}
            )

        return final_assistant_content

    def execute(self):
        while True:
            completion = self.client.chat.completions.create(
                model="mistral-medium-latest",
                messages=self.messages,
                tools=self.tools,
                tool_choice="auto",
            )
            response_message = completion.choices[0].message

            if response_message.tool_calls:
                self.messages.append(response_message)

                tool_outputs = []

                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    raw_args = tool_call.function.arguments
                    function_args = (
                        raw_args
                        if isinstance(raw_args, dict)
                        else json.loads(raw_args or "{}")
                    )

                    if function_name in self.function_map:
                        function_to_call = self.function_map[function_name]
                        exected_output = function_to_call(**function_args)
                        tool_output_content = str(exected_output)
                        print(
                            f"\nExecuting tool:{function_name} with args {function_args}") # For Debugging #, Output:{tool_output_content[:500]}")

                        tool_outputs.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": tool_output_content,
                            }
                        )
                    else:
                        print(f"Unknown tool requested: {function_name}")
                self.messages.extend(tool_outputs)

            else:
                return response_message.content


client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=base_url)
system = "You are helpful AI assistant."
tools = TOOLS
agent = Agent(client, system, tools)


# Example usage
prompt = str(input("\nEnter your prompt: "))
response = agent(prompt)
print("\n" + response)
