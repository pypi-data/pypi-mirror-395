import os
import sys
import subprocess
import getpass
from pathlib import Path

def init_data_dir() -> str:
    """
    Ensure GRID_DATA_DIR is set. On first run (when unset), prompt the user to choose
    between user-wide (~/.grid) or system-wide (/opt/grid) storage, create the directory,
    and optionally append the export to ~/.bashrc.
    """
    data_dir = os.environ.get("GRID_DATA_DIR")
    if data_dir:
        return data_dir

    # Non-interactive (e.g., tests or services), default to user-wide storage
    if not sys.stdin.isatty():
        data_dir = os.path.expanduser("~/.grid")
        try:
            os.makedirs(data_dir, exist_ok=True)
        except Exception:
            pass
        os.environ["GRID_DATA_DIR"] = data_dir
        return data_dir

    print("GRID_DATA_DIR is not set. It seems this is the first time running the server.")
    print("Select storage option:")
    print("  1: User-wide (~/.grid)")
    print("  2: System-wide (/opt/grid)")
    choice = input("Enter 1 or 2: ").strip()
    if choice == "1":
        data_dir = os.path.expanduser("~/.grid")
        try:
            os.makedirs(data_dir, exist_ok=True)
        except Exception as e:
            print(f"Error creating directory {data_dir}: {e}")
            sys.exit(1)
    elif choice == "2":
        data_dir = "/opt/grid"
        username = getpass.getuser()
        try:
            subprocess.run(["sudo", "mkdir", "-p", data_dir], check=True)
            subprocess.run(["sudo", "groupadd", "-f", "grid-users"], check=True)
            subprocess.run(["sudo", "usermod", "-aG", "grid-users", username], check=True)
            subprocess.run(["sudo", "chown", "-R", f"root:grid-users", data_dir], check=True)
            subprocess.run(["sudo", "chmod", "-R", "775", data_dir], check=True)
            subprocess.run(["sudo", "chmod", "g+s", data_dir], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error setting up system-wide storage: {e}")
            sys.exit(1)
        print(f"[grid] {username} added to grid-users. You may need to restart your shell for group changes to take effect.")
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

    bashrc_path = Path.home() / ".bashrc"
    should_export = input(
        f"Would you like to add 'export GRID_DATA_DIR={data_dir}' to {bashrc_path}? (y/n): "
    ).strip().lower()
    if should_export in ("y", "yes"):
        try:
            with open(bashrc_path, "a") as f:
                f.write(f"\n# Added by GRID server setup\nexport GRID_DATA_DIR={data_dir}\n")
            print(f"Appended export to {bashrc_path}")
        except Exception as e:
            print(f"Error writing to {bashrc_path}: {e}")
            sys.exit(1)

    os.environ["GRID_DATA_DIR"] = data_dir
    return data_dir