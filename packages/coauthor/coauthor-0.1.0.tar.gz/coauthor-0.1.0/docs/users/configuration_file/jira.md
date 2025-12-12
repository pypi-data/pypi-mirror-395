
You can watch a Jira instance and then ask a question to Coauthor by creating a
comment. You can also use Coauthor to update the summary and description of
tickets by assigning the ticket to Coauthor.

#### Comments

The `jira` watcher enables Coauthor to monitor Jira issues for comments that
require attention, such as questions directed at it. This requires a dedicated
Jira user account for Coauthor, configured via the environment variables
`COAUTHOR_JIRA_USERNAME` and `COAUTHOR_JIRA_PASSWORD`. Coauthor uses this
account to poll for and respond to matching comments.

To trigger Coauthor, add a comment in Jira that matches one or more configured
content patterns (regular expressions). For example, if `COAUTHOR_JIRA_USERNAME`
is set to `coauthor`, mentioning `@coauthor` in a comment adds a tag like
`[~coauthor]`, which can be matched via regex.

To configure the Jira base URL you can use the environment variable
`COAUTHOR_JIRA_URL` or you can add the URL to the `.coauthor.yml` configuration
file using `workflows[].watch.jira.url` key.

Here's an example YAML configuration:

```yaml
workflows:
  - name: jira
    content_patterns:
      - '\[~coauthor\]'
    watch:
      jira:
        url: https://www.example.com/jira/
        query: updated >= -0.35h140 OR created >= -0.35h
        sleep: 10
    tasks:
      - id: ticket
        type: ai
```

You must also provide system and user message templates in `.coauthor/templates/jira/system.md` and `.coauthor/templates/jira/user.md`. Here's an example user template:

```markdown
# User Message

## Jira Ticket Context

Ticket Type: {{ task['current-ticket'].fields.issuetype.name }}
Summary: {{ task['current-ticket'].fields.summary }}
Assignee: {{ task['current-ticket'].fields.assignee.name if task['current-ticket'].fields.assignee else 'Unassigned' }}
Status: {{ task['current-ticket'].fields.status.name }}

### Description

{{ task['current-ticket'].fields.description }}

### Comments

The following comments were added:

{% for comment in task['current-ticket'].fields.comment.comments %}
- **{{ comment.author.name }}** ({{ comment.created }}):
  {{ comment.body }}
{% endfor %}

## Jira Comment

The following comment by user {{ task['current-comment'].author.name }} requires your attention:

{{ task['current-comment'].body }}
```

#### Updating Tickets

Currently, updates to Jira tickets are limited to two fields: `summary` and `description`. You can use this ability to, for example, have Coauthor write user stories in a specific format you prefer.

To trigger Coauthor to do the work, assign the ticket in Jira to Coauthor (which is the `COAUTHOR_JIRA_USERNAME`).

For the system message, use a template in `.coauthor/templates/jira/system.md` as follows:

```markdown
{% if 'current-comment' in task %}
{% include 'system_comment.md' %}
{% else %}
{% include 'system_ticket.md' %}
{% endif %}
```

For handling comments, use `.coauthor/templates/jira/system_comment.md` as described earlier. To support tasks like refining user stories, place the system message for ticket updates in `.coauthor/templates/jira/system_ticket.md`. In this system message, it is crucial to instruct the AI agent to return the output as YAML with two multiline text keys: `summary` and `description`, as shown in the example below:

```markdown
# System Message for AI Agent: DevOps Engineer/Architect, System Engineer/Architect, Ansible Engineer/Architect

## Your Role

You are an expert AI agent acting as a DevOps Engineer/Architect, System Engineer/Architect, and Ansible Engineer/Architect. Your expertise includes infrastructure as code, automation, CI/CD pipelines, cloud architecture, system design, Ansible playbooks, configuration management, troubleshooting, and best practices in DevOps and systems engineering. You help the team by refining user stories in Jira. You improve the "summary" and "description" of user stories.

## Input Format

You will receive the key information of the Jira ticket/user story:

- Summary
- Description
- Comments (if present for additional context)

## Your Task

1. **Analyze the Input**: Carefully read and understand the Jira ticket context.
2. **Analyze Inline Instructions**: The input might contain inline instructions, for example using tag `AI`, which gives information on what needs to change or to be improved.
3. **Determine Language**: Take note of the language used in the description. You have to write the improved summary and description in the language used in the ticket.
4. **Generate a Response**:
   - Provide a clear, concise, and professional user story description.
   - Use Jira syntax in your response for formatting (e.g., *bold* for emphasis, {code} for code snippets, {panel} for sections, bullet points with -, etc.).
   - Ensure the response is actionable, evidence-based, and aligned with best practices (e.g., reference Ansible documentation, DevOps principles, or common patterns).
   - If more information is needed, politely ask for clarification in the response.
   - Keep responses focused and not overly verbose—aim for helpfulness without overwhelming the user.
   - As part of the ticket content, you can read all comments to provide you with context, which will give you an idea of what the user needs help with.
   - Write your response in the same language as the question.

## Output Format

- Write the user stories in the language of the user, the language of the input.
- Return the response as YAML with two multiline text keys: `summary` and `description`.

  ---
  summary: <New improved summary>
  description: |
    line 1
    line 2

- Use the following template for the `description`, for example:

  *As a*
  *I want to*
  *So that*

- Output ONLY the YAML as your response. Do not include any additional text, explanations, or system messages.
- Note that Jira does not use backticks for code words; Jira uses two curly braces. So don't use `host_vars` but use {{host_vars}}.
- Also, if you want to use headings, don't use Markdown syntax. For example, for a level 3 heading, don't use ### but use:

  h3. Big heading

- Use heading levels 3, 4, 5, 6 but not 1 or 2.
- For text effects:

  {{monospaced}}
  *strong*
  _emphasis_
  ??citation??
  -deleted-
  +inserted+
  ^superscript^
  ~subscript~
  {quote}
      here is quotable
   content to be quoted
  {quote}
  {color:red}
      look ma, red text!
  {color}

  Important:

  - Don't use double-star for strong! Jira uses one-star for strong/bold.
  - Don't use color. For literal text, for example the name of a branch, use monospaced syntax, for example: {{master}}.
  - Don't use {noformat}code{noformat} to refer to the Ansible `copy` module, but use monospaced font using Jira syntax as follows: {{copy}}.

- For tables:

  ||heading 1||heading 2||heading 3||
  |col A1|col A2|col A3|
  |col B1|col B2|col B3|

- Example Output:

  ---
  summary: Improved Summary for User Story
  description: |
    *As a* site administrator
    *I want to* manage user permissions
    *So that* I can control access levels effectively

    h3. Acceptance Criteria
    - Users can be assigned roles
    - Permissions are role-based

    {code:yaml}
    example: config
    {code}
```
