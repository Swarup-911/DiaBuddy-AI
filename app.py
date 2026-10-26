
from flask import Flask, request, jsonify, send_from_directory
import urllib.request
import urllib.error
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL_NAME = "niharika:latest"

SYSTEM_PROMPT = """
You are DiaBuddy, an AI assistant providing general diabetes
education and nutrition information.

Rules:
- Explain glucose readings cautiously and consider measurement timing.
- Individual glucose targets differ. Never diagnose based on one reading.
- Suggest balanced meal ideas based on dietary preferences.
- Ask for missing context when needed.
- Never prescribe or change insulin doses or medication.
- Never promise a specific glucose result from a food or meal.
- Do not claim to be a doctor.
- For severe symptoms or urgent situations, advise appropriate medical care.
- Use simple, supportive language.
- Suggest practical, culturally appropriate foods.
- Use the conversation history to understand follow-up questions.
- Do not invent personal details that the user has not shared.
"""


@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "app": "DiaBuddy",
        "model": MODEL_NAME
    })


@app.route("/api/ask", methods=["POST"])
def ask_ai():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Please send a valid JSON request."}), 400

    message = data.get("message", "")
    history = data.get("history", [])

    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "Please enter a question."}), 400

    if len(message) > 4000:
        return jsonify({
            "error": "Please keep your message under 4000 characters."
        }), 400

    if not isinstance(history, list):
        return jsonify({
            "error": "Conversation history must be a list."
        }), 400

    # Keep only the most recent 20 messages.
    # Validate each message before sending it to Ollama.
    safe_history = []

    for item in history[-20:]:
        if not isinstance(item, dict):
            continue

        role = item.get("role")
        content = item.get("content")

        if role not in ("user", "assistant"):
            continue

        if not isinstance(content, str) or not content.strip():
            continue

        if len(content) > 4000:
            continue

        safe_history.append({
            "role": role,
            "content": content.strip()
        })

    # Include the previous conversation and the current question.
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *safe_history,
        {"role": "user", "content": message.strip()}
    ]

    payload = {
        "model": MODEL_NAME,
        "stream": False,
        "messages": messages,
        "options": {"temperature": 0.3}
    }

    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        answer = result.get("message", {}).get("content", "")

        if not answer:
            return jsonify({
                "error": "The AI returned an empty response."
            }), 502

        return jsonify({"answer": answer})

    except urllib.error.HTTPError as error:
        return jsonify({
            "error": f"Ollama returned HTTP error {error.code}."
        }), 502

    except urllib.error.URLError:
        return jsonify({
            "error": "Could not connect to Ollama. Check that Ollama is running."
        }), 503

    except TimeoutError:
        return jsonify({
            "error": "The AI took too long to respond. Please try again."
        }), 504

    except (ValueError, KeyError):
        return jsonify({
            "error": "The AI returned an invalid response."
        }), 502


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

