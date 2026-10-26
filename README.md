# 🩺 DiaBuddy AI

An AI-powered diabetes education and nutrition assistant.

## About

DiaBuddy AI is an educational prototype built with Python, Flask, HTML, CSS, JavaScript, and Ollama. It provides general diabetes education and balanced meal suggestions through a conversational interface.

## Features

* AI-powered chat interface
* Conversation context support
* Diabetes education and nutrition information
* Balanced meal suggestions
* Locally running AI model through Ollama

## Technology Stack

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Python and Flask
* **AI runtime:** Ollama
* **Model:** `niharika:latest`

## Run Locally

### 1. Install Python dependencies

```bash
pip install flask
```

### 2. Start Ollama

Make sure Ollama is installed and running, and the configured model is available.

```bash
ollama list
```

If your model is missing, use the appropriate model installation instructions for your Ollama setup.

### 3. Start the application

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Medical Disclaimer

DiaBuddy AI is an educational prototype, not a medical device. It does not diagnose conditions or prescribe or adjust insulin or medication doses. Consult a qualified healthcare professional for personal medical decisions.

## Project Status

Educational prototype under development.
