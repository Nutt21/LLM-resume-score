from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse

from openai import OpenAI
from typing import List
from functions import score_resume, extract_text
import os
import pandas as pd
from dotenv import load_dotenv
from models import Output
import json
import io

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


app = FastAPI(title="Resume Scoring API", description="API to extract criteria from job descriptions and score resumes.")

# Task 1: Extract Ranking Criteria
@app.post("/extract-criteria")
async def extract_criteria(file: UploadFile = File(...)):
    """
    Extracts ranking criteria from a job description.

    - **file**: Upload a job description (PDF or DOCX)
    
    **Returns**:
    - A JSON object containing the extracted criteria.
    """
    text = extract_text(file)
    if not text:
        raise HTTPException(status_code=400, detail="No text extracted from the file.")
    
    # Use LLM to extract key criteria 
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",

        messages=[{"role": "system", "content": "Extract key ranking criteria such as skills, certifications, experience, and qualifications. Ensure output is in JSON format"},
                  {"role": "user", "content": text}],
        response_format=Output
    )
    content = completion.choices[0].message.content
    formatted_content = json.loads(content)
    return formatted_content

#Task 2: Score Resumes
@app.post("/score-resumes")
async def score_resumes(
    criteria: List[str] = Form(...),
    files: List[UploadFile] = File(...)
):
    """
    Scores resumes based on extracted criteria.

    - **criteria**: List of ranking criteria (e.g., skills, certifications)
    - **files**: Multiple resumes (PDF or DOCX)

    **Returns**:
    - An Excel file containing scores for each candidate.
    """
    results = []
    for file in files:
        try:
            # Extract text from the resume
            text = extract_text(file)
            if not text:
                raise HTTPException(status_code=400, detail=f"No text extracted from {file.filename}.")

            # Score the resume against the criteria
            scores = score_resume(text, criteria)
            total_score = sum(scores.values())

            # Add the result to the list
            results.append({
                "Candidate Name": file.filename,
                **scores,
                "Total Score": total_score
            })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing {file.filename}: {str(e)}")
        

    #Convert results to a DataFrame
    df = pd.DataFrame(results)

    # Save DataFrame to an Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Scores")
    output.seek(0)

    # Return the Excel file as a downloadable response
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=resume_scores.xlsx"}
    )
