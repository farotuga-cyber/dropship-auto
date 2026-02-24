---
layout: default
---

# Loja Dropship Automática

Bem‑vindo à nossa loja! Navegue os produtos abaixo:

<ul>
{% for page in site.pages %}
  {% if page.layout == "product" %}
    <li><a href="{{ page.url }}">{{ page.title }}</a> – {{ page.price | prepend: '$' }}</li>
  {% endif %}
{% endfor %}
</ul>
