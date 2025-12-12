# Coauthor Context

## Language Guidelines

- The primary language for the coauthor project is English. All code,
  documentation, and project files must be in English.
- Interactions with users may be in Dutch or other languages, but when
  generating or modifying code, content, or documentation via tools, always use
  English.
- Jira comments and ticket descriptions "should" be in the language of the
  interaction.
- Do not use Jira syntax (e.g., {code}, {{monospaced}}) in project files. Use
  Markdown syntax instead. Jira syntax is reserved for Jira comments and
  tickets.
- This file (`COAUTHOR.md`) must be written in English using Markdown syntax.

## Coding Conventions

- Use consistent snake_case for variable names.
- In except blocks: avoid single-letter names like `e`; use descriptive names
  like `exception_error`.
- When opening files with `open()`, always specify the encoding explicitly
  (e.g., `encoding='utf-8'`) to avoid linter issues such as pylint W1514
  (unspecified-encoding).

### Example (good)

```python
except Exception as exception_error:
    results[path] = f"Error: {str(exception_error)}"
```

## CHANGELOG.md Conventions

- Most recent changes are listed at the top of the file.
- Add new entries under the current version section.

## Tool Usage Guidelines

- Always use the `write_files` tool to save any proposed file changes. Do not
  assume changes are saved without calling this tool.
