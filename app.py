
import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
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
    print("Selected task received:", task)

    if not code:
        return jsonify({"error": "Please enter some code first."}), 400

    if language not in ["Python", "C", "C++", "Java"]:
        return jsonify({"error": "Invalid programming language."}), 400

    if task not in ["Explain Code", "Find Errors", "Improve Code"]:
        return jsonify({"error": "Invalid task selected."}), 400

    if len(code) > 12000:
        return jsonify({"error": "Code is too long."}), 400

    task_instructions = {
      "Find Errors": """
Act as a precise code debugger.

Start directly with the error. No greeting or introduction.

Follow this exact format:

## 🔴 Error Found
**Error:** Write the exact error name.
**Line:** Mention the line number if it can be identified.
**Problematic Code:**
Show the line of code causing the error.

## Why This Error Occurs
Explain the reason in simple language.

## Step-by-Step Explanation
Explain how the program reaches this error.

## How to Fix It
Show the corrected code.

## Expected Output
Show the output after fixing the error.

If there are multiple errors, list them separately.
Never invent errors or line numbers.
If no errors are found, clearly state that.
""",
        "Explain Code": """
Explain the code line by line.
Describe what each statement does.
Explain the overall logic and expected output.
Use simple language for beginners.
""",

        


        "Improve Code": """
Review the code for readability, efficiency,
structure and good programming practices.

Provide an improved version.
Explain the important changes.
Preserve the original functionality.
"""
    }

    prompt = f"""
You are a precise programming assistant.

Do not introduce yourself.
Do not greet the user.
Do not repeat the user's request.
Start directly with the answer.
Avoid phrases such as "Let's look at your code"
or "Here is the breakdown".

Programming language: {language}
User's request: {task}

{task_instructions[task]}

Use simple language suitable for beginners.
Format your response using headings, bullet points and code blocks.

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
