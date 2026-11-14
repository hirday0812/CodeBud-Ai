
import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key) if api_key else None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    if client is None:
        return jsonify({"error": "Gemini API key not configured."}), 500

    data = request.get_json(silent=True) or {}

    code = data.get("code", "").strip()
    language = data.get("language", "").strip()
    task = data.get("task", "").strip()

    if not code:
        return jsonify({"error": "Please enter some code first."}), 400

    if language not in ["Python", "C", "C++", "Java"]:
        return jsonify({"error": "Please select a valid programming language."}), 400

    if task not in ["Explain Code", "Find Errors", "Improve Code"]:
        return jsonify({"error": "Please select a valid analysis option."}), 400

    if len(code) > 12000:
        return jsonify({"error": "Code is too long. Please keep it under 12,000 characters."}), 400

    prompt = f"""
You are CodeBuddy AI, a helpful programming assistant.

Programming language: {language}
User's request: {task}

Analyze the following code.

Instructions:
- Use simple language suitable for a beginner.
- Be accurate and explain your reasoning clearly.
- If there are errors, identify the relevant lines where possible.
- Do not invent errors if the code is correct.
- Format your response using clear headings and bullet points.
- If improving code, explain the important changes.

Code:
{code}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        return jsonify({
            "result": response.text or "Gemini returned an empty response."
        })

    except Exception as e:
        print("Gemini API error:", str(e))
        return jsonify({
            "error": "Unable to analyze your code right now. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
