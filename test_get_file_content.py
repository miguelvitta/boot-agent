from config import MAX_CHARS
from functions.get_file_content import get_file_content


def test():
    result = get_file_content("calculator", "lorem.txt")
    print("Result for 'lorem.txt':")
    # 1) length is greater than MAX_CHARS (because we added the suffix)
    assert len(result) > MAX_CHARS

    # 2) content ends with the exact truncation message string
    suffix = f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'
    assert result.endswith(suffix)

    print(result)
    print("")

    result = get_file_content("calculator", "main.py")
    print("Result for 'main.py':")
    print(result)
    print("")

    result = get_file_content("calculator", "pkg/calculator.py")
    print("Result for 'pkg/calculator' file:")
    print(result)

    result = get_file_content("calculator", "/bin/cat")
    print("Result for '/bin/cat' 'cat' tool:")
    print(result)

    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print("Result for 'a file that does not exist' directory:")
    print(result)


if __name__ == "__main__":
    test()
