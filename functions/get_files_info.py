import os

def get_files_info(working_directory, directory="."):
    try:
        pwd = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(pwd, directory))
        valid_dir = os.path.commonpath([pwd, full_path]) == pwd
        ph = f"'{directory}'" if directory != "." else "current"
        if not valid_dir:
            raise Exception(f'Cannot list "{directory}" as it is outside the permitted working directory')
        if not os.path.isdir(full_path):
            raise Exception(f'"{directory}" is not a directory')
        print(f"Result for {ph} directory")
        for element in os.listdir(full_path):
            print(f"- {element}: file_size={os.path.getsize(full_path + "/" + element)} bytes, is_dir={os.path.isdir(full_path + "/" + element)}")
    except Exception as e:
        print(f"Error: {e}")