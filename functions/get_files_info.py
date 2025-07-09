import os
from google.genai import types
from functions.utils import return_abs_path

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory=None):
    abs_working_dir, abs_dir = return_abs_path(working_directory, directory)

    if not abs_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif not os.path.isdir(abs_dir):
        return f'Error: "{directory}" is not a directory'
    else:
        contents = []
        is_dir = False
        try:
            for content in os.listdir(abs_dir):
                content_path = os.path.join(abs_dir, content)
                is_dir = os.path.isdir(content_path)

                try:
                    file_size = os.path.getsize(content_path)
                except Exception as e:
                    return f"Error: {e}"
                
                contents.append(f"- {content}: file_size={file_size}, is_dir={is_dir}")
        except Exception as e:
            return f"Error: {e}"
        
        return "\n".join(contents)

