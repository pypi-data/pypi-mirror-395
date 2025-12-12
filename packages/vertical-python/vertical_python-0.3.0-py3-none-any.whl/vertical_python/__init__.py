import argparse
import re
from pathlib import Path

CODEC_PATTERN = re.compile(r"^[ \t\f]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)")
"""https://peps.python.org/pep-0263/"""


def rotate(text: str | memoryview) -> str:
    if isinstance(text, memoryview):
        text = text.tobytes().decode("utf-8")

    lines = text.splitlines()
    lines = strip_encoding(lines)

    # pad trailing whitespace
    max_width = max(len(line) for line in lines)
    lines = [l.ljust(max_width) for l in lines]

    vertical = []
    for line in lines:
        for i, char in enumerate(line):
            if len(vertical) - 1 < i:
                vertical.append("")
            vertical[i] += char

    # right to left
    vertical = reversed(vertical)
    # strip trailing space
    vertical = [v.rstrip() for v in vertical]
    return "\n".join(vertical)


def encode_py_to_vpy(text: str) -> str:
    # inverse of rotate(): rotate 3 times (270° CCW == 90° CW)
    for _ in range(3):
        text = rotate(text)
    return text


def strip_encoding(lines: list[str]) -> list[str]:
    if CODEC_PATTERN.match(lines[0]):
        return [""] if len(lines) == 1 else lines[1:]
    return lines


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="vertical-python",
        description="python but vertical",
    )
    parser.add_argument("path", help="path to .vpy or .py file")

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--print",
        help="just print the rotated vpy, not eval",
        action="store_true",
    )
    mode.add_argument(
        "--encode",
        help="treat PATH as .py and print vertical .vpy to stdout",
        action="store_true",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    text = Path(args.path).read_text()

    if args.encode:
        # .py -> .vpy
        vpy = encode_py_to_vpy(text)
        print(vpy)
        return

    # default path: interpret input as .vpy
    rotated = rotate(text)
    if args.print:
        print(rotated)
    else:
        exec(rotated)


if __name__ == "__main__":
    main()
