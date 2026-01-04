import os

from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    """
    Read up to MAX_CHARS characters from a file within working_directory.
    Always returns a string (including errors).
    """
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Ensure target_path is within working_directory
        valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        if not valid_target_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Must be a regular file
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read up to MAX_CHARS characters
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)
            # If there's still more content, mark as truncated
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {e}"