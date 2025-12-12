# Current Code of the Module

{% set path_code_linux = task["path-modify-event"] | replace(".yml",".py") %}
{% set path_code_win = task["path-modify-event"] | replace(".yml",".ps1") %}

{% if path_code_linux | file_exists %}

The current content of the YAML documentation file { path_code_linux } is:

{{ path_code_linux | include_file_content }}

{% else %}

The current content of the YAML documentation file { path_code_win } is:

{{ path_code_win | include_file_content }}

{% endif %}
