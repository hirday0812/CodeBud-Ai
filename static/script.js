// =================================
// ELEMENTS
// =================================

const codeInput = document.getElementById("codeInput");
const charCount = document.getElementById("charCount");

const clearBtn = document.getElementById("clearBtn");
const analyzeBtn = document.getElementById("analyzeBtn");

const result = document.getElementById("result");

const language = document.getElementById("language");
const task = document.getElementById("task");

const themeToggle = document.getElementById("themeToggle");
const themeIcon = document.getElementById("themeIcon");

const fileType = document.getElementById("fileType");

// =================================
// LIGHT AND DARK MODE
// =================================

const savedTheme = localStorage.getItem("codebuddy-theme") || "light";

document.documentElement.setAttribute("data-theme", savedTheme);

updateThemeIcon();

themeToggle.addEventListener("click", function () {
  const currentTheme = document.documentElement.getAttribute("data-theme");

  const newTheme = currentTheme === "light" ? "dark" : "light";

  document.documentElement.setAttribute("data-theme", newTheme);

  localStorage.setItem("codebuddy-theme", newTheme);

  updateThemeIcon();
});

function updateThemeIcon() {
  const currentTheme = document.documentElement.getAttribute("data-theme");

  if (currentTheme === "light") {
    themeIcon.textContent = "☾";
    themeToggle.title = "Switch to dark mode";
  } else {
    themeIcon.textContent = "☀";
    themeToggle.title = "Switch to light mode";
  }
}

// =================================
// CHARACTER COUNTER
// =================================

codeInput.addEventListener("input", function () {
  charCount.textContent = codeInput.value.length + " characters";
});

// =================================
// LANGUAGE LABEL
// =================================

function updateLanguageLabel() {
  fileType.textContent = language.value.toUpperCase();
}

language.addEventListener("change", updateLanguageLabel);

// =================================
// CLEAR CODE
// =================================

clearBtn.addEventListener("click", function () {
  codeInput.value = "";

  charCount.textContent = "0 characters";

  codeInput.focus();
});

// =================================
// ANALYZE BUTTON
// TEMPORARY FRONTEND TEST
// =================================

analyzeBtn.addEventListener("click", function () {
  const code = codeInput.value.trim();

  const selectedLanguage = language.value;

  const selectedTask = task.value;

  if (code === "") {
    result.textContent = "Please enter some code before analysing.";

    return;
  }

  const heading = document.createElement("h3");
  heading.textContent = "Frontend test successful";

  const languageText = document.createElement("p");
  languageText.textContent = "Programming language: " + selectedLanguage;

  const taskText = document.createElement("p");
  taskText.textContent = "Analysis type: " + selectedTask;

  const message = document.createElement("p");
  message.textContent =
    "Your code has been received. Gemini integration will be added next.";

  result.replaceChildren(heading, languageText, taskText, message);
});
