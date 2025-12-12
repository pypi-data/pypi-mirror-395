{%- set readme_path = task['path-modify-event'] | find_up('README.md') -%}
{{ readme_path | include_file_content }}