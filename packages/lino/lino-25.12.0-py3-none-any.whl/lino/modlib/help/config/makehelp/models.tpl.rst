{{header(1, str(_("Database models")))}}

.. toctree::
    :maxdepth: 2
    :hidden:

{% for m in get_models() %}
    {{full_model_name(m)}}
{% endfor  %}

{% for m in get_models() %}
- :doc:`{{full_model_name(m)}}` :
  {{abstract(m, 2)}}
  {{makehelp.generate('makehelp/model.tpl.rst', full_model_name(m)+'.rst', model=m)}}

{% endfor  %}
