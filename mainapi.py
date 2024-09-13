from flask import Flask, request, jsonify
import os
import json
from run_firstpage import process_files, generate_score

app = Flask(__name__)

UPLOAD_FOLDER1 = 'Data/Resumes'
UPLOAD_FOLDER2 = 'Data/JobDescription'
JSON_FOLDER = 'Data/Processed/Resumes'
JSON_FOLDER1 = 'Data/Processed/JobDescription'
ALLOWED_EXTENSIONS = {'pdf'}

# Ensure upload folders exist
if not os.path.exists(UPLOAD_FOLDER1):
    os.makedirs(UPLOAD_FOLDER1)
if not os.path.exists(UPLOAD_FOLDER2):
    os.makedirs(UPLOAD_FOLDER2)

app.config['UPLOAD_FOLDER1'] = UPLOAD_FOLDER1
app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def find_json_file_by_resume_pattern(pattern):
    """Find a JSON file in JSON_FOLDER that matches the given pattern in the filename."""
    for filename in os.listdir(JSON_FOLDER):
        if filename.endswith('.json') and pattern in filename:
            file_path = os.path.join(JSON_FOLDER, filename)
            file_path = os.path.normpath(file_path)  # Normalize the file path
            return file_path
    return None

def find_json_file_by_jd_pattern(pattern):
    """Find a JSON file in JSON_FOLDER1 that matches the given pattern in the filename."""
    for filename in os.listdir(JSON_FOLDER1):
        if filename.endswith('.json') and pattern in filename:
            file_path = os.path.join(JSON_FOLDER1, filename)
            file_path = os.path.normpath(file_path)  # Normalize the file path
            return file_path
    return None

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and process files."""
    if 'Resume' not in request.files or 'Jd' not in request.files:
        return jsonify({'error': 'Both Resume and Job Description files are required'}), 400
    
    resume_file = request.files['Resume']
    jd_file = request.files['Jd']
    
    if resume_file.filename == '' or jd_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if resume_file and allowed_file(resume_file.filename) and jd_file and allowed_file(jd_file.filename):
        resume_filename = resume_file.filename
        jd_filename = jd_file.filename
        
        resume_file_path = os.path.join(app.config['UPLOAD_FOLDER1'], resume_filename)
        jd_file_path = os.path.join(app.config['UPLOAD_FOLDER2'], jd_filename)
        
        resume_file_path = os.path.normpath(resume_file_path)  # Normalize the file path
        jd_file_path = os.path.normpath(jd_file_path)  # Normalize the file path
        
        resume_file.save(resume_file_path)
        jd_file.save(jd_file_path)
        
        # Call process_files after saving the files
        result = process_files()

        # Find JSON file corresponding to the resume file
        resume_pattern = resume_filename.rsplit('.', 1)[0]  # Extract base name without extension
        jd_pattern = jd_filename.rsplit('.', 1)[0]
        
        resume_json_file_path = find_json_file_by_resume_pattern(resume_pattern)
        jd_json_file_path = find_json_file_by_jd_pattern(jd_pattern)

        response = generate_score(resume_json_file_path, jd_json_file_path)
        print(response)
        return jsonify({'message': 'Files uploaded and processing complete',
            'resume_filename': resume_filename,
            'jd_filename': jd_filename,
            'similarity_score': response['similarity_score'],
            'improvement': response['groq_result']})
    
    return jsonify({'error': 'File type not allowed'}), 400

def read_json(filename):
    """Read and return JSON data from a file."""
    with open(filename) as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    app.run(debug=True)
