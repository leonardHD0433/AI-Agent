import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
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

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

content = client.models.generate_content(model=model_name, 
                                         contents=messages,
                                         config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
                                        )

if "--verbose" in sys.argv:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {content.usage_metadata.candidates_token_count}")
    print(f"Response: {content.text}")

elif content.function_calls:
    for function_call_part in content.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")

else:
    print(content.text)