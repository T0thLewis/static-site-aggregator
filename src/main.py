from copystatic import copy_files_wrapper
from generate_page import generate_pages_recursive


def main():
    print("----------------------------------")
    print("Initializing static site aggregator...")
    print("----------------------------------")
    print("* Copying static files...")
    copy_files_wrapper("static", "public")
    print("* Generating pages...")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
