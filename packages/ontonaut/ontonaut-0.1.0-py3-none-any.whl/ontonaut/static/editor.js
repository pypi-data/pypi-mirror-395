/**
 * Ontonaut Code Editor Widget
 * A clean, marimo-style code editor with custom execution backends
 */

function render({ model, el }) {
  // Create the main container
  const container = document.createElement("div");
  container.className = "ontonaut-container";

  // Create the editor section
  const editorSection = document.createElement("div");
  editorSection.className = "ontonaut-editor-section";

  // Create the textarea for code input
  const textarea = document.createElement("textarea");
  textarea.className = "ontonaut-editor";
  textarea.value = model.get("code");
  textarea.placeholder = model.get("placeholder");
  textarea.readOnly = model.get("read_only");
  textarea.spellcheck = false;

  // Add line numbers if enabled
  if (model.get("line_numbers")) {
    const lineNumbersContainer = document.createElement("div");
    lineNumbersContainer.className = "ontonaut-line-numbers";
    editorSection.appendChild(lineNumbersContainer);

    const updateLineNumbers = () => {
      const lines = textarea.value.split("\n").length;
      lineNumbersContainer.innerHTML = Array.from(
        { length: lines },
        (_, i) => `<div class="line-number">${i + 1}</div>`
      ).join("");
    };

    updateLineNumbers();
    textarea.addEventListener("input", updateLineNumbers);
  }

  editorSection.appendChild(textarea);

  // Create the toolbar
  const toolbar = document.createElement("div");
  toolbar.className = "ontonaut-toolbar";

  // Language indicator
  const langIndicator = document.createElement("span");
  langIndicator.className = "ontonaut-language";
  langIndicator.textContent = model.get("language");
  toolbar.appendChild(langIndicator);

  // Run button
  const runButton = document.createElement("button");
  runButton.className = "ontonaut-run-button";
  runButton.innerHTML = `
    <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
      <path d="M4 2v12l10-6z"/>
    </svg>
    <span>Run</span>
  `;
  runButton.onclick = () => {
    model.send({ type: "execute", code: textarea.value });
  };
  toolbar.appendChild(runButton);

  // Clear button
  const clearButton = document.createElement("button");
  clearButton.className = "ontonaut-clear-button";
  clearButton.textContent = "Clear";
  clearButton.onclick = () => {
    textarea.value = "";
    model.set("code", "");
    model.save_changes();
  };
  toolbar.appendChild(clearButton);

  // Create the output section
  const outputSection = document.createElement("div");
  outputSection.className = "ontonaut-output-section";

  const outputLabel = document.createElement("div");
  outputLabel.className = "ontonaut-output-label";
  outputLabel.textContent = "Output";

  const outputContent = document.createElement("pre");
  outputContent.className = "ontonaut-output";
  outputContent.textContent = model.get("output") || "";

  const errorContent = document.createElement("pre");
  errorContent.className = "ontonaut-error";
  errorContent.textContent = model.get("error") || "";

  outputSection.appendChild(outputLabel);
  outputSection.appendChild(outputContent);
  outputSection.appendChild(errorContent);

  // Assemble the widget
  container.appendChild(toolbar);
  container.appendChild(editorSection);
  container.appendChild(outputSection);
  el.appendChild(container);

  // Sync code changes from frontend to backend
  textarea.addEventListener("input", () => {
    model.set("code", textarea.value);
    model.save_changes();
  });

  // Handle keyboard shortcuts
  textarea.addEventListener("keydown", (e) => {
    // Cmd/Ctrl + Enter to run
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
      e.preventDefault();
      runButton.click();
    }

    // Tab key for indentation
    if (e.key === "Tab") {
      e.preventDefault();
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      textarea.value = textarea.value.substring(0, start) + "    " + textarea.value.substring(end);
      textarea.selectionStart = textarea.selectionEnd = start + 4;
      model.set("code", textarea.value);
      model.save_changes();
    }
  });

  // Listen for changes from Python
  model.on("change:code", () => {
    if (textarea.value !== model.get("code")) {
      textarea.value = model.get("code");
    }
  });

  model.on("change:output", () => {
    outputContent.textContent = model.get("output");
    if (model.get("output")) {
      outputSection.style.display = "block";
    }
  });

  model.on("change:error", () => {
    errorContent.textContent = model.get("error");
    if (model.get("error")) {
      outputSection.style.display = "block";
    } else {
      errorContent.textContent = "";
    }
  });

  model.on("change:language", () => {
    langIndicator.textContent = model.get("language");
  });

  model.on("change:theme", () => {
    container.setAttribute("data-theme", model.get("theme"));
  });

  model.on("change:read_only", () => {
    textarea.readOnly = model.get("read_only");
  });

  // Set initial theme
  container.setAttribute("data-theme", model.get("theme"));

  // Hide output initially if empty
  if (!model.get("output") && !model.get("error")) {
    outputSection.style.display = "none";
  }
}

export default { render };
