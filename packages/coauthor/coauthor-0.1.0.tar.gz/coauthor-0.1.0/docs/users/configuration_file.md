# Configuration

The `.coauthor.yml` configuration file is essential for customizing the behavior of your Coauthor AI agent. It defines various tasks grouped into workflows, facilitating efficient process automation.

## Modules

### File Watcher

By default, the File Watcher will ignore certain folders such as `__pycache__`, `.obsidian`, and `.git`. You can customize this behavior in your `.coauthor` configuration file.

```yaml
---
file-watcher:
  ignore-folders: [__pycache__, .obsidian, .git]
```

## Workflows

The `workflows` section consists of a list of workflows. Each workflow is uniquely identified by its `name` attribute in the configuration file. Workflows are collections of tasks executed in sequence when specific conditions, like changes in files or directories, are met.

## Tasks

Tasks within the `.coauthor.yml` are defined using their `id` and `type` attributes. They perform distinct functions, from AI-based file modifications to regex-based updates. Below are some available task types:

### AI Tasks

The `ai` task type employs AI to update a file based on specified configurations. To utilize this task, configure the `OPENAI_API_URL` and `OPENAI_API_KEY` environment variables. These variables ensure proper AI request authentication and routing.

- `id`: A unique identifier for the task.
- `type`: Must be set to `ai`.

