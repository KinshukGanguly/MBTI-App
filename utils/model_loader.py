import os
import joblib
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

def load_model(path: str):
    if path is None:
        raise ValueError("Model path is None. Check your .env file.")
    full_path = BASE_DIR / path
    if not full_path.exists():
        raise FileNotFoundError(
            f"File not found: {full_path}\n"
            f"BASE_DIR resolved to: {BASE_DIR}\n"
            "Check your .env paths and folder structure."
        )
    return joblib.load(full_path)

def load_all_models():
    tfidf_path = os.getenv("TFIDF_PATH")

    model_paths = {
        'IE': os.getenv("MODEL_IE"),
        'SN': os.getenv("MODEL_SN"),
        'TF': os.getenv("MODEL_TF"),
        'JP': os.getenv("MODEL_JP")
    }

    if not tfidf_path:
        raise ValueError("TFIDF_PATH not found in .env")

    for key, path in model_paths.items():
        if not path:
            raise ValueError(f"{key} model path missing in .env")

    tfidf = load_model(tfidf_path)
    models = {trait: load_model(path) for trait, path in model_paths.items()}

    return tfidf, models