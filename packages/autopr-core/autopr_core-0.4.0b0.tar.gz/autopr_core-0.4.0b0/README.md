# AutoPR — AI-powered Pull Request Generator & Reviewer

[![PyPI version](https://badge.fury.io/py/autopr.svg)](https://pypi.org/project/autopr/)
[![Try the demo](https://img.shields.io/badge/demo-autopr_demo-blue.svg)](https://github.com/your-user/autopr-demo)

AutoPR automates the repetitive parts of pull requests for teams: it writes concise PR titles & descriptions, validates CI/tests, runs deterministic static and lint checks, and provides an AI-assisted review summary.

## Quickstart

### Install from PyPI (Recommended)

```bash
pip install autopr
```

### Install from Source

```bash
git clone https://github.com/surenkotian/AutoPR.git
cd AutoPR
pip install -e .
```

2. **Run the API server:**
   ```bash
   uvicorn autopr.main:app --reload --port 8000
   ```

3. **Try the CLI:**
   ```bash
   pr-ai gen --diff "+ added line" --commits "fix: add helper" --issue "#123"
   ```

## API Documentation

Once the server is running, visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API docs.

## Command Cheat Sheet

| Command | Description |
|---------|-------------|
| `pr-ai gen` | Generate PR title and description |
| `pr-ai review` | Perform AI-assisted code review |
| `pr-ai analyze` | Run static analysis on code diffs |
| `pr-ai ci-parse` | Parse CI/test logs |
| `pr-ai coverage-compare` | Compare coverage reports |
| `pr-ai validate-issue` | Check if changes align with issue |

## Features

- **FastAPI Backend** with `/generate` and `/review` endpoints
- **CLI Tool** for all operations
- **Static Analysis** for Python code
- **CI/Test Validation** tools
- **Multiple LLM Providers** (OpenAI, Anthropic, Stub)
- **GitHub Actions Integration**

## Using Real LLM Providers

Set `AUTOPR_PROVIDER` to `openai` or `anthropic` and provide API keys:

```bash
export OPENAI_API_KEY="your-key"
export AUTOPR_PROVIDER="openai"
```

See `.env.example` for all configuration options.

## Demo

Try AutoPR in action with our ready-to-deploy demo repository. See `publish-demo/README.md` for setup instructions.

## License

MIT