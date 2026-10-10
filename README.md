# Tarjumi AI - AI Language Translation Tool

An AI language translation tool that I built for CodeAlpha Internship - Task 1. It translates text between 36 languages, detects the source language automatically, and lets you copy, listen to or download the result. The interface is a dark, futuristic dashboard with an animated globe, made with Streamlit and powered by the Google Gemini API.

## Project Overview
I wanted to build a translation tool that feels fast and polished, so I used the Google Gemini API for the translation and spent time on the interface and on handling errors properly. The app keeps the API key out of the code, asks Gemini for a structured JSON reply, and shows clear messages instead of crashing when something goes wrong.

## Problem Statement
People often need quick, accurate translations without switching between several tools. This project lets a user paste text, choose a language and get a translation in one place. It also detects the source language, and it explains problems (a missing key, a busy server, no internet) in plain words.

## Features
- 36 languages, including Tamil, Hindi, Telugu, Malayalam, Spanish, French, Japanese and more
- Automatic source-language detection
- Swap languages in one click
- Copy, Listen (text-to-speech) and Download .txt buttons for every result
- Recent translations with a "Reuse" button
- Animated globe background, glassmorphism panel and smooth animations
- Input validation: handles empty text, identical languages and text over 5000 characters
- Automatic fallback to another Gemini model when one is busy or unavailable
- Friendly error messages for a missing or invalid key, rate limits and connection problems
- The API key is read from a `.env` file, so it is never uploaded to GitHub
- Animations are switched off for users who prefer reduced motion
- Automated tests with pytest (Gemini is faked, so no key is needed)

## Technology Stack
| Area | Tools |
|------|-------|
| Language | Python 3.10+ (tested on Python 3.13) |
| UI | Streamlit |
| Translation | Google Gemini API (`google-genai`) |
| Configuration | python-dotenv (`.env` file) |
| Effects | Custom CSS, JavaScript canvas animation, browser speech synthesis |
| Testing | pytest |

## Architecture
```
User text
   -> Input validation          (empty, same language, 5000-character limit)
   -> Prompt building           (system instruction + text inside <text> tags)
   -> Gemini API call           (first available model, with automatic fallback)
   -> JSON reply parsing        (detected language + translation)
   -> Result card               (Copy / Listen / Download + recent history)
```
The translation logic and the interface live in `app.py`. Session state keeps the selected languages, the result and the history between interactions.

## How the Translation Works
1. **Prompting.** The text is sent inside `<text>` tags with a system instruction that tells Gemini to treat it only as content to translate and never as instructions. This protects the tool from text that tries to change its behaviour.

2. **Structured output.** Gemini is asked to reply with JSON that contains the detected language and the translation. The app parses it, and if the model ignores the format, it still shows the plain reply instead of failing.

3. **Model fallback.** The app uses `gemini-flash-latest` first. If a model is not found, rate-limited or temporarily unavailable, it tries the next one in the list before showing an error.

You can force a specific model by adding `GEMINI_MODEL=model-name` to your `.env` file.

## Project Structure
```
CodeAlpha_AI-Language-Translation-Tool/
|-- app.py                  # Streamlit UI + Gemini translation logic
|-- tests/
|   `-- test_app.py         # pytest smoke tests (Gemini is faked)
|-- assets/                 # Screenshots used in this README
|   |-- before-result.png
|   `-- after-result.png
|-- .streamlit/
|   `-- config.toml         # Dark theme (no secrets)
|-- run.bat                 # One-click setup and launch (Windows)
|-- requirements.txt
|-- pytest.ini
|-- .env.example            # Template for your own API key
|-- .gitignore
`-- README.md
```

## Installation
Get a free Gemini API key first: https://aistudio.google.com/app/apikey

**Windows (PowerShell):**
```powershell
git clone https://github.com/MohamedMusthafa07/CodeAlpha_AI-Language-Translation-Tool.git
cd CodeAlpha_AI-Language-Translation-Tool
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```
Then open `.env` and paste your key: `GEMINI_API_KEY=your_key_here`

**Easier way on Windows:** double-click `run.bat`. The first time, it creates the virtual environment, installs the requirements and opens `.env` so you can paste your key.

**macOS / Linux:**
```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
cp .env.example .env
```

Tip: use Python 3.12 or 3.13. Very new Python versions may not have pre-built packages for all dependencies yet.

## How to Run
```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```
The app opens at http://localhost:8501.

## How to Test
```powershell
.\.venv\Scripts\python.exe -m pytest -q
```
Expected result: `3 passed`. The tests use a fake Gemini client, so they need no API key and no internet connection.

## Example Texts
- Good morning, how are you? (English to Tamil)
- Where is the nearest railway station? (English to Hindi)
- Thank you for your help. (English to Japanese)
- hello (English to Malayalam)

## Error Handling
The tool never shows a raw error. It replies with a short message instead:

| Situation | What the user sees |
|-----------|--------------------|
| No text entered | "Type or paste some text to translate." |
| Same source and target language | "Choose two different languages." |
| Missing API key | A message asking for `GEMINI_API_KEY` in the `.env` file |
| Invalid API key | "Gemini rejected the API key..." |
| Rate limit reached | "Gemini rate limit or quota reached. Wait a minute and try again." |
| Gemini server busy | The app tries another model, then shows "Gemini is temporarily unavailable" |
| No internet | "Could not reach Gemini. Check your internet connection..." |

## Performance Considerations
- Each translation needs only one API call, with a 45-second timeout.
- The text limit of 5000 characters keeps requests fast and within the free tier.
- The background animation uses a lightweight canvas and pauses for users who prefer reduced motion.
- Recent translations are kept in session state, so reusing one needs no new API call.

## Screenshots
**Before the result**

![Before result](Before Translation.png)

**After the result**

![After result](After Translation.png)

## What I Learned
- Calling the Gemini API and asking for structured JSON output
- Handling API errors (invalid key, rate limits, busy servers, retired models) with clear messages
- Building a custom-styled Streamlit interface with CSS and JavaScript animations
- Keeping secrets out of source code and out of GitHub
- Testing an app without a real API key by faking the API client
- Publishing and documenting a project on GitHub

## Future Improvements
- Translate whole documents (PDF and Word files)
- Speech-to-text input for spoken translation
- Export the full translation history
- Favourite language pairs
- Docker image and CI workflow

## Internship Information
Developed as part of the CodeAlpha Internship - Task 1: Language Translation Tool.

## Author
**A. Mohamed Musthafa**

- GitHub: [MohamedMusthafa07](https://github.com/MohamedMusthafa07)
- LinkedIn: [mohamedmusthafa07](https://www.linkedin.com/in/mohamedmusthafa07)