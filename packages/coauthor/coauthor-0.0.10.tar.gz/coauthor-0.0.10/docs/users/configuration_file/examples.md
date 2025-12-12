
### Hugo Website Workflow Example

Coauthor can help maintain the Hugo-based community website for the C2 Platform [c2platform.org](https://c2platform.org). The `.coauthor.yml` configuration supports tasks like updating translations for Markdown files in the `content/en/` directory. Setting the `translate` attribute to `true` triggers tasks such as `ai-translate` for content translation and `write-file` for outputting the result.

Below is an example configuration snippet:

```yaml
jinja:
  search_path: .coauthor/templates
  custom_delimiters:
    block_start_string: "{{{{%"
    block_end_string: "%}}}}"
    variable_start_string: "{{{{"
    variable_end_string: "}}}}"
workflows:
  - name: website
    path_patterns:
      - .*\.md$
    content_patterns:
      - ".*@ai-test:.*"
    watch:
      filesystem:
        paths:
          - content/en/
    scan:
      filesystem:
        paths:
          - content/en/
    tasks:
      - id: ai-update
        type: ai
      - id: write-file
        type: write_file
        content: >-
          {{{{ config | get_task_attribute('ai-update', 'response') }}}}
  - name: hugo
    path_patterns:
      - layouts\/.*\.html$
    content_patterns:
      - ".*@ai-test:.*"
    watch:
      filesystem:
        paths:
          - layouts
    tasks:
      - id: ai-update
        type: ai
      - id: write-file
        type: write_file
        content: >-
          {{{{ config | get_task_attribute('ai-update', 'response') }}}}
  - name: translation
    path_patterns:
      - .*\.md$
    content_patterns:
      - ".*translate: true.*"
    watch:
      filesystem:
        paths:
          - content/en/
    scan:
      filesystem:
        paths:
          - content/en/
    tasks:
      - id: ai-translate
        type: ai
      - id: write-file
        type: write_file
        content: >-
          {{{{ config | get_task_attribute('ai-translate', 'response') }}}}
        path: >-
          {{{{ config['current-task']['path-modify-event']
          | replace('content/en', 'content/nl') }}}}
      - id: translate-false
        type: regex_replace_in_file
        patterns:
          - regex: "translate: true"
            replace: "translate: false"
  - name: regex-file-updates
    path_patterns:
      - .*\.md$
    watch:
      filesystem:
        paths:
          - content/en/
    tasks:
      - id: regex-file-updates
        type: regex_replace_in_file
        patterns:
          - regex: ({{< \b[\s\S]*?>}})
            internal_regex: \s+
            internal_replace: ' '
          - regex: "(?<!` ) -> "
            replace: " → "
          - regex: "(?<!` ) <- "
            replace: " ← "
          - regex: \[([^\]]+)\]\(http://localhost:1313([^\)]+?)/\)
            replace: '{{< rellink path="\2" >}}'
```

Following this configuration, Coauthor effectively manages tasks such as translations, file writing, and regex-based transformations, thereby streamlining website management and content automation.

