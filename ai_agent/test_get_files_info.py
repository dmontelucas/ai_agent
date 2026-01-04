from functions.get_files_info import get_files_info


def print_result(title: str, result: str):
    print(title)
    # Indent each returned line by two spaces
    if result:
        for line in result.splitlines():
            print(f"  {line}")
    else:
        print("  (no output)")
    print()


def main():
    print_result(
        'Result for current directory:',
        get_files_info("calculator", ".")
    )

    print_result(
        "Result for 'pkg' directory:",
        get_files_info("calculator", "pkg")
    )

    print_result(
        "Result for '/bin' directory:",
        get_files_info("calculator", "/bin")
    )

    print_result(
        "Result for '../' directory:",
        get_files_info("calculator", "../")
    )


if __name__ == "__main__":
    main()
