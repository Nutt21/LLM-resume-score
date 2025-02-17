# LLM-Resume-Score: Resume Scoring API

This is a FastAPI-based application that extracts ranking criteria from job descriptions and scores resumes against those criteria. The API supports bulk uploads of resumes in PDF or DOCX formats, processes them using OpenAI's GPT-4o-mini model, and returns an Excel sheet with the scores.

Features

Extract Ranking Criteria: Extract key ranking criteria (e.g., skills, certifications, experience) from a job description.

Score Resumes: Score multiple resumes against the extracted criteria using OpenAI's GPT-4.

Bulk Upload: Accept multiple resumes in PDF or DOCX formats.

Excel Output: Generate and download an Excel sheet with candidate scores.

Setup

Prerequisites

Python 3.8 or higher

OpenAI API key

FastAPI

Additional dependencies: pdfplumber, python-docx, pandas, openai, python-dotenv

Installation

Clone the repository:

git clone <https://github.com/yourusername/resume-scoring-api.git>
cd resume-scoring-api

Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install the required dependencies:

pip install -r requirements.txt

Create a .env file in the root directory and add your OpenAI API key:

OPENAI_API_KEY=your_openai_api_key_here

Run the FastAPI application:

uvicorn main:app --reload

Access the API documentation at:

<http://127.0.0.1:8000/docs>

API Endpoints

1. Extract Ranking Criteria

Endpoint: POST /extract-criteria

Description: Extracts key ranking criteria from a job description file (PDF or DOCX).

Input:

file: Upload a job description file (PDF or DOCX).

Output:

JSON response with extracted criteria.

Example Request:

curl -X POST "<http://127.0.0.1:8000/extract-criteria>" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@job_description.pdf"

Example Response:

{
  "criteria": [
    "Proficient with Microsoft Word and Excel",
    "General knowledge of employment law and practices",
    "Knowledge of AI"
  ]
}

1. Score Resumes

Endpoint: POST /score-resumes

Description: Scores multiple resumes against provided ranking criteria and returns an Excel sheet with the results.

Input:

criteria: List of ranking criteria (e.g., ["Proficient with Microsoft Word and Excel", "Knowledge of AI"]).

files: Upload multiple resume files (PDF or DOCX).

Output:

Excel file (resume_scores.xlsx) with candidate scores.

Example Request:

curl -X POST "<http://127.0.0.1:8000/score-resumes>" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "criteria=Proficient with Microsoft Word and Excel" \
  -F "criteria=Knowledge of AI" \
  -F "files=@resume1.pdf" \
  -F "files=@resume2.docx"

Example Output:

An Excel file (resume_scores.xlsx) with the following structure:

Candidate Name

Proficient with Microsoft Word and Excel

Knowledge of AI

Total Score

resume1.pdf

4

3

7

resume2.docx

5

4

9

Usage Example

Step 1: Extract Criteria

Upload a job description file (PDF or DOCX) to the /extract-criteria endpoint.

Retrieve the extracted criteria in JSON format.

Step 2: Score Resumes

Use the extracted criteria as input to the /score-resumes endpoint.

Upload multiple resumes (PDF or DOCX).

Download the Excel sheet with candidate scores.

Dependencies

FastAPI: Web framework for building the API.

pdfplumber: Extracts text from PDF files.

python-docx: Extracts text from DOCX files.

openai: Interacts with OpenAI's GPT-4o-mini model.

pandas: Generates Excel files.

python-dotenv: Manages environment variables.

Contributing

Contributions are welcome! Please follow these steps:

Fork the repository.

Create a new branch for your feature or bugfix.

Commit your changes and push to the branch.

Submit a pull request.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Contact

For questions or feedback, please contact:

Your Name  
Email: [rnithishere@gmail.com]
GitHub: Nutt21
