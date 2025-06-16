import os
from functions.utils import return_abs_path

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
