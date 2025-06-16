import os
from functions.utils import return_abs_path

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