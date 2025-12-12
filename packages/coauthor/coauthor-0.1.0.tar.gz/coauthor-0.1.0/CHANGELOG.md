# CHANGELOG
<!-- start changelog -->

## 0.1.0 ( 2025-12-05 )

- Fix "ValueError: Project not found: coauthor"
- Added `search_files` tool to search for strings or regex in project files,
  with optional context lines.
- Disabled langchain/langgraph code.

## 0.0.10 ( 2025-12-04 )

- Fix `json_object` for responses for Jira comments/tickets.
- Workflows can/need to be optional in multi-project setup.
- Added `save_config_dump` in `config.py`.
- Added support for project based on profiles.
- Create config dump file `.coauthor_dump.yml` in debug log mode (`--debug`).
- Added `jira` profile.
- Fixed bug in `is_binary_file`.
- Added context management using `COAUTHOR.md` with tools `get_context` and
  `update_context` for learning from interactions.
- Added tools `delete_files` and `move_files`.
- Removed `returns_response` feature.
- Added support for projects based on profiles.
- Detect, log and skip duplicate tools calls.
- Improved `save_response` with `response.model_dump()` .
- Use `os.getcwd()` with `os.path.expanduser` to support Linux home notation
  `~/`.
- Improved logging of requests and response details for troubleshooting.
- Add tools `list_modified_files`, `get_diffs`.
- Made `workflows` optional for projects.
- Always send user message with information on projects.
- Added tools `list_tracked_directories`, `create_directories`.
- Added tools support.
- Added `role-readme` workflow to profile `ansible-collection`.
- Ability to submit all files in a directory and subdirectories as user
  messages.
- Jinja2 filters `find_up` and `find_down`.
- Ability to export a profile for example a follows:

  ```bash
  coauthor --export --profile ansible-collection
  ```

- First profile: `ansible-collection`.
- Support for profiles.
- Added `get_url` Jinja filter.
- Added ability to send files as user messages as context based on
  frontmatter in Markdown files.
- Added ability to configure additional user messages on a task.
- Added `--notify` switch, currently only used by Jira watcher to send desktop
  notifications.
- Added Jira watcher that uses [Python Jira](https://jira.readthedocs.io/) to
  watch Jira instances and update tickets using AI task.
- Added YouTube Data API Pytest test.
- Added new task `youtube` to download YouTube video transcripts.
- Added new task `replace_redirecting_links`.
- Add `extname` Jinja filters
- Added `markdown` module for `include-files`.
- Added `basename`, `dirname` Jinja filters.
- PlantUML task `plantuml` to export PlantUML files to png, svg files.
- Print Coauthor version using `--version`.
- Added ability to raise an error in a Jinja template for example as follows:

  ```jinja
  {{ raise("uh oh...") }}
  ```

- Added ability to use `json_object` as `response_format` to improve Jira
  integration.
- Switch Coauthor AI model to `x-ai/grok-4`.
- Logging with caller module and caller method/function.
- Task `include-files` support for indentation and use of named capturing
  groups in template.
- Default config for `file-watcher`.
- System and user message templates can now created in three locations.
- Task `process_file_with_openai_agent` renamed to `ai`.
- Variable `task` and `workflow` added to Jinja context.
- Fixed endless AI submit loop when a Jira workflow is used.
- `prompt_template_paths` using workflow name not id.
- Binary files causing error. Binary files are now ignored.
- Unexpected keyword argument 'proxies' fixed with upgrade OpenAI Python API
  library `1.13.3` → `1.57.4` .

## O.0.4 ( 2024-11-21 )

- Improved
  - Refactoring workflows & tasks

## 0.0.3

- Added
  - Initial Coauthor release
<!-- end changelog -->