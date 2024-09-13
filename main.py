# import os
# import shutil
# import time
# from pathlib import Path

# def delete_directory(directory):
#     attempts = 0
#     while attempts < 5:
#         try:
#             shutil.rmtree(directory)
#             print(f"Directory {directory} deleted successfully.")
#             break
#         except FileNotFoundError:
#             print(f"Directory {directory} not found, no need to delete.")
#             break
#         except PermissionError as e:
#             attempts += 1
#             print(f"Permission error: {e}. Retrying in 5 seconds...")
#             time.sleep(5)
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             break
#     else:
#         print(f"Failed to delete {directory} after {attempts} attempts.")

# # Example usage
# dir_to_delete = Path('C:\\Users\\lenovo\\AppData\\Local\\Temp\\fastembed_cache\\fast-bge-base-en')
# delete_directory(dir_to_delete)

# from streamlit_app import get_selected_file, get_resume_score


# def print_selected_resume():
#     selected_file = get_selected_file()
#     score = get_resume_score()
#     print("Parsed Resume Name:", selected_file)
#     print("Score is: ", score)

# # Example usage
# if __name__ == "__main__":
#     print_selected_resume()

import json

def read_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

selected_file = read_json("Data/Processed/Resumes/" + "Resume-Python Resume.pdf77c78f69-b0e6-4e50-8751-c556382f5015.json")