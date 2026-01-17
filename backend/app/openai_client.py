from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key = OPENAI_API_KEY)

def generate_insight(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model = "gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a football analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature = 0.4
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"OpenAI error: {str(e)}"