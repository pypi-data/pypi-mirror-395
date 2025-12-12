{{header(1,"{} (``{}``)".format(actor.get_actor_label(), str(actor)))}}

.. - Technical docs:  {{refto(actor)}}

.. - Database model: {{refto(actor.model)}})

{{actor_overview(actor)}}

.. {#doc2rst(actor.__doc__)#}

{#
{{header(2, str(_("Filter parameters")))}}

{% if actor.parameters %}
{{doctest.fields_help(actor, all=True)}}
{% endif %}
#}
