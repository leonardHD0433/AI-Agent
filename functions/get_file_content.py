import os
from google.genai import types
from functions.utils import return_abs_path

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Return the contents of the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file to read. Required. If not provided, an error is returned.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    abs_working_dir, abs_file_path = return_abs_path(working_directory, file_path)
    
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    else:
        try:
            with open(abs_file_path, "r") as f:
                file_content = f.read()
            
            if len(file_content) > 10000:         
                file_content = file_content[:10000]
                file_content += f'[...File "{file_path}" truncated at 10000 characters]'

            return file_content
        
        except Exception as e:
            return f"Error: {e}"