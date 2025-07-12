from functions.utils import return_abs_path
from google.genai import types
import os
import subprocess

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the specified Python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the Python file to execute. Required. If not provided, an error is returned.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path):
    abs_working_dir, abs_file_path = return_abs_path(working_directory, file_path)

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    elif not abs_file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    else:
        try:
            result = subprocess.run(['python', abs_file_path], cwd=abs_working_dir, timeout=30, capture_output=True)
            stdout = result.stdout.decode()
            stderr = result.stderr.decode()

            if stdout or stderr:    
                return_string = f'STDOUT: {stdout}\nSTDERR: {stderr}'
                if result.returncode != 0:
                    return_string += f'\nProcess exited with code {result.returncode}' 
                return return_string
            else:
                return 'No output produced.'

        except Exception as e:
            return f"Error: executing Python file: {e}"