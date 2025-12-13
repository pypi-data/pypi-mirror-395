{{h1("Local help for "+settings.SITE.title)}}

Welcome to the :term:`local help pages` of the
**{{settings.SITE.title}}** site.

{{doc2rst(settings.SITE.__doc__)}}

.. toctree::
    :maxdepth: 1

    actors
{% if include_useless %}
    plugins
    models
{% endif %}
    copyright
