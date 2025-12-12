# Marimo Notebooks

Interactive marimo notebooks demonstrating all Ontonaut features.

## 📚 Notebooks

### Getting Started
- **[01-getting-started.py](./01-getting-started.py)** - Basic CodeEditor usage
  - Python, JSON, Calculator, and Regex executors
  - Theme switching and configuration
  - Programmatic control

### ChatBot Guide
- **[02-chatbot-guide.py](./02-chatbot-guide.py)** - Complete ChatBot features
  - Echo handler for testing
  - OpenAI integration
  - Custom company wrappers
  - MCP server integration
  - Streaming and tab management

### Integrations
- **[03-openai-integration.py](./03-openai-integration.py)** - OpenAI streaming
  - Direct OpenAI API usage
  - Custom handler implementation
  - Environment variable setup

## 🚀 Running Notebooks

### Install Marimo

```bash
pip install marimo
```

### Run a Notebook

```bash
# Run interactively
marimo edit book/marimo/01-getting-started.py

# Run as app
marimo run book/marimo/01-getting-started.py
```

### Open All Notebooks

```bash
marimo edit book/marimo/*.py
```

## 📝 Creating Your Own

Create a new marimo notebook:

```bash
marimo new my_notebook.py
```

Add Ontonaut widgets:

```python
import marimo as mo
from ontonaut import CodeEditor, ChatBot, PythonExecutor, EchoHandler

# Create widgets
editor = CodeEditor(executor=PythonExecutor())
chatbot = ChatBot(handler=EchoHandler())

# Display them
editor
chatbot
```

## 🔗 Features in Notebooks

### Interactive Editing
- Edit code directly in the browser
- See results immediately
- Export to various formats

### Reactive Execution
- Cells auto-update when dependencies change
- Marimo tracks widget state changes
- Build reactive dashboards

### Static Rendering
All notebooks can be statically rendered for GitHub Pages:

```bash
# Export to HTML
marimo export html 01-getting-started.py > index.html

# Export all
for f in book/marimo/*.py; do
    marimo export html $f > $(basename $f .py).html
done
```

## 📖 Notebook Structure

Each notebook follows this structure:

```python
import marimo as mo

__generated_with = "0.18.3"
app = mo.App()

@app.cell
def _():
    # Imports
    import marimo as mo
    from ontonaut import ...
    return ...

@app.cell
def _(mo):
    # Documentation
    mo.md("# Title")
    return

@app.cell
def _():
    # Widget examples
    editor = CodeEditor(...)
    editor
    return

if __name__ == "__main__":
    app.run()
```

## 🎨 Best Practices

### 1. Use Markdown Cells
Document your notebooks with markdown:

```python
@app.cell
def _(mo):
    mo.md("""
    # Widget Demo

    This demonstrates the CodeEditor widget.
    """)
    return
```

### 2. Hide Code When Appropriate
Use `hide_code=True` for cleaner presentations:

```python
@app.cell(hide_code=True)
def _():
    # Setup code hidden from view
    setup_widgets()
    return
```

### 3. Name Your Widgets
Make them accessible across cells:

```python
@app.cell
def _():
    my_editor = CodeEditor(...)
    return my_editor,  # Note the comma!

@app.cell
def _(my_editor):
    # Use in another cell
    mo.md(f"Output: {my_editor.output}")
    return
```

### 4. Provide Examples
Include working examples in notebooks:

```python
@app.cell
def _(mo):
    mo.md("""
    ## Example

    Try running:
    ```python
    x = 10
    y = 20
    result = x + y
    ```
    """)
    return
```

## 🌐 Publishing to GitHub Pages

1. **Export all notebooks:**

```bash
cd book/marimo
for f in *.py; do
    marimo export html $f > $(basename $f .py).html
done
```

2. **Create index.html:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Ontonaut Notebooks</title>
</head>
<body>
    <h1>Ontonaut Interactive Notebooks</h1>
    <ul>
        <li><a href="01-getting-started.html">Getting Started</a></li>
        <li><a href="02-chatbot-guide.html">ChatBot Guide</a></li>
        <li><a href="03-openai-integration.html">OpenAI Integration</a></li>
    </ul>
</body>
</html>
```

3. **Deploy:**

```bash
# Copy to docs folder for GitHub Pages
mkdir -p ../../docs/notebooks
cp *.html ../../docs/notebooks/
```

4. **Enable GitHub Pages** in repository settings pointing to `/docs`

## 🔧 Troubleshooting

### Notebook Won't Load
- Check marimo version: `marimo --version`
- Update marimo: `pip install --upgrade marimo`
- Verify imports: `python -c "import ontonaut"`

### Widgets Not Displaying
- Ensure ontonaut is installed: `pip install -e .`
- Check for JavaScript errors in browser console
- Try restarting marimo server

### Changes Not Reflecting
- Rebuild package: `make build`
- Restart marimo server
- Clear browser cache

## 📚 Learn More

- [Marimo Documentation](https://docs.marimo.io)
- [Ontonaut Docs](../markdown/)
- [Architecture Guide](../../docs/)

## 🎯 Next Steps

1. Run the notebooks to see examples
2. Modify them to experiment
3. Create your own notebooks
4. Export and share your work!
