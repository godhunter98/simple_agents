from typing import Any, List, Optional, Dict
import json


class Agent:
    def __init__(
        self,
        client,
        model: str = 'mistral-medium-latest',
        system: str = "",
        tools: Optional[List[Dict[str, Any]]] = None,
        debug: bool = False,
    ) -> None:
        self.client = client
        self.system = system
        self.model = model
        self.messages: list = []
        self.debug = debug  # Control whether to show tool call details
        self.last_tool_calls: list[dict] = []
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

        return final_assistant_content

    def execute(self):
        # Clearing any previous tool calls
        self.last_tool_calls = []

        while True:
            completion = self.client.chat.completions.create(
                model=self.model,
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

                    # Capturing tool information for logging
                    self.last_tool_calls.append(
                        {
                            "function_name": function_name,
                            "arguments": raw_args,
                            "tool_call_id": tool_call.id,
                        }
                    )

                    if function_name in self.function_map:
                        function_to_call = self.function_map[function_name]
                        exected_output = function_to_call(**function_args)
                        tool_output_content = str(exected_output)

                        tool_outputs.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": tool_output_content,
                            }
                        )
                    else:
                        if self.debug:
                            print(f"Unknown tool requested: {function_name}")
                self.messages.extend(tool_outputs)

            else:
                # Return plain response (no formatting)
                return response_message.content


if __name__ == "__main__":
    pass
