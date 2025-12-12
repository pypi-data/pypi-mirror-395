import argparse
import sys
from pathlib import Path
from .builder import build_script


def main(argv=None):
    parser = argparse.ArgumentParser(prog="pyexe", description="Simple py -> exe packer (v0.1.0)")
    sub = parser.add_subparsers(dest="cmd")

    p_build = sub.add_parser("build", help="Build a script into an exe-like bundle")
    p_build.add_argument("script", help="Path to the Python script to bundle")
    p_build.add_argument("-o", "--output", help="Output path (file or directory). Default: ./dist/<name>.exe or .pyz")
    p_build.add_argument("--embed-interpreter", action="store_true", help="Embed current Python interpreter into package (may be large). Requires Windows and permissions.")

    args = parser.parse_args(argv)

    if args.cmd == "build":
        script = Path(args.script)
        if not script.exists():
            print(f"Error: script not found: {script}", file=sys.stderr)
            sys.exit(2)

        out = args.output
        try:
            build_script(script, output=out, embed_interpreter=args.embed_interpreter)
        except Exception as e:
            print(f"Build failed: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
