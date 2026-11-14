
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
Act as a programming teacher explaining code to a beginner.

Do not greet the user or introduce yourself.
Start directly with the explanation.

Follow this exact format:

## What This Code Does
Explain the main purpose in 1-2 simple sentences.

## Line-by-Line Explanation
Explain every important line separately.
Show the original line of code followed by its meaning.
Use simple words and beginner-friendly examples.

## How the Code Works
Explain the complete execution flow in numbered steps.

## Expected Output
Show the output in a code block.
If the output depends on user input, explain that.

Keep the explanation clear and concise.
Do not repeat the same information.
Never invent output.
""",

        


  "Improve Code": """
Act as an experienced programming mentor.

Do not greet the user or introduce yourself.
Start directly with the improved code.

Follow this exact format:

## Improved Code
Provide the complete corrected and improved program
inside a code block using the selected programming language.

## What Was Improved
List the important changes made to the original code.

## Why It's Better
Explain how the changes improve readability,
efficiency or programming practices.

## Expected Output
Show the expected output in a code block, if applicable.

Important rules:
- Preserve the original functionality.
- Do not remove important features.
- Do not introduce unnecessary complexity.
- Use beginner-friendly techniques.
- Never claim an improvement that was not made.
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
