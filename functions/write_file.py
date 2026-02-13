import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        pwd = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(pwd, file_path))
        valid = os.path.commonpath([pwd, full_path]) == pwd
        if not valid:
            raise Exception(f'Cannot write to "{file_path}" as it is outside the permitted working directory')
        if os.path.isdir(full_path):
            raise Exception(f'Cannot write to "{file_path}" as it is a directory')
        with open(full_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Writes text content to a file inside the specified working directory. "
        "If the file already exists, it will be overwritten. "
        "The function ensures the file path remains within the permitted "
        "working directory for security reasons. "
        "Returns a success message including the number of characters written."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file inside the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file.",
            ),
        },
        required=["file_path", "content"]
    ),
)