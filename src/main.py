from copystatic import copy_files_wrapper
from generate_page import generate_page


def main():
    print("----------------------------------")
    print("Initializing static site aggregator...")
    print("----------------------------------")
    print("* Copying static files...")
    copy_files_wrapper("static", "public")
    print("* Generating pages...")
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
