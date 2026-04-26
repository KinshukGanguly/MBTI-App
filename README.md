# 🧠 MBTI Personality Predictor

Streamlit application that runs four stacked ensemble classifiers (I/E, S/N, T/F, J/P)
on user text using a shared TF-IDF vectorizer, then visualises per-axis probabilities as
a diverging horizontal bar chart.

---

## Project Structure

```
mbti_app/
├── app.py                  ← Streamlit entry point
├── .env                    ← Your local config (never commit this)
├── .env.example            ← Template — commit this
├── requirements.txt        ← Pinned dependencies
├── utils/
│   ├── __init__.py
│   ├── model_loader.py     ← Env-aware joblib loader + path validation
│   └── predictor.py        ← Token validation + predict_mbti pipeline
└── README.md
```

---

## 1 · Virtual Environment Setup (Windows)

### Create & activate

```powershell
# Navigate to the project folder
cd "C:\path\to\mbti_app"

# Create the venv (Python 3.10+ recommended)
python -m venv venv

# Activate it
venv\Scripts\activate
```

Your terminal prompt should now show `(venv)`.

### Install dependencies

```powershell
pip install -r requirements.txt
```

---


## Model weights drive link : [Link](https://drive.google.com/drive/folders/1EOD38FBXzWY5-hrMoOUuKh0EHj2hbMqt?usp=drive_link)

### download the model weights and place the same in the repository. All file names are set accordingly


## 2 · Configure .env

```powershell
# Copy the template
copy .env.example .env
```

Open `.env` in any text editor and update the paths:

```
MODEL_DIR=C:\Users\YourName\OneDrive\Desktop\mbti app\models
VECTORIZER_DIR=C:\Users\YourName\OneDrive\Desktop\mbti app\vectorizer
MODEL_IE=stack_model_EI.pkl
MODEL_SN=stack_model_SN.pkl
MODEL_TF=stack_model_TF.pkl
MODEL_JP=stack_model_JP.pkl
VECTORIZER=tfidf_vectorizer.pkl
MIN_TOKEN_COUNT=30
```

> **.env is gitignored** — never push it. Share `.env.example` instead.

---

## 3 · Run the App

```powershell
# With venv active:
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## 4 · Sharing with a Friend — pip freeze Workflow

### Your machine (producer)

```powershell
# With venv active and all packages installed:
pip freeze > requirements.txt
```

This pins every transitive dependency with exact versions — fully reproducible.

### Friend's machine (consumer)

```powershell
# Clone / copy the project folder
cd "path\to\mbti_app"

# Create their own venv
python -m venv venv
venv\Scripts\activate

# Install exactly what you pinned
pip install -r requirements.txt

# Set up their own .env
copy .env.example .env
# (then edit .env with their own model paths)

# Run
streamlit run app.py
```

---

## 5 · Deactivate / Clean Up

```powershell
# Deactivate venv
deactivate

# Delete venv entirely if needed (does not affect project files)
rmdir /s /q venv
```

---

## 6 · Environment Variables Reference

| Variable         | Description                              | Default              |
|------------------|------------------------------------------|----------------------|
| `MODEL_DIR`      | Folder containing the four .pkl models   | *(required)*         |
| `VECTORIZER_DIR` | Folder containing the vectorizer .pkl    | *(required)*         |
| `MODEL_IE`       | Filename for the I/E stacked model       | `stack_model_EI.pkl` |
| `MODEL_SN`       | Filename for the S/N stacked model       | `stack_model_SN.pkl` |
| `MODEL_TF`       | Filename for the T/F stacked model       | `stack_model_TF.pkl` |
| `MODEL_JP`       | Filename for the J/P stacked model       | `stack_model_JP.pkl` |
| `VECTORIZER`     | Filename for the TF-IDF vectorizer       | `tfidf_vectorizer.pkl` |
| `MIN_TOKEN_COUNT`| Minimum word count for valid prediction  | `30`                 |
| `APP_TITLE`      | Browser tab + app heading title          | `MBTI Personality Predictor` |
| `APP_ICON`       | Emoji icon shown in tab and header       | `🧠`                 |

---

## 7 · Notes on Token Threshold

`MIN_TOKEN_COUNT=50` is a conservative lower bound. Research on MBTI text classification
(e.g., Gjurkovic & Snajder 2018, Acheampong et al. 2021) consistently shows prediction
quality degrades below ~50 words due to sparse TF-IDF feature activation. For production,
consider raising this to **50–100** depending on your training corpus average length.
