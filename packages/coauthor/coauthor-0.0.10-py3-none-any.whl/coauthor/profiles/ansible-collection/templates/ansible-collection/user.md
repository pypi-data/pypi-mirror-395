Update the contents of file {{ task['path-modify-event'] }} with embedded inline instructions.

The current content of the file is:

```markdown
{{ task['path-modify-event'] | include_file_content }}
```
