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

analyzeBtn.addEventListener("click", async () => {
  const code = codeInput.value.trim();
  const selectedLanguage = language.value;
  const selectedTask = task.value;

  if (!code) {
    result.textContent = "Please enter some code before starting the analysis.";
    return;
  }

  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "Analyzing...";

  result.innerHTML = `
        <div class="loading-state">
            <div class="loading-spinner"></div>
            <p class="loading-text">Analyzing your code...</p>
        </div>
    `;

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        code: code,
        language: selectedLanguage,
        task: selectedTask,
      }),
    });

    let data;

    try {
      data = await response.json();
    } catch {
      throw new Error(
        "The server returned an invalid response. Please try again.",
      );
    }

    if (!response.ok) {
      throw new Error(
        data.error || "We couldn't analyze your code. Please try again.",
      );
    }

    if (!data.result || !data.result.trim()) {
      throw new Error("The AI returned an empty response. Please try again.");
    }

    result.replaceChildren();

    const heading = document.createElement("h3");
    heading.textContent = "Analysis Result";

    const output = document.createElement("div");
    const formattedHTML = marked.parse(data.result);
    output.innerHTML = DOMPurify.sanitize(formattedHTML);

    // Highlight the error section in red
    const errorHeading = [...output.querySelectorAll("h1, h2, h3, h4")].find(
      (h) => h.textContent.includes("Error Found"),
    );

    if (errorHeading) {
      const errorBox = document.createElement("div");
      errorBox.className = "error-highlight";

      const parent = errorHeading.parentNode;
      parent.insertBefore(errorBox, errorHeading);

      let current = errorHeading;

      while (current) {
        if (current !== errorHeading && /^H[1-4]$/.test(current.tagName)) {
          break;
        }

        const next = current.nextElementSibling;
        errorBox.appendChild(current);
        current = next;
      }
    }

    // Create copy button
    const copyBtn = document.createElement("button");
    copyBtn.className = "copy-btn";
    copyBtn.textContent = "Copy Result";

    copyBtn.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(output.innerText);

        copyBtn.textContent = "Copied!";

        setTimeout(() => {
          copyBtn.textContent = "Copy Result";
        }, 2000);
      } catch (error) {
        copyBtn.textContent = "Copy failed";
      }
    });

    result.appendChild(heading);
    result.appendChild(copyBtn);
    result.appendChild(output);
  } catch (error) {
    console.error("Analysis error:", error);

    let message = error.message;

    if (error instanceof TypeError || message.includes("Failed to fetch")) {
      message =
        "Unable to connect to the server. Please check your internet connection and try again.";
    }

    result.replaceChildren();

    const errorBox = document.createElement("div");
    errorBox.className = "friendly-error";

    const errorHeading = document.createElement("h3");
    errorHeading.textContent = "Something went wrong";

    const errorMessage = document.createElement("p");
    errorMessage.textContent = message;

    errorBox.appendChild(errorHeading);
    errorBox.appendChild(errorMessage);
    result.appendChild(errorBox);
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "Analyze Code";
  }
});
