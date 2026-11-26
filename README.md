# CodeBuddy AI

**An AI-powered programming assistant that helps developers understand, debug, and improve code.**

[Live Website](https://codebud-ai-7pig.onrender.com/) · [GitHub Repository](https://github.com/hirday0812/CodeBud-Ai)

## Overview

CodeBuddy AI is a web-based programming assistant powered by Google's Gemini AI. It helps students and developers understand code, identify programming errors, and improve code quality through an easy-to-use interface.

Users can select a programming language, paste their code, choose an analysis task, and receive an AI-generated response.

## Features

- **Explain Code:** Provides beginner-friendly explanations of code, including its logic and working.
- **Find Errors:** Identifies programming errors and explains possible corrections.
- **Improve Code:** Suggests improvements for readability, efficiency, and coding practices.
- **Multiple Languages:** Supports Python, C, C++, and Java.
- **Light and Dark Themes:** Offers a choice of interface themes.
- **Copy Results:** Allows users to copy AI-generated responses.
- **Clear Editor:** Quickly clears the code editor and previous results.
- **Responsive Interface:** Works on desktop, tablet, and mobile screens.
- **Error Handling:** Displays understandable messages for invalid input and connection issues.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web framework |
| Google Gemini AI | Code analysis and generation |
| HTML | Page structure |
| CSS | Styling and responsive design |
| JavaScript | Frontend interactions |
| Marked.js | Markdown rendering |
| DOMPurify | Sanitizing rendered HTML |
| Gunicorn | Production WSGI server |
| Render | Cloud deployment |

## Project Structure

```text
CodeBudAi/
│
├── app.py
├── test_gemini.py
├── requirements.txt
├── .gitignore
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/hirday0812/CodeBud-Ai.git
cd CodeBud-Ai
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your own API key from Google AI Studio.

**Important:** Never upload your `.env` file or expose your API key publicly.

### 6. Run the application

```bash
python app.py
```

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

## How to Use

1. Open CodeBuddy AI.
2. Select a programming language.
3. Choose Explain Code, Find Errors, or Improve Code.
4. Paste your source code into the editor.
5. Click **Analyze Code**.
6. Read the generated analysis.
7. Copy the result if required.

## Deployment

The application is deployed on Render and connected to the GitHub repository.

**Live URL:** https://codebud-ai-7pig.onrender.com/

The Gemini API key is configured as an environment variable on the hosting platform.

## Security

- API credentials are stored in environment variables.
- The `.env` file is excluded through `.gitignore`.
- AI-generated Markdown is sanitized using DOMPurify before being displayed.

## Future Improvements

- Support for additional programming languages.
- Code execution in a secure sandbox.
- User accounts and saved analysis history.
- Downloadable code explanations and reports.
- More detailed debugging suggestions.

## Author

Developed as a Generative AI mini-project.

**GitHub:** https://github.com/hirday0812

---

*CodeBuddy AI — Understand code. Find errors. Write better programs.*