from functions.utils import return_abs_path

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