=========
Copyright
=========

.. raw:: html

  <div>
  {% for p in site.sorted_plugins %}{{p.get_site_info()|safe}}{% endfor %}
  </div>
