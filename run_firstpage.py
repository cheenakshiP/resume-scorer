# import json
# import logging
# import os
# from scripts import JobDescriptionProcessor, ResumeProcessor
# from scripts.utils import get_filenames_from_dir, init_logging_config
# from scripts.similarity.get_score import *
# from groq import Groq
# PROCESSED_RESUMES_PATH = "Data/Processed/Resumes"
# PROCESSED_JOB_DESCRIPTIONS_PATH = "Data/Processed/JobDescription"
# def process_files():
#     init_logging_config()

#     def remove_old_files(files_path):
#         for filename in os.listdir(files_path):
#             try:
#                 file_path = os.path.join(files_path, filename)
#                 if os.path.isfile(file_path):
#                     os.remove(file_path)
#             except Exception as e:
#                 logging.error(f"Error deleting {file_path}:\n{e}")

#         logging.info("Deleted old files from " + files_path)

#     logging.info("Started to read from Data/Resumes")
#     try:
#         remove_old_files(PROCESSED_RESUMES_PATH)
#         file_names = get_filenames_from_dir("Data/Resumes")
#         logging.info("Reading from Data/Resumes is now complete.")
#     except:
#         logging.error("There are no resumes present in the specified folder.")
#         logging.error("Exiting from the program.")
#         logging.error("Please add resumes in the Data/Resumes folder and try again.")
#         return {"success": False, "message": "Error processing resumes."}

#     logging.info("Started parsing the resumes.")
#     for file in file_names:
#         processor = ResumeProcessor(file)
#         success = processor.process()
#     logging.info("Parsing of the resumes is now complete.")

#     logging.info("Started to read from Data/JobDescription")
#     try:
#         remove_old_files(PROCESSED_JOB_DESCRIPTIONS_PATH)
#         file_names = get_filenames_from_dir("Data/JobDescription")
#         logging.info("Reading from Data/JobDescription is now complete.")
#     except:
#         logging.error("There are no job-descriptions present in the specified folder.")
#         logging.error("Exiting from the program.")
#         logging.error("Please add job descriptions in the Data/JobDescription folder and try again.")
#         return {"success": False, "message": "Error processing job descriptions."}

#     logging.info("Started parsing the Job Descriptions.")
#     for file in file_names:
#         processor = JobDescriptionProcessor(file)
#         success = processor.process()
#     logging.info("Parsing of the Job Descriptions is now complete.")
    
#     return {"success": True, "message": "Processing complete."}

# def read_json(filename):
#         with open(filename) as f:
#             data = json.load(f)
#         return data

# def generate_score(output, output1):
#     selected_file = read_json(output)
#     selected_jd = read_json(output1)
#     resume_string = " ".join(selected_file["extracted_keywords"])
#     jd_string = " ".join(selected_jd["extracted_keywords"])
#     result = get_score(resume_string, jd_string)
#     similarity_score = round(result[0].score * 100, 2)
#     # return (similarity_score)
#     client = Groq(
#     api_key=os.environ.get("api_key"),
#     )
#     query = "send main points of why it is not an ats compliant"
#     chat_completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "system",
#                 "content": selected_file["clean_data"],
#             },
#             {
#                 "role": "user",
#                 "content" : query
#             }
#         ],
#         model="llama3-8b-8192",
#     )
#     groq_result = chat_completion.choices[0].message.content
#     return {
#         'similarity_score': similarity_score,
#         'groq_result': groq_result
#     }
    

# os.environ["api_key"]= "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"
import json
import os
from scripts import JobDescriptionProcessor, ResumeProcessor
from scripts.utils import get_filenames_from_dir
from scripts.similarity.get_score import *
from groq import Groq

PROCESSED_RESUMES_PATH = "Data/Processed/Resumes"
PROCESSED_JOB_DESCRIPTIONS_PATH = "Data/Processed/JobDescription"

def process_files():
    def remove_old_files(files_path):
        for filename in os.listdir(files_path):
            try:
                file_path = os.path.join(files_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}:\n{e}")

    try:
        remove_old_files(PROCESSED_RESUMES_PATH)
        file_names = get_filenames_from_dir("Data/Resumes")
    except:
        print("There are no resumes present in the specified folder.")
        print("Exiting from the program.")
        print("Please add resumes in the Data/Resumes folder and try again.")
        return {"success": False, "message": "Error processing resumes."}

    for file in file_names:
        processor = ResumeProcessor(file)
        success = processor.process()

    try:
        remove_old_files(PROCESSED_JOB_DESCRIPTIONS_PATH)
        file_names = get_filenames_from_dir("Data/JobDescription")
    except:
        print("There are no job descriptions present in the specified folder.")
        print("Exiting from the program.")
        print("Please add job descriptions in the Data/JobDescription folder and try again.")
        return {"success": False, "message": "Error processing job descriptions."}

    for file in file_names:
        processor = JobDescriptionProcessor(file)
        success = processor.process()
    
    return {"success": True, "message": "Processing complete."}

def read_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

def generate_score(output, output1):
    selected_file = read_json(output)
    selected_jd = read_json(output1)
    resume_string = " ".join(selected_file["extracted_keywords"])
    jd_string = " ".join(selected_jd["extracted_keywords"])
    result = get_score(resume_string, jd_string)
    similarity_score = round(result[0].score * 100, 2)
    
    client = Groq(api_key=os.environ.get("api_key"))
    query = "send main points of why it is not an ats compliant"
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": selected_file["clean_data"],
            },
            {
                "role": "user",
                "content": query
            }
        ],
        model="llama3-8b-8192",
    )
    groq_result = chat_completion.choices[0].message.content
    return {
        'similarity_score': similarity_score,
        'groq_result': groq_result
    }

# os.environ["api_key"] = "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"
