from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python
from functions.write_file import write_file
from google.genai import types

FUNCTIONS = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python": run_python,
    "write_file": write_file
}

def call_function(function_call_part, verbose=False):
    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"
    fn = FUNCTIONS.get(function_call_part.name)

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    if fn is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    
    result = fn(**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )