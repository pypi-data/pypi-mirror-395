import argparse
import sys
from .converters import convert


def main() -> None:
    parser = argparse.ArgumentParser(prog="gpsexchang", description="Convert between GPX and FIT formats")
    parser.add_argument("-s", "--sourceFile", required=True, help="Source file path")
    parser.add_argument("--source", required=True, choices=["gpx", "fit"], help="Source format")
    parser.add_argument("--dest", required=True, choices=["gpx", "fit"], help="Destination format")
    parser.add_argument("-o", "--output", required=False, help="Destination file path")
    args = parser.parse_args()
    try:
        out = convert(args.sourceFile, args.source, args.dest, args.output)
        print(out)
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

