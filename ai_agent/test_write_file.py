from functions.write_file import write_file


def print_case(label: str, result: str):
    print(label)
    print(f"  {result}")
    print()


def main():
    print_case(
        'write_file("calculator", "lorem.txt", "wait, this isn\'t lorem ipsum")',
        write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
    )

    print_case(
        'write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")',
        write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
    )

    print_case(
        'write_file("calculator", "/tmp/temp.txt", "this should not be allowed")',
        write_file("calculator", "/tmp/temp.txt", "this should not be allowed"),
    )


if __name__ == "__main__":
    main()
