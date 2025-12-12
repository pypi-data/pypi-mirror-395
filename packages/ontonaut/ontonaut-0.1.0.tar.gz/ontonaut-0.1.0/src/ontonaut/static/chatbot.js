/**
 * Ontonaut ChatBot Widget
 * Simple streaming input/output with tabs and code formatting
 */

function render({ model, el }) {
  // Create main container (like CodeEditor)
  const container = document.createElement("div");
  container.className = "ontonaut-stream-container";

  // Create toolbar
  const toolbar = document.createElement("div");
  toolbar.className = "ontonaut-stream-toolbar";

  const langIndicator = document.createElement("span");
  langIndicator.className = "ontonaut-stream-language";
  langIndicator.textContent = "AI Assistant";

  const runButton = document.createElement("button");
  runButton.className = "ontonaut-stream-run-button";
  runButton.innerHTML = `
    <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
      <path d="M4 2v12l10-6z"/>
    </svg>
    <span>Run</span>
  `;
  runButton.disabled = model.get("is_streaming");

  const clearButton = document.createElement("button");
  clearButton.className = "ontonaut-stream-clear-button";
  clearButton.textContent = "Clear";

  toolbar.appendChild(langIndicator);
  toolbar.appendChild(runButton);
  toolbar.appendChild(clearButton);

  // Create input section
  const inputSection = document.createElement("div");
  inputSection.className = "ontonaut-stream-input-section";

  const inputBox = document.createElement("textarea");
  inputBox.className = "ontonaut-stream-input";
  inputBox.placeholder = model.get("placeholder");
  inputBox.value = model.get("input_text");
  inputBox.rows = 3;

  inputSection.appendChild(inputBox);

  // Create tabs section
  const tabsSection = document.createElement("div");
  tabsSection.className = "ontonaut-stream-tabs";

  // Create output section
  const outputSection = document.createElement("div");
  outputSection.className = "ontonaut-stream-output-section";

  const outputLabel = document.createElement("div");
  outputLabel.className = "ontonaut-stream-output-label";
  outputLabel.textContent = "Output";

  const outputContent = document.createElement("div");
  outputContent.className = "ontonaut-stream-output";
  outputContent.innerHTML = formatOutput(model.get("output") || "");

  const errorContent = document.createElement("pre");
  errorContent.className = "ontonaut-stream-error";
  errorContent.textContent = model.get("error") || "";

  outputSection.appendChild(outputLabel);
  outputSection.appendChild(outputContent);
  outputSection.appendChild(errorContent);

  // Assemble widget
  container.appendChild(toolbar);
  container.appendChild(inputSection);
  container.appendChild(tabsSection);
  container.appendChild(outputSection);
  el.appendChild(container);

  // Format output with code blocks
  function formatOutput(text) {
    if (!text) return "";

    // Convert markdown-style code blocks to HTML
    let html = text;

    // Match code blocks: ```language\ncode\n```
    html = html.replace(/```(\w+)?\n([\s\S]*?)```/g, (match, lang, code) => {
      const language = lang || 'text';
      return `<pre class="code-block" data-lang="${language}"><code>${escapeHtml(code.trim())}</code></pre>`;
    });

    // Match inline code: `code`
    html = html.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');

    // Convert newlines to <br> for remaining text
    html = html.replace(/\n/g, '<br>');

    return html;
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // Render tabs
  function renderTabs() {
    const tabs = model.get("tabs");
    const activeTab = model.get("active_tab");

    tabsSection.innerHTML = "";

    if (tabs.length === 0) {
      tabsSection.style.display = "none";
      return;
    }

    tabsSection.style.display = "flex";

    // Render saved tabs
    tabs.forEach((tab, index) => {
      const tabButton = document.createElement("button");
      tabButton.className = "ontonaut-tab";
      if (activeTab === index) {
        tabButton.classList.add("active");
      }

      const tabTitle = document.createElement("span");
      tabTitle.className = "ontonaut-tab-title";
      tabTitle.textContent = tab.title;

      const closeBtn = document.createElement("span");
      closeBtn.className = "ontonaut-tab-close";
      closeBtn.textContent = "×";
      closeBtn.onclick = (e) => {
        e.stopPropagation();
        closeTab(index);
      };

      tabButton.appendChild(tabTitle);
      tabButton.appendChild(closeBtn);

      tabButton.onclick = () => switchTab(index);
      tabsSection.appendChild(tabButton);
    });

    // Add "Current" tab
    const currentTab = document.createElement("button");
    currentTab.className = "ontonaut-tab ontonaut-tab-current";
    if (activeTab === -1 || activeTab >= tabs.length) {
      currentTab.classList.add("active");
    }
    currentTab.textContent = "Current";
    currentTab.onclick = () => switchTab(-1);
    tabsSection.appendChild(currentTab);
  }

  function switchTab(index) {
    // Just update model - the listener will handle UI updates
    model.set("active_tab", index);
    model.save_changes();
  }

  function updateTabContent(index) {
    // Update the displayed content based on active tab
    const tabs = model.get("tabs");

    if (index === -1 || index >= tabs.length) {
      // Show current output
      outputContent.innerHTML = formatOutput(model.get("output"));
      errorContent.textContent = model.get("error") || "";
    } else {
      // Show saved tab
      const tab = tabs[index];
      outputContent.innerHTML = formatOutput(tab.content);
      errorContent.textContent = "";
    }
  }

  function closeTab(index) {
    const tabs = model.get("tabs");
    const newTabs = tabs.filter((_, i) => i !== index);
    model.set("tabs", newTabs);
    model.save_changes();

    // Adjust active tab if needed
    if (model.get("active_tab") === index) {
      model.set("active_tab", -1);
      model.save_changes();
    }
  }

  // Execute function
  function executeInput() {
    const input = inputBox.value.trim();
    if (!input || model.get("is_streaming")) return;

    model.send({ type: "execute", input: input });
  }

  // Event listeners
  runButton.onclick = executeInput;

  clearButton.onclick = () => {
    inputBox.value = "";
    outputContent.innerHTML = "";
    errorContent.textContent = "";
    model.set("input_text", "");
    model.set("output", "");
    model.set("error", "");
    model.save_changes();
  };

  // Sync input changes
  inputBox.addEventListener("input", () => {
    model.set("input_text", inputBox.value);
    model.save_changes();
  });

  // Keyboard shortcuts
  inputBox.addEventListener("keydown", (e) => {
    // Cmd/Ctrl + Enter to run
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
      e.preventDefault();
      executeInput();
    }

    // Tab for indentation
    if (e.key === "Tab") {
      e.preventDefault();
      const start = inputBox.selectionStart;
      const end = inputBox.selectionEnd;
      inputBox.value = inputBox.value.substring(0, start) + "    " + inputBox.value.substring(end);
      inputBox.selectionStart = inputBox.selectionEnd = start + 4;
      model.set("input_text", inputBox.value);
      model.save_changes();
    }
  });

  // Listen for model changes
  model.on("change:input_text", () => {
    if (inputBox.value !== model.get("input_text")) {
      inputBox.value = model.get("input_text");
    }
  });

  model.on("change:output", () => {
    // Only update if viewing current tab
    if (model.get("active_tab") === -1 || model.get("active_tab") >= model.get("tabs").length) {
      outputContent.innerHTML = formatOutput(model.get("output"));
      if (model.get("output")) {
        outputSection.style.display = "block";
      }
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

  model.on("change:tabs", () => {
    renderTabs();
  });

  model.on("change:active_tab", () => {
    renderTabs();
    updateTabContent(model.get("active_tab"));
  });

  model.on("change:is_streaming", () => {
    const streaming = model.get("is_streaming");
    runButton.disabled = streaming;
    inputBox.disabled = streaming;

    if (streaming) {
      runButton.classList.add("disabled");
      inputBox.classList.add("disabled");
    } else {
      runButton.classList.remove("disabled");
      inputBox.classList.remove("disabled");
    }
  });

  model.on("change:theme", () => {
    container.setAttribute("data-theme", model.get("theme"));
  });

  model.on("change:placeholder", () => {
    inputBox.placeholder = model.get("placeholder");
  });

  // Set initial theme
  container.setAttribute("data-theme", model.get("theme"));

  // Hide output initially if empty
  if (!model.get("output") && !model.get("error")) {
    outputSection.style.display = "none";
  }

  // Initial render
  renderTabs();
}

export default { render };
