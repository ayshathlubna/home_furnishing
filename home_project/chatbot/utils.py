import os
import requests
from dotenv import load_dotenv

load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = "tiiuae/falcon-7b-instruct"  # free conversational model


print("HF_API_KEY:", HF_API_KEY)  # make sure it prints your key


def get_hf_response(prompt):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 150, "temperature": 0.7}
    }
    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_MODEL}",
            headers=headers,
            json=payload,
            timeout=20
        )
        data = response.json()
        if "error" in data:
            return "Sorry, I am having trouble responding right now."
        return data[0]["generated_text"].split("Bot:")[-1].strip()
    except Exception as e:
        print("HF API Error:", e)
        return "Sorry, I am having trouble responding right now."
