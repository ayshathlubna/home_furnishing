# nlp_utils.py
import re

def parse_user_message(message):
    message = message.lower()
    min_price = None
    max_price = None
    keywords = []

    # Extract numbers
    numbers = [int(n) for n in re.findall(r'\d+', message)]

    if "less than" in message or "under" in message or "below" in message:
        if numbers:
            max_price = numbers[0]

    elif "more than" in message or "above" in message or "over" in message:
        if numbers:
            min_price = numbers[0]

    elif "between" in message and "and" in message:
        if len(numbers) >= 2:
            min_price, max_price = numbers[0], numbers[1]

    elif numbers:
        # If just "products under 1000" or "1000 rupees"
        max_price = numbers[0]

    # Extract keywords (basic approach: remove numbers and price words)
    ignore_words = {"less", "more", "than", "under", "over", "between", "and", "above", "below", "products", "product", "price", "rs", "rupees"}
    keywords = [w for w in re.findall(r'\w+', message) if not w.isdigit() and w not in ignore_words]

    return {
        "min_price": min_price,
        "max_price": max_price,
        "keywords": keywords
    }
