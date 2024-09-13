import shutil
import time
from pathlib import Path

def delete_directory(directory):
    attempts = 0
    while attempts < 5:
        try:
            shutil.rmtree(directory)
            print(f"Directory {directory} deleted successfully.")
            break
        except FileNotFoundError:
            print(f"Directory {directory} not found, no need to delete.")
            break
        except PermissionError as e:
            attempts += 1
            print(f"Permission error: {e}. Retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    else:
        print(f"Failed to delete {directory} after {attempts} attempts.")
