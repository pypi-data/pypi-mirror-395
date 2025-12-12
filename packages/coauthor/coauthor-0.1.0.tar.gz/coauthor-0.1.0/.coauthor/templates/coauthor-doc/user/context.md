{%- if 'url' in task['frontmatter-item'] -%}
{%- include 'context/url.md' -%}
{%- endif -%}
{%- if 'file' in task['frontmatter-item'] -%}
{%- include 'context/file.md' -%}
{%- endif -%}
{%- if 'diff' in task['frontmatter-item'] -%}
{%- include 'context/diff.md' -%}
{%- endif -%}
