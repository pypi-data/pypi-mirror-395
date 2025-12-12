# User Message

## Jira Ticket Context

Ticket Type: {{ task['current-ticket'].fields.issuetype.name }}
Summary: {{ task['current-ticket'].fields.summary }}
Assignee: {{ task['current-ticket'].fields.assignee.name if task['current-ticket'].fields.assignee else 'Unassigned' }}
Status: {{ task['current-ticket'].fields.status.name }}
{% if task['current-ticket'].fields.labels %}
Labels: {{ task['current-ticket'].fields.labels | join(', ') }}
{% endif %}
{% if task['current-ticket'].fields.components %}
Components:
{% for component in task['current-ticket'].fields.components %}
- Name: {{ component.name }}
  Description: {{ component.description if component.description else 'No description available' }}
{% endfor %}
{% else %}
No components.
{% endif %}

{% if 'related-tickets' in config and 'parent' in task['related-tickets'] and task['related-tickets']['parent'] %}
### Parent Ticket

- ID: {{ task['related-tickets']['parent'].key }}
  Summary: {{ task['related-tickets']['parent'].fields.summary }}
  {% if task['related-tickets']['parent'].fields.description %}
  Description: {{ task['related-tickets']['parent'].fields.description }}
  {% endif %}
{% endif %}

{% if 'related-tickets' in config and 'epic' in task['related-tickets'] and task['related-tickets']['epic'] %}
### Epic

- ID: {{ task['related-tickets']['epic'].key }}
  Summary: {{ task['related-tickets']['epic'].fields.summary }}
  {% if task['related-tickets']['epic'].fields.description %}
  Description: {{ task['related-tickets']['epic'].fields.description }}
  {% endif %}
{% endif %}

### Description

{{ task['current-ticket'].fields.description }}

### Linked Issues

{% if 'related-tickets' in config and 'grouped_linked' in task['related-tickets'] and task['related-tickets']['grouped_linked'] %}
{% for link_type, tickets in task['related-tickets']['grouped_linked'].items() %}
#### {{ link_type | capitalize }}

{% for ticket_info in tickets %}
- ID: {{ ticket_info.ticket.key }}
  Summary: {{ ticket_info.ticket.fields.summary }}
  {% if ticket_info.ticket.fields.description %}
  Description: {{ ticket_info.ticket.fields.description }}
  {% endif %}
{% endfor %}
{% endfor %}
{% else %}
No linked issues.
{% endif %}

{% if 'current-comment' in task %}

### Comments

The following comments were added:

{% for comment in task['current-ticket'].fields.comment.comments %}
- **{{ comment.author.name }}** ({{ comment.created }}):
  {{ comment.body }}
{% endfor %}

## Jira Comment

The following comment by user {{ task['current-comment'].author.name }} requires
your attention:

{{ task['current-comment'].body }}

{% endif %}