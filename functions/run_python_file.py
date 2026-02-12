import os
import subprocess

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
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: executing Python file: {e}")