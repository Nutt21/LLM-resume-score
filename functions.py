import json
from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import List

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def score_resume(text: str, criteria: List[str]):
    scores = {}
    # Use OpenAI to evaluate the relevance of the criterion in the resume
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Evaluate the resume text against the given criteria and provide scores in JSON format. Make sure you are strict in evaluating."},
        {"role": "user", "content": f"Criteria: {json.dumps(criteria)}\nResume Text: {text}\nProvide scores in JSON format like this: {{\"criteria\": [\"criteria1\", \"criteria2\"], \"scores\": [score1, score2]}}"}
    ],
    response_format={"type": "json_object"}  # Ensure the response is in JSON format
)
    content = response.choices[0].message.content
    try:
        
        response_json = json.loads(content)
        # Extract scores and map them to criteria
        for criterion, score in zip(response_json["criteria"], response_json["scores"]):
            scores[criterion] = score
    except (json.JSONDecodeError, KeyError) as e:
        print("Error parsing OpenAI response:", e)
        # Default to 0 for all criteria if parsing fails
        scores = {criterion: 0 for criterion in criteria}
    return scores