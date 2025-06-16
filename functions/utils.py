import os

def return_abs_path(working_directory, file):
    return os.path.abspath(working_directory), os.path.abspath(os.path.join(working_directory, file or ""))

