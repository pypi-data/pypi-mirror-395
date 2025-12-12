import sys

from .context_diff_getter import get_context_diff, get_context_diff_string
from .unified_diff_getter import get_unified_diff, get_unified_diff_string


def main():
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: uvx yklib_diff_getter <str_a> <str_b>")
        print("Usage: python -m yklib_diff_getter <str_a> <str_b>")
        sys.exit(1)
    
    if len(sys.argv) == 3:
        # str_a, str_b = sys.argv[1:]
        print(get_unified_diff_string(*sys.argv[1:]))
    elif len(sys.argv) == 4:        
        if sys.argv[1] == "unified":
            print(get_unified_diff_string(*sys.argv[2:]))
        elif sys.argv[1] == "context":
            print(get_context_diff_string(*sys.argv[2:]))
        else:
            print("Usage: unified <str_a> <str_b>")
            print("Usage: context <str_a> <str_b>")
            sys.exit(1)

__all__ = [
    "get_context_diff",
    "get_context_diff_string",
    "get_unified_diff",
    "get_unified_diff_string",
]

if __name__ == "__main__":
    print("Executing __main__.py")
    main()