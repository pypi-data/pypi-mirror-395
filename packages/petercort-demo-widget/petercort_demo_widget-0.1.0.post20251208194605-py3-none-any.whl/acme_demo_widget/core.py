import sys
from typing import Optional


def hello(name: Optional[str] = None) -> str:
    """Return a friendly greeting."""
    target = name or "world"
    return f"Hello, {target}!"


def main() -> None:
    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        name = None
    print(hello(name))


if __name__ == "__main__":
    main()
