---
layout: page
permalink: /nhi-bulletins/
title: NHI Bulletins
parent_title: Resources & Publications
parent_url: /humanitas-journal/
excerpt: "Back issues of the National Humanities Bulletin."
---

<figure class="page-figure"><a href="{{ '/uploads/2020/08/bulletin-spring-1991.pdf' | relative_url }}"><img src="{{ '/uploads/2020/08/NIH-Bulletin.jpg' | relative_url }}" alt="National Humanities Bulletin"></a></figure>

<ul class="doc-list">
{% for b in site.data.bulletins %}
  <li>
    <h2 class="doc-title"><a href="{{ b.pdf | relative_url }}">National Humanities Bulletin<br>{{ b.issue }} (PDF)</a></h2>
    <p class="doc-meta">Including:</p>
    <ul class="doc-contents">{% for c in b.contents %}<li>{{ c }}</li>{% endfor %}</ul>
  </li>
{% endfor %}
</ul>
