import json
import os
import uuid

import requests
from flask import (
    Flask, Response, jsonify, render_template,
    request, session, stream_with_context
)

import db

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


def current_session_id():
    if "chat_id" not in session:
        session["chat_id"] = uuid.uuid4().hex
    return session["chat_id"]


@app.get("/")
def index():
    current_session_id()
    return render_template("index.html")


@app.get("/history")
def history():
    return jsonify(db.get_history(current_session_id(), 20))


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    if not isinstance(message, str) or not 1 <= len(message.strip()) <= 1000:
        return jsonify(error="Viestin pituus saa olla 1–1000 merkkiä."), 400

    sid = current_session_id()
    db.save_message(sid, "user", message.strip())
    messages = db.get_history(sid, 10)

    def generate():
        answer = []

        try:
            with requests.post(
                "http://127.0.0.1:11434/api/chat",
                json={
                    "model": "qwen2.5:0.5b",
                    "messages": messages,
                    "stream": True,
                },
                stream=True,
                timeout=(10, 180),
            ) as response:
                response.raise_for_status()

                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        piece = chunk.get("message", {}).get("content", "")
                        if piece:
                            answer.append(piece)
                            yield piece

            if answer:
                db.save_message(sid, "assistant", "".join(answer))

        except Exception:
            app.logger.exception("Ollama error")
            yield "\n[Tekoälypalvelussa tapahtui virhe.]"

    return Response(
        stream_with_context(generate()),
        mimetype="text/plain",
        headers={"X-Accel-Buffering": "no", "Cache-Control": "no-cache"},
    )
