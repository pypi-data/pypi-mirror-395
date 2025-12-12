- Use the example below as a template for the `description` for a `Story` ticket type. Note
  that "Ontwerp/implementatie" section is optional. If the input text contains
  code examples and technical comments, instructions for design/implementation,
  don't remove these but put them in this separate section.
- Limit the text to max 230 words.
- Use the following template for the `description` for a `Story` ticket type.
  For example for Dutch:

  ```jira
  *Als*
  *Wil*
  *Zodat*

  h4. Achtergrond

  Add description of background

  h4. Acceptatie-criteria

  - criteria 1
  - criteria 2

  h4. Taken

  - Description of task
  - Description of task

  h4. Ontwerp/implementatie

  - Hugo shortcodes voor externe-links zijn `layouts/shortcodes/extlink_ignore.html` en `layouts/shortcodes/extlink.html`

  - Voorbeeld van gebruik:
    {code}
    {% raw %}
    {{< extlink "https://www.redhat.com/en/technologies/management/ansible" "Red Hat Ansible Automation Platform" >}}
    {% endraw %}
    {code}
  ```
