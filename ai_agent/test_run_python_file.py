from functions.run_python_file import run_python_file


def print_case(label: str, result: str):
    print(label)
    # indent multi-line output
    for line in result.splitlines() if result else ["(no output)"]:
        print(f"  {line}")
    print()


def main():
    print_case(
        'run_python_file("calculator", "main.py")',
        run_python_file("calculator", "main.py"),
    )

    print_case(
        'run_python_file("calculator", "main.py", ["3 + 5"])',
        run_python_file("calculator", "main.py", ["3 + 5"]),
    )

    print_case(
        'run_python_file("calculator", "tests.py")',
        run_python_file("calculator", "tests.py"),
    )

    print_case(
        'run_python_file("calculator", "../main.py")',
        run_python_file("calculator", "../main.py"),
    )

    print_case(
        'run_python_file("calculator", "nonexistent.py")',
        run_python_file("calculator", "nonexistent.py"),
    )

    print_case(
        'run_python_file("calculator", "lorem.txt")',
        run_python_file("calculator", "lorem.txt"),
    )


if __name__ == "__main__":
    main()
