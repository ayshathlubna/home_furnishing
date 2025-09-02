from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Instruction-tuned model for chat (small for local use)
MODEL_NAME = "bigscience/bloomz-560m"  

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

def get_hf_response(user_message, chat_history=None, max_tokens=60):
    """
    Generate a friendly, concise response using Hugging Face model.
    chat_history: list of previous messages ["User: ...", "Bot: ..."]
    """
    try:
        # Build conversation prompt
        history_text = "\n".join(chat_history) if chat_history else ""
        prompt = f"{history_text}\nUser: {user_message}\nBot:"

        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=True,
            top_p=0.9,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id
        )
        reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
        reply = reply.split("Bot:")[-1].strip()
        return reply if reply else "Sorry, I couldn't generate a response."
    except Exception:
        return "Sorry, I couldn't process that."
