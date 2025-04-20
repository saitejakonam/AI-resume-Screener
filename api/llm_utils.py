import os
import google.generativeai as genai
import json
import re
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-pro")

# Prompt template
prompt_template = """
You are an AI model trained to extract detailed resume data in a structured JSON format.
Only return fields that are present and populated in the resume. Do not include fields with null, empty, or placeholder values (e.g., 'N/A', 'Not mentioned').

Extract the following fields from the resume provided below with the same keys mentioned and proper values:
1. 'FullName'
2. 'Email Address'
3. 'Phone Number'
4. 'Location' (City, State)
5. 'Years of Experience' (calculated based on work history)
6. Work Experience: list of objects with the following keys:
   - jobTitle (string)
   - company (string)
   - location (string)
   - duration (string)
7. 'Skills': list of strings (both technical and soft skills)
8. Education: list of objects with the following keys:
   - degree (string)
   - university (string)
   - GPA (string, if available)
   - graduation year (string, if available)
9. Projects: list of objects with the following keys:
    - title (string)
    - description (string)
10. Achievements: list of strings (if any)
11. Certifications: list of strings (if any)
12. LinkedIn Profile: string (if available)
13. GitHub or Portfolio: string (if available)
14. Activities: list of strings (if any)
15. Additional Information: list of strings (if any)

Return the result strictly in JSON format.

Resume:
"""

def extract_candidate_metadata(resume_text: str) -> dict:
    try:
        full_prompt = prompt_template + resume_text
        response = model.generate_content(full_prompt)

        print("📨 Raw Gemini Response:")
        print("-" * 40)
        print(response.text.strip())

        # Extract JSON between ```json ... ``` if present
        match = re.search(r"```json(.*?)```", response.text.strip(), re.DOTALL)
        json_text = match.group(1).strip() if match else response.text.strip()

        print("🧼 Cleaned JSON Candidate Output:")
        print(json_text)

        metadata = json.loads(json_text)

        print("✅ Parsed Metadata Output:")
        print(metadata)

        return metadata

    except Exception as e:
        print("[Gemini LLM] Error extracting metadata:", str(e))
        return {}
