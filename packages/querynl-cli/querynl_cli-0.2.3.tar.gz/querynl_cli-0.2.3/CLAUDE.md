# QueryNL Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-10-12

## Active Technologies
- Python 3.11+ (001-ai-powered-database)
- Python 3.11+ (matches existing QueryNL backend, per constitution from CLAUDE.md) + Click 8.1+ (CLI framework), Rich 13.0+ (terminal formatting), prompt_toolkit 3.0+ (REPL input), Keyring 25.0+ (credential storage), keyrings.cryptfile 1.3+ (headless fallback) (002-command-line-interface)
- Files for config (~/.querynl/config.yaml), OS keychain for credentials, SQLite for local query history (002-command-line-interface)
- Python 3.10+ (existing codebase uses 3.10-3.12) (003-export-and-save)
- File system (local paths, no database storage for exports) (003-export-and-save)
- Python 3.11+ (matches existing QueryNL codebase) (004-natural-language-based)
- Python 3.10+ (existing codebase uses 3.10-3.12, per setup.py) + LangChain (LLM orchestration), OpenAI/Anthropic (LLM providers), SQLAlchemy (schema introspection), Rich (terminal UI), Click (CLI framework) (005-add-test-data)
- N/A (operates on existing user databases - MySQL, PostgreSQL, SQLite) (005-add-test-data)
- Python 3.10+ (existing codebase uses 3.10-3.12, per setup.py) + LangChain (LLM orchestration), OpenAI/Anthropic (LLM providers), SQLAlchemy (schema introspection), Faker (data generation), toposort (dependency ordering), Rich (terminal UI), Click (CLI framework) (005-add-test-data)

## Project Structure
```
src/
tests/
```

## Commands
cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style
Python 3.11+: Follow standard conventions

## Recent Changes
- 005-add-test-data: Added Python 3.10+ (existing codebase uses 3.10-3.12, per setup.py) + LangChain (LLM orchestration), OpenAI/Anthropic (LLM providers), SQLAlchemy (schema introspection), Faker (data generation), toposort (dependency ordering), Rich (terminal UI), Click (CLI framework)
- 005-add-test-data: Added Python 3.10+ (existing codebase uses 3.10-3.12, per setup.py) + LangChain (LLM orchestration), OpenAI/Anthropic (LLM providers), SQLAlchemy (schema introspection), Rich (terminal UI), Click (CLI framework)
- 004-natural-language-based: Added Python 3.11+ (matches existing QueryNL codebase)

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
