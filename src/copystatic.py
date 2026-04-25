import os
import shutil


def copy_files_wrapper(source, dest):
    print(f'* Checking if "./{dest}" directory exists...')
    if os.path.exists(dest):
        print(f'* Removing existing "./{dest}" directory')
        shutil.rmtree(dest)
    print(f'* Creating new "./{dest}" directory')
    os.makedirs(dest)
    copy_files_recursive(source, dest)


def copy_files_recursive(source, dest):
    for item in os.listdir(source):
        s = os.path.join(source, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            os.makedirs(d)
            copy_files_recursive(s, d)
        else:
            print(f"* {s} -> {d}")
            shutil.copy2(s, d)
