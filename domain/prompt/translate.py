from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def translate_prompt(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Translate the following English text into a natural, listener-friendly Korean sentence, as if describing the mood or story of a song to a music listener."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=200,
            temperature=0.5,
        )

        translated = response.choices[0].message.content.strip()
        return translated

    except Exception as e:
        print(f"[번역 실패] {e}")
        return prompt
