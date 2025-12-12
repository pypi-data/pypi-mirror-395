{% if 'current-comment' in task %}
{% include 'system_comment.md' %}
{% else %}
{% include 'system_ticket.md' %}
{% endif %}
