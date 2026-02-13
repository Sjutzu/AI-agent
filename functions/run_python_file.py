import os
import subprocess
from google.genai import types
class ValidationError(Exception):
    pass

def run_python_file(working_directory, file_path, args=None):
    try:
        pwd = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(pwd, file_path))
        valid_dir = os.path.commonpath([pwd, full_path]) == pwd
        if not valid_dir:
            raise ValidationError(f'Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(full_path):
            raise ValidationError(f'"{file_path}" does not exist or is not a regular file')
        if file_path[len(file_path) - 3:len(file_path)] != ".py":
            raise ValidationError(f'"{file_path}" is not a Python file')
        command = ["python", full_path]
        if args: command.extend(args)
        run = subprocess.run(
            command,
            cwd=working_directory, 
            capture_output= True,
            text= True,
            timeout=30
        )
        output = ""
        if run.returncode != 0:
            output += f"Process exited with code {run.returncode}\n"
        if not run.stderr and not run.stdout:
            output += f"No output produced\n"
        else:
            output += f"STDOUT: {run.stdout}STDERR: {run.stderr}"
        return output
    except ValidationError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Executes a Python file located inside the specified working directory. "
        "The function validates that the file exists, is a regular file, "
        "is a .py file, and remains within the permitted working directory. "
        "Optional command-line arguments may be passed to the script. "
        "Returns the captured standard output and standard error, along with "
        "the exit code if the process fails."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file inside the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the Python script.",
            ),
        },
        required=["file_path"]
    ),
)