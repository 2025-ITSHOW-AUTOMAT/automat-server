from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# def translate_prompt(prompt: str) -> str:
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",  # 혹은 "gpt-3.5-turbo" 등
#             messages=[
#                 {
#                     "role": "system",
#                     "content": "Translate the following English text into natural Korean for user display."
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             max_tokens=200,
#             temperature=0.5,
#         )

#         translated = response.choices[0].message.content.strip()
#         return translated

#     except Exception as e:
#         print(f"[번역 실패] {e}")
#         return prompt  # 실패 시 원문 그대로 반환

def translate_prompt(prompt: str) -> str:
    return f"[번역된] {prompt}"
