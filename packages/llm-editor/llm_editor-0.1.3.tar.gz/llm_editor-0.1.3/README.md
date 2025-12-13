# LLM Editor

A CLI tool to edit files using LLMs.

## Installation

```bash
pip install .
```

## Configuration

You can configure the tool using a YAML file.

### YAML Configuration

Run the following command to generate a default configuration file at `~/.llm-editor/config.yaml`:

```bash
edit --init-config
```

Then edit the file to add your API key:

```yaml
llm:
  provider: openai
  api_key: "your-api-key"
  model: "gpt-4o"

app:
  backup_enabled: true
  backup_suffix: ".backup"
```

## Usage

### 1. Using Prompt Tags (Scripting Mode)

Add your instructions directly to the file using `<tag>` markers.

**Example `input.txt`:**

```text
<tag> start_prompt
Convert the following Python code to JavaScript.
<tag> end_prompt

def greet(name):
    print(f"Hello, {name}!")

greet("World")
```

Run the tool:

```bash
edit input.txt
```

### 2. Interactive Mode

If the input file does not contain prompt tags, the tool will open your default text editor (configured via `$EDITOR`). You can type your instructions there, save, and close the editor to proceed.

### Options

- `--outfile <path>`: Write output to a specific file (input file is preserved).
- `--inplace`: Overwrite the input file directly (skips backup).
- `--init-config`: Initialize the configuration file.
