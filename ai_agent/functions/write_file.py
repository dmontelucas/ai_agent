import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file relative to the working directory, creating parent directories if needed",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The full text content to write into the file",
            ),
        },
        required=["file_path", "content"],
    ),
)


def write_file(working_directory, file_path, content):
    """
    Write `content` to `file_path` inside `working_directory`.
    Always returns a string (including errors).
    """
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Guardrail: must stay inside working_directory
        valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs
        if not valid_target_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Can't write to a directory
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Ensure parent dirs exist
        parent_dir = os.path.dirname(target_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        # Overwrite file content
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
