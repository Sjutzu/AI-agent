import os
from config import MAX_CHARS
from google.genai import types

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
            return content
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=(
        "Reads the contents of a file from the specified working directory. "
        "The function ensures the requested file is inside the permitted working directory "
        "for security reasons. It returns up to MAX_CHARS characters of the file. "
        "If the file exceeds MAX_CHARS, the output is truncated and a truncation "
        "notice is appended to the result."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file inside the working directory.",
            ),
        },
        required=["file_path"]
    ),
)