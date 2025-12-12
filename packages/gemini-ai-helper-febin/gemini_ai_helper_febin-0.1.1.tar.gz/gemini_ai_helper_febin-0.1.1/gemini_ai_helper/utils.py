import re

def clean_text(text):
    text= text.strip()
    text=re.sub(r"\s+", " ", text)
    return text
