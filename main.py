import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python
from functions.write_file import schema_write_file
from call_function import call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python,
        schema_write_file
    ]
)


if len(sys.argv) < 2:
    print("No prompt passed")
    sys.exit(1)

user_prompt = sys.argv[1]
model_name = "gemini-2.0-flash-001"
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

max_iters = 20

try:
    for _ in range(max_iters):
        content = client.models.generate_content(
            model=model_name, 
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )
        for candidate in content.candidates:
            messages.append(candidate.content)

        is_verbose = "--verbose" in sys.argv

        if is_verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {content.usage_metadata.candidates_token_count}")
            print(f"Response: {content.text}")

        if content.function_calls:
            for function_call_part in content.function_calls:
                function_call_result = call_function(function_call_part, verbose=is_verbose)

                if not function_call_result.parts or not getattr(function_call_result.parts[0], "function_response", None):
                    raise RuntimeError("Invalid tool response from call_function")

                tool_part = function_call_result.parts[0].function_response
                resp = tool_part.response
                if "--verbose" in sys.argv:
                    print(f"-> {resp}")

                resp_msg = types.Content(
                    role = "user",
                    parts= [
                        types.Part.from_function_response(
                            name=tool_part.name,
                            response=resp
                        )
                    ]
                )

                messages.append(resp_msg)

            continue

        if content.text:
            print(f"Final Response: {content.text}")
            break

except Exception as e:
    print(e)