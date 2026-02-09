import os

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
        print(f"Error: {e} ")