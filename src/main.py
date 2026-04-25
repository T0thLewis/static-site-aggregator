from copystatic import copy_files_wrapper


def main():
    print("Initiating copy of static files...")
    copy_files_wrapper("static", "public")


if __name__ == "__main__":
    main()
