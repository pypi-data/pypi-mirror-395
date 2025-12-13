import argparse
from . import main

def cli():
    parser = argparse.ArgumentParser(description='This is CLI to transform pdf into images')

    parser.add_argument('--pdf', type=str, help="Path to pdf", required=True)
    parser.add_argument('--ouput-dir', type=str, help="Output directory", default="images")
    parser.add_argument('--password', type=str, help="PDF password", default=None)

    args = parser.parse_args()

    main(args.pdf, args.ouput_dir, args.password)

if __name__ == "__main__":
    cli()
