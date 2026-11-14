---
layout: page
permalink: /epistulae/
title: Epistulae
parent_title: Resources & Publications
parent_url: /humanitas-journal/
excerpt: "Epistulae — an occasional publication of the National Humanities Institute."
---

<figure class="page-figure"><img src="{{ '/uploads/2021/11/Epistulae.jpg' | relative_url }}" alt="Epistulae"></figure>

**_Epistulae_**<br>
Luke C. Sheahan, Editor<br>
<a href="mailto:epistulae@nhinet.org">epistulae@nhinet.org</a>

_Epistulae_ (ə-pis´-tŭ-lā), Latin (n., pl.): letters or correspondence. An occasional publication of the National Humanities Institute, _Epistulae_ seeks to provide clarity and insight on significant issues of our time. While addressed to the educated public, it aspires to high scholarly standards.

<ul class="doc-list">
{% for e in site.data.epistulae %}
  <li>
    <p class="doc-kicker">Epistulae No. {{ e.number }} · {{ e.category }}</p>
    <h2 class="doc-title">{% if e.html %}<a href="{{ '/epistulae-no-' | append: e.number | append: '/' | relative_url }}">{{ e.title }}</a>{% else %}{{ e.title }}{% endif %}</h2>
    <p class="doc-meta">By {{ e.author }}</p>
    <p class="doc-links">{% if e.html %}<a href="{{ '/epistulae-no-' | append: e.number | append: '/' | relative_url }}">HTML</a>{% endif %}<a href="{{ e.pdf | relative_url }}">PDF</a></p>
  </li>
{% endfor %}
</ul>
