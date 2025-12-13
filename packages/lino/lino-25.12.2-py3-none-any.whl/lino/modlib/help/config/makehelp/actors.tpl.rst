{{header(1, str(_("Data tables")))}}

.. toctree::
    :maxdepth: 2
    :hidden:

{% for a in actors.actors_list if not a.abstract %}
    {{a}}{{makehelp.generate('makehelp/actor.tpl.rst', str(a)+'.rst', actor=a)}}
{% endfor  %}

{{actors2table()}}
