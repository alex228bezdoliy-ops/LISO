import os
import sys
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter


def ask_user(prompt):
    while True:

        answer = input(f"{prompt} [y/n]: ").strip().lower()
        
        if answer in ('y', 'yes'):
            return True
        
        elif answer in ('n', 'no'):
            return False
        
        else:
            print("Please write correct option [y/n]")


def copy_files(disk_path):

    dir_completer = PathCompleter(expanduser=True, only_directories=True)

    while True:

        copy_file_path = prompt("Please input MOUNTED DIRECTORY to copy files: ", completer=dir_completer).strip()
        copy_file_path = os.path.expanduser(copy_file_path)

        if not os.path.exists(copy_file_path):

            os.makedirs(copy_file_path, exist_ok=True)
            print(f"Directory created: {copy_file_path}")
            break

        elif os.path.exists(copy_file_path):
            break

        else:
            print("Invalid path, try again.")

    if not os.path.exists(disk_path):
        print(f"Disk path not found: {disk_path}")
        sys.exit(1)

    os.system(f"sudo cp -r {disk_path}/* {copy_file_path}/")
    print(f"Files copied to: {copy_file_path}")

def write_iso(disk_path, iso_path):

    print("⚠ WARNING: ALL DATA ON YOUR DISK WILL BE REMOVED!")

    if ask_user("Do you want to continue?"):

        os.system(f"sudo dd if={iso_path} of={disk_path} bs=4M status=progress oflag=sync")
        print("ISO successfully written to disk.")

    else:

        print("Operation cancelled.")
        sys.exit(0)


def user_disk_path():

    while True:

        disk_path = input("Please input a Flash path (/dev/sdX): ").strip()

        if os.path.exists(disk_path):
            return disk_path
        
        else:
            print("Input a valid disk path!")


def user_iso_path():
    iso_completer = PathCompleter(expanduser=True)

    while True:
        iso_path = prompt("Please input ISO path: ", completer=iso_completer).strip()
        iso_path = os.path.expanduser(iso_path)

        if os.path.exists(iso_path) and iso_path.endswith('.iso'):
            return iso_path
        
        else:
            print("Please input a valid ISO path!")


def main():
    disk_path = user_disk_path()

    if ask_user("Do you want to copy files from your Flash?"):
        copy_files(disk_path)

    else:
        iso_path = user_iso_path()
        write_iso(disk_path, iso_path)


def welcome():
    print("Welcome to LISO!")

    if ask_user("Do you want to continue?"):
        main()

    else:
        sys.exit()

if __name__ == "__main__":
    welcome()
