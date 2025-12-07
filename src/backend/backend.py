import os
import re
import json
from openai import OpenAI

OPENROUTER_API_KEY = os.getenv("ASSESSLY_API_KEY")

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

def preprocess_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.,;:?!()\-\'\"]+', '', text)
    text = text.strip()
    return text

def generate_quiz_from_pdf(text: str, num_questions: int = 10, difficulty: str = "medium"):
    
    cleaned_text = preprocess_text(text)
    
    model_name = "openai/gpt-oss-20b:free"
    
    marks_instruction = "Assign exactly 1 mark to each question."

    prompt = f"""Create exactly {num_questions} multiple-choice questions with {difficulty} difficulty from the following text.

Text:
{cleaned_text}

Return ONLY a valid JSON array with this exact structure:
[
  {{
    "question": "Question text here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option A",
    "marks": 1
  }}
]

Requirements:
- Each question must have exactly 4 options
- The correct_answer must be one of the options exactly as written
- {marks_instruction}
- Return only the JSON array, no additional text
- Ensure proper JSON formatting"""
    
    try:
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a quiz generator that only returns valid JSON arrays."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        quiz_text = completion.choices[0].message.content
        
        if not quiz_text:
            return {"error": "No response from AI model"}
        
        quiz_text = quiz_text.strip()
        if quiz_text.startswith("```json"):
            quiz_text = quiz_text[7:]
        if quiz_text.startswith("```"):
            quiz_text = quiz_text[3:]
        if quiz_text.endswith("```"):
            quiz_text = quiz_text[:-3]
        quiz_text = quiz_text.strip()
        
        quiz_data = json.loads(quiz_text)
        
        if not isinstance(quiz_data, list):
            quiz_data = [quiz_data]
        
        return {"quiz_data": quiz_data}
        
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse quiz data: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}
