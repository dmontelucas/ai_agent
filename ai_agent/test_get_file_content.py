from functions.get_file_content import get_file_content
from config import MAX_CHARS


def print_header(title: str):
    print(title)


def main():
    # 1) Truncation test: lorem.txt
    print_header('get_file_content("calculator", "lorem.txt")')
    lorem = get_file_content("calculator", "lorem.txt")
    if lorem.startswith("Error:"):
        print(lorem)
    else:
        print(f"Length returned: {len(lorem)}")
        # Show only the tail so we can see the truncation marker
        tail = lorem[-120:] if len(lorem) >= 120 else lorem
        print(f"Tail: {tail}")

        expected_marker = f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'
        print(f"Truncation marker present: {expected_marker in lorem}")
    print()

    # 2) Other required test cases
    print_header('get_file_content("calculator", "main.py")')
    print(get_file_content("calculator", "main.py"))
    print()

    print_header('get_file_content("calculator", "pkg/calculator.py")')
    print(get_file_content("calculator", "pkg/calculator.py"))
    print()

    print_header('get_file_content("calculator", "/bin/cat")')
    print(get_file_content("calculator", "/bin/cat"))
    print()

    print_header('get_file_content("calculator", "pkg/does_not_exist.py")')
    print(get_file_content("calculator", "pkg/does_not_exist.py"))
    print()


if __name__ == "__main__":
    main()
