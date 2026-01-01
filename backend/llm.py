# import os
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()

# client = OpenAI(
#   api_key=os.getenv("OPENAI_API_KEY")
# )

# def generate_answer(context: str, question: str) -> str:
#     prompt = f"""
# You are a helpful assistant.
# Answer ONLY using the context below.
# If the answer is not present, say:
# "The answer is not available in the provided documents."

# Context:
# {context}

# Question:
# {question}
# """

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0
#     )

#     return response.choices[0].message.content.strip()


#  for ollama

import ollama

def generate_answer(context: str, question: str) -> str:
    prompt = f"""
You are a helpful assistant.
Answer ONLY using the context below.
If the answer is not present, say:
"The answer is not available in the provided documents."

Context:
{context}

Question:
{question}
"""

    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"].strip()
