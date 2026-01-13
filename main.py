import argparse
from pathlib import Path

from equb_mobi_to_cbz.converter import convert_to_cbz
from equb_mobi_to_cbz.gui import run_gui


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--cli", action="store_true")
  parser.add_argument("--out", type=str, default="")
  parser.add_argument("inputs", nargs="*")
  args = parser.parse_args()

  if not args.cli:
    run_gui()
    return

  if not args.inputs:
    raise SystemExit("No input files.")

  output_dir = Path(args.out).resolve() if args.out else None
  for input_file in args.inputs:
    convert_to_cbz(Path(input_file).resolve(), output_dir=output_dir)


if __name__ == "__main__":
  main()
