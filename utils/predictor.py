import os
import re
from dotenv import load_dotenv

load_dotenv()

MIN_TOKENS = int(os.getenv("MIN_TOKEN_COUNT", "30"))

TRAIT_META = {
    "IE": {
        "left":  ("I", "Introversion", "🔋"),
        "right": ("E", "Extraversion", "🌐"),
    },
    "SN": {
        "left":  ("S", "Sensing",   "🔍"),
        "right": ("N", "Intuition", "💡"),
    },
    "TF": {
        "left":  ("T", "Thinking", "⚙️"),
        "right": ("F", "Feeling",  "❤️"),
    },
    "JP": {
        "left":  ("J", "Judging",    "📋"),
        "right": ("P", "Perceiving", "🌊"),
    },
}

def count_tokens(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))

def validate_input(text: str):
    """Returns (is_valid: bool, token_count: int, message: str | None)"""
    stripped = text.strip()
    if not stripped:
        return False, 0, "⚠️ Please enter some text to analyse."
    n = count_tokens(stripped)
    if n < MIN_TOKENS:
        needed = MIN_TOKENS - n
        return False, n, (
            f"⚠️ Your input has **{n} tokens**. "
            f"Please add at least **{needed} more word(s)** "
            f"(minimum: {MIN_TOKENS}) for a reliable prediction."
        )
    return True, n, None

def predict_mbti(text, tfidf, models):
    X = tfidf.transform([text]).toarray()
    results = {}

    for trait, model in models.items():
        proba = model.predict_proba(X)[0]

        if trait == "IE":
            results["I"], results["E"] = proba[0]*100, proba[1]*100
        elif trait == "SN":
            results["S"], results["N"] = proba[0]*100, proba[1]*100
        elif trait == "TF":
            results["T"], results["F"] = proba[0]*100, proba[1]*100
        elif trait == "JP":
            results["J"], results["P"] = proba[0]*100, proba[1]*100

    return results

def get_mbti_type(result):
    return (
        ("I" if result["I"] >= result["E"] else "E") +
        ("S" if result["S"] >= result["N"] else "N") +
        ("T" if result["T"] >= result["F"] else "F") +
        ("J" if result["J"] >= result["P"] else "P")
    )