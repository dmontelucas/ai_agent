import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    """
    Execute a Python file within `working_directory` using subprocess.
    Always returns a string (including errors).
    """
    try:
        if args is None:
            args = []

        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Guardrail: must stay inside working_directory
        if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Must exist and be a regular file
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Must be a .py file
        if not target_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Build command
        command = ["python", target_path]
        if args:
            command.extend(args)

        # Run subprocess
        completed = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        parts = []

        if completed.returncode != 0:
            parts.append(f"Process exited with code {completed.returncode}")

        stdout = (completed.stdout or "").strip()
        stderr = (completed.stderr or "").strip()

        if not stdout and not stderr:
            parts.append("No output produced")
        else:
            if stdout:
                parts.append(f"STDOUT:\n{stdout}")
            if stderr:
                parts.append(f"STDERR:\n{stderr}")

        return "\n".join(parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
