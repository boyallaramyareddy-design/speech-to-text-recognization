<<<<<<< HEAD
# speech-to-text-recognization
=======
# Speech-to-Text with Team Speaker Recognition (Local Prototype)

This is a small Flask demo that lets you enroll short voice samples for team members and then recognize who is speaking from new recordings.

What it does
- Enroll: record a short WAV sample and assign a name. The server stores a simple MFCC-based embedding in a local SQLite database.
- Recognize: record audio; the client also captures a browser transcript (via Web Speech API) and sends audio + transcript to the server. The server compares MFCC embeddings and returns the best-matching name and confidence.

# speech-to-text-recognization

Speech-to-Text with Team Speaker Recognition (Local Prototype)

This is a small Flask demo that lets you enroll short voice samples for team members and then recognize who is speaking from new recordings.

What it does
- Enroll: record a short WAV sample and assign a name. The server stores a simple MFCC-based embedding in a local SQLite database.
- Recognize: record audio; the client also captures a browser transcript (via Web Speech API) and sends audio + transcript to the server. The server compares MFCC embeddings and returns the best-matching name and confidence.

Quick setup (Windows PowerShell)

1. Create and activate a virtual environment

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

# speech-to-text-recognization

Speech-to-Text with Team Speaker Recognition (Local Prototype)

This is a small Flask demo that lets you enroll short voice samples for team members and then recognize who is speaking from new recordings.

What it does
- Enroll: record a short WAV sample and assign a name. The server stores a simple MFCC-based embedding in a local SQLite database.
- Recognize: record audio; the client also captures a browser transcript (via Web Speech API) and sends audio + transcript to the server. The server compares MFCC embeddings and returns the best-matching name and confidence.

Quick setup (Windows PowerShell)

1. Create and activate a virtual environment

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

# speech-to-text-recognization

Speech-to-Text with Team Speaker Recognition (Local Prototype)

This is a small Flask demo that lets you enroll short voice samples for team members and then recognize who is speaking from new recordings.

What it does
- Enroll: record a short WAV sample and assign a name. The server stores a simple MFCC-based embedding in a local SQLite database.
- Recognize: record audio; the client also captures a browser transcript (via Web Speech API) and sends audio + transcript to the server. The server compares MFCC embeddings and returns the best-matching name and confidence.

Quick setup (Windows PowerShell)

1. Create and activate a virtual environment

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

3. Run the app

```powershell
py -3 app.py
```

The app will attempt to open http://127.0.0.1:5000 in your default browser and print the URL in the terminal.

Notes & limitations
- This is a prototype: speaker recognition uses MFCC averages and cosine similarity. It's simple and works for small sets of speakers with clean recordings, but it's not robust for production use. Consider Resemblyzer or neural speaker embeddings for better accuracy.
- The client encodes WAV in the browser (no ffmpeg required).
- Transcription uses the browser Web Speech API (webkitSpeechRecognition) — it runs locally in the browser and is sent to the server along with audio. The server does not perform heavy ASR.
- For better server-side transcription, integrate a cloud API (OpenAI/Google) or Whisper locally (requires PyTorch and ffmpeg).

Next improvements
- Add enrollment quality checks and allow multiple enrollment samples per person.
- Replace MFCC averaging with a proper embedding model.
- Add UI to view stored enrollments and recognition history.

If you want, I can create the virtualenv, install packages automatically, and run a smoke test now.
