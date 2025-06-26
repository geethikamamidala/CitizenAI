
def analyze_sentiment(text):
    text = text.lower()
    if any(word in text for word in ["good", "great", "happy", "love"]):
        return "Positive"
    elif any(word in text for word in ["bad", "poor", "hate", "angry"]):
        return "Negative"
    else:
        return "Neutral"
