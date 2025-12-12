# Context Ansible Role File `{{ task["user-message-context-file"] }}` file

The content of the `{{ task["user-message-context-file"] | basename }}` is:

{{ task["user-message-context-file"] | include_file_content }}
