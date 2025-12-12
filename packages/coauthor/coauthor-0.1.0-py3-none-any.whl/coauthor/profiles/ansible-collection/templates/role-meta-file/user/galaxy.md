# Context Ansible Collection `galaxy.yml` file

The content of the `galaxy.yml` is:

{%- set galaxy_path = task['path-modify-event'] | find_up('galaxy.yml') -%}
{{ galaxy_path | include_file_content }}
