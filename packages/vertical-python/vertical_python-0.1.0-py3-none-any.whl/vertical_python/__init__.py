import argparse
from pathlib import Path


def rotate(text: str) -> str:
    lines = text.splitlines()

    # pad trailing whitespace
    max_width = max(len(line) for line in lines)
    lines = [l.ljust(max_width) for l in lines]

    vertical = []
    for line in lines:
        for i, char in enumerate(line):
            if len(vertical) - 1 < i:
                vertical.append('')
            vertical[i] += char

    # right to left
    vertical = reversed(vertical)
    return '\n'.join(vertical)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="vertical-python", description="python but vertical")
    parser.add_argument("path", help="path to vertical .vpy file")
    parser.add_argument('--print', help="just print the rotated vpy, not eval", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    rotated = rotate(Path(args.path).read_text())
    if args.print:
        print(rotated)
    else:
        exec(rotated)


if __name__ == "__main__":
    main()



