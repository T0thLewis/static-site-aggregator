import sys

from copystatic import copy_files_wrapper
from generate_page import generate_pages_recursive


def main():
    base_path = sys.argv[1] if len(sys.argv) > 1 else "/"
    print("----------------------------------")
    print("Initializing static site aggregator...")
    print("----------------------------------")
    print("* Copying static files...")
    copy_files_wrapper("static", "docs")
    print("* Generating pages...")
    generate_pages_recursive("content", "template.html", "docs", base_path=base_path)


if __name__ == "__main__":
    main()
