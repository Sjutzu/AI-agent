import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        pwd = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(pwd, file_path))
        valid = os.path.commonpath([pwd, full_path]) == pwd
        if not valid:
            raise Exception(f'Cannot read "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(full_path):
            raise Exception(f'File not found or is not a regular file: "{file_path}"')
        with open(full_path) as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'\n\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            print(content)
            return content
    except Exception as e:
        print(f"Error: {e}")
