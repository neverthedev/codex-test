# OpenAI CLI Tool

A tiny Python command-line tool that sends a prompt to an OpenAI model using the official OpenAI Python SDK and prints the response.

## Setup

Install the Python dependency:

```bash
python -m pip install -r requirements.txt
```

Set your OpenAI API key in the environment:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

Optionally choose a default model:

```bash
export OPENAI_MODEL="gpt-5.5"
```

## Usage

```bash
python openai_cli.py "Write a haiku about Python"
```

You can also pass the prompt as separate words:

```bash
python openai_cli.py Write a haiku about Python
```

Use another model for a single call:

```bash
python openai_cli.py --model gpt-5.4-mini "Explain recursion briefly"
```
