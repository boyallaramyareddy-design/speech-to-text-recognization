from flask import Flask, render_template, request, jsonify
import os
import io
import json
import numpy as np
import soundfile as sf
from python_speech_features import mfcc
from math import sqrt
import sqlite3
import webbrowser

app = Flask(__name__)

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, 'enrollments.db')


def ensure_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS enrollments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        mfcc_json TEXT NOT NULL
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        confidence REAL,
        transcript TEXT
    )
    ''')
    conn.commit()
    conn.close()


def compute_embedding(wav_bytes):
    # wav_bytes: bytes of WAV file
    data, sr = sf.read(io.BytesIO(wav_bytes))
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)
    # compute MFCC and take mean over time as embedding
    mf = mfcc(data, samplerate=sr, numcep=13)
    emb = np.mean(mf, axis=0)
    return emb.tolist()


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/enroll', methods=['POST'])
def enroll():
    ensure_db()
    name = request.form.get('name')
    file = request.files.get('file')
    if not name or not file:
        return jsonify({'error': 'name and file required'}), 400
    wav_bytes = file.read()
    try:
        emb = compute_embedding(wav_bytes)
    except Exception as e:
        return jsonify({'error': 'failed to process audio', 'details': str(e)}), 500
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('INSERT OR REPLACE INTO enrollments (name, mfcc_json) VALUES (?, ?)', (name, json.dumps(emb)))
    conn.commit()
    conn.close()
    return jsonify({'status': 'enrolled', 'name': name})


@app.route('/recognize', methods=['POST'])
def recognize():
    ensure_db()
    file = request.files.get('file')
    transcript = request.form.get('transcript', '')
    if not file:
        return jsonify({'error': 'file required'}), 400
    wav_bytes = file.read()
    try:
        query_emb = compute_embedding(wav_bytes)
    except Exception as e:
        return jsonify({'error': 'failed to process audio', 'details': str(e)}), 500
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT name, mfcc_json FROM enrollments')
    rows = cur.fetchall()
    best = None
    best_score = -1.0
    for name, mfcc_json in rows:
        stored = json.loads(mfcc_json)
        score = cosine_similarity(query_emb, stored)
        if score > best_score:
            best_score = score
            best = name
    # store history
    cur.execute('INSERT INTO history (name, confidence, transcript) VALUES (?, ?, ?)', (best, float(best_score), transcript))
    conn.commit()
    conn.close()
    return jsonify({'speaker': best, 'score': float(best_score), 'transcript': transcript})


if __name__ == '__main__':
    ensure_db()
    url = 'http://127.0.0.1:5000'
    print(f'App starting — open {url} in your browser')
    try:
        webbrowser.open(url)
    except Exception:
        pass
    app.run(debug=True)