Coauthor allows the flexibility to customize system and user prompts using the [Jinja](https://jinja.palletsprojects.com/en/stable/) templating engine. Prompts are named `system.md` (required) and `user.md` (optional). Without a user prompt, the entire file is submitted as the user prompt. Prompts can be defined at both the workflow and task levels. Coauthor searches for prompts in the following order:

1. `{workflow['name']}/{task['id']}/{filename}`
2. `{workflow['name']}/{filename}`
3. `{filename}`

Prompt templates can be saved in the `.coauthor/templates` directory. You can modify the default Jinja settings by adding a `jinja` section in `.coauthor.yml`. For example:

```yaml
jinja:
  search_path: .coauthor/templates
  custom_delimiters:
    block_start_string: "{{{{%"
    block_end_string: "%}}}}"
    variable_start_string: "{{{{"
    variable_end_string: "}}}}"
```

### Regex Replace

This task type updates a file using regex pattern matching and substitution.

- `id`: A unique identifier for the task.
- `type`: Set to `regex_replace_in_file`.

### Write a File

This task writes content to a file, such as saving an AI task's response.

- `id`: A unique identifier for the task.
- `type`: Specify `write_file` as the task type.
- `content`: The content to be written to the file.
- `path`: An optional path for the file to create or update. Without a specified `path`, the path that triggered the workflow is used.

Both `path` and `content` support Jinja templating. For instance, the `translation` workflow shown below in the Hugo website example writes the AI task's response to a different file using this feature.

### PlantUML

This task converts PlantUML files to image formats like PNG and SVG using the PlantUML jar file.

### Include a File

The `include-file` task type enables you to dynamically include the content of
external files into your documents. This is achieved by specifying a regex
pattern to locate the placeholder in the target document, with the file path for
inclusion captured by either the first capturing group or a named group `path`.

A customizable template allows you to define how the included content is
represented in the document, ensuring consistency and flexibility. Consider the
example configurations below that illustrate usage.

#### Basic Example

The following configuration illustrates using a regular expression where the
file path to be included is captured by the first group.

```yaml
workflows:
  - name: include-files
    path_patterns:
      - .*\.md$
    watch:
      filesystem:
        paths:
          - content/en/
    scan:
      filesystem:
        paths:
          - content/en/
    tasks:
      - id: include-code-examples
        type: include-file
        dir: ../cka
        regex: <!--\s*start-code-sample\s+([^ \t\n]+)\s*-->\s*(.*?)<!--\s*end-code-sample\s*-->
        template: |
          <!-- start-code-sample {{{{ task['include_file_path'] }}}} -->
          ```{{{{ task['include_file_path'] | extname }}}}
          # {{{{ task['include_file_path'] }}}}
          {{{{ task['include_file_content'] }}}}
          ```
          <!-- end-code-sample -->
```

In practice, any markdown file with a placeholder like this:

```markdown
<!-- start-code-sample ch02/rbac/build-observer-pod.yaml -->
<!-- end-code-sample -->
```

Will be replaced with:

````markdown
<!-- start-code-sample ch02/rbac/build-observer-pod.yaml -->
```yaml
# ch02/rbac/build-observer-pod.yaml
# (Actual content of the YAML file is inserted here)
```
<!-- end-code-sample -->
````

#### Example Using Named Group `path`

Here is an example where the file path for inclusion is specified using a named
capturing group.

```yaml
workflows:
- name: include-files
    path_patterns:
      - .*\.md$
    watch:
      filesystem:
        paths:
          - content/en/
    scan:
      filesystem:
        paths:
          - content/en/
    tasks:
      - id: include-code-examples
        type: include-file
        dir: ../cka
        regex: '(```(yaml|sh)\{[^\}]*data-src=\"(?P<path>[^\s\}]+)\"\})(.*?)```'
        template: |
          {{{{ task['match'][1] }}}}
          # {{{{ task['include_file_path'] }}}}
          {{{{ task['include_file_content'] }}}}
```

Now, by including the following in a markdown file:

````markdown
```yaml{data-src="ch02/rbac/build-bot-serviceaccount.yaml"}
```
````

This will be expanded to:

````markdown
```yaml{data-src="ch02/rbac/build-bot-serviceaccount.yaml"}
# ch02/rbac/build-bot-serviceaccount.yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: build-bot
```
````

#### Example Using Named Groups and the `indent` Group

The example below illustrates how named capturing groups are utilized for
greater flexibility and control in `include-file` tasks. This approach leverages
groups like `indent`, which adds the ability to maintain consistent formatting
by preserving the original indentation level of included content, alongside
`first_line` for capturing the initiating line/configuration.

The enhancement allows you to apply an indentation captured by `indent` to the
included file content, ensuring consistent formatting across documents. In this
example, the `indent` group captures any leading spaces/tabs before the code
block's starting line, using them when inserting the content, preserving
visually structured and aligned documents.

```yaml
workflows:
- name: include-files
    path_patterns:
      - .*\.md$
    watch:
      filesystem:
        paths:
          - content/en/
    scan:
      filesystem:
        paths:
          - content/en/
    tasks:
      - id: include-code-examples
        type: include-file
        dir: ../cka
        regex: '(?P<indent>[^\S\r\n]*)(?P<first_line>```(yaml|sh)\{[^\}]*data-src=\"(?P<path>[^\s\}]+)\"\})\n(?P<code_content>.*?)\n(?P=indent)```'
        template: |
          {{{{ task['match_groups']['first_line'] }}}}
          # {{{{ task['include_file_path'] }}}}
          {{{{ task['include_file_content'] }}}}
          ```
```

Now, by including the following in a markdown file:

````markdown
   ```yaml{data-src="ch02/rbac/build-bot-serviceaccount.yaml"}
   ```
````

This will be expanded to:

````markdown
   ```yaml{data-src="ch02/rbac/build-bot-serviceaccount.yaml"}
   # ch02/rbac/build-bot-serviceaccount.yaml
   ---
   apiVersion: v1
   kind: ServiceAccount
   metadata:
     name: build-bot
  ```
````

### Replace Redirecting Links

The `replace_redirecting_links` task type is used to identify and update links that redirect to different URLs, preventing unnecessary redirection. This is useful in ensuring that links within your content point directly to the desired destination without intermediate steps.

For instance, you might have content with various `https://oreil.ly` links that redirect. Using this task type, you can provide a regular expression to capture these URLs. The task will then verify the links and replace them with their direct targets.

Example of its usage:

```yaml
workflows:
- name: oreilly-links
    path_patterns:
      - .*\.md$
    watch:
      filesystem:
        paths:
          - content/en/
    scan:
      filesystem:
        paths:
          - content/en/
    tasks:
      - id: replace-redirect-links
        type: replace_redirecting_links
        regex: '"(https://oreil\.ly/[^\s"]+)"'
```

### YouTube

The `youtube` task allows you to download a transcript and data of a YouTube
video. Which you can then process using the AI task.

```yaml
workflows:
  - name: youtube
    path_patterns:
      - .*\.md$
    content_patterns:
      - - .*@whatever:.*
        - .*youtube_id:\s*(?P<video_id>\S+).*
    watch:
      filesystem:
        paths:
          - content/en/
    tasks:
      - id: youtube
        type: youtube
      - id: ai-update
        type: ai
      - id: write-file
        type: write_file
        content: >-
          {{{{ config | get_task_attribute('ai-update', 'response') }}}}
```

### Jira

```{include} configuration_file/jira.md
:parser: myst_parser.sphinx_
:start-line: 1
```

## Examples

```{include} configuration_file/examples.md
:parser: myst_parser.sphinx_
:start-line: 1
```

<!--
Tips and Suggestions:
- Consider adding more details to under-documented tasks like PlantUML (e.g., required attributes, example YAML).
- Ensure consistent formatting across sections; for example, use bullet points for task attributes in all task descriptions where applicable.
- In the YouTube section, fix the minor grammatical error: "Which you can then process" should be "which you can then process".
- The Jira section has been improved for clarity, fixed typos (e.g., "reqular" to "regular"), and structured similarly to other tasks.
- Overall, the document could benefit from a table of contents for better navigation.
-->
