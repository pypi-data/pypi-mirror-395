import difflib
from typing import List


def get_unified_diff(str_a: str, str_b: str) -> List[str]:
    diff_iterator = difflib.unified_diff(
        str_a.split(), str_b.split(), "変更前", "変更後"
    )
    return list(diff_iterator)


def get_unified_diff_string(str_a: str, str_b: str) -> str:
    diff_list = get_unified_diff(str_a, str_b)
    return "\n".join(diff_list)


if __name__ == "__main__":

    import sys

    if len(sys.argv) != 3:
        print("Usage: python unified_diff_getter.py <path_a> <path_b>")
        sys.exit(1)

    str_a = open(sys.argv[1]).read()
    str_b = open(sys.argv[2]).read()
    print(get_unified_diff_string(str_a, str_b))
