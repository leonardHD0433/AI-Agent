from functions.utils import return_abs_path
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the given content to the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file to be written. Required. If not provided, an error is returned.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the specified file. Required. If not provided, an error is returned.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    abs_working_dir, abs_file_path = return_abs_path(working_directory, file_path)

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    else:
        try:
            with open(abs_file_path, "w") as f:
                f.write(content)
        except Exception as e:
            return f"Error: {e}"
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'