---
layout: page
permalink: /humanitas-journal/
title: Resources & Publications
excerpt: "Publications, commentary and recordings from the Center for the Study of Statesmanship."
---

<ul class="doc-list">
  <li><h2 class="doc-title"><a href="{{ '/epistulae/' | relative_url }}">Epistulae</a></h2><p class="doc-meta">An occasional publication of the National Humanities Institute.</p></li>
  <li><h2 class="doc-title"><a href="{{ '/ideas-n-commentary/' | relative_url }}">Ideas &amp; Commentary</a></h2><p class="doc-meta">Essays and commentary from CSS scholars.</p></li>
  <li><h2 class="doc-title"><a href="{{ '/nhi-bulletins/' | relative_url }}">NHI Bulletins</a></h2><p class="doc-meta">Back issues of the National Humanities Bulletin.</p></li>
  <li><h2 class="doc-title"><a href="{{ '/video-audio/' | relative_url }}">Video &amp; Audio</a></h2><p class="doc-meta">Podcasts, conference video and recorded events.</p></li>
</ul>

{% assign hum = site.humanitas | sort: "date" | reverse %}{% if hum.size > 0 %}
<h2>From <em>Humanitas</em></h2>
<ul class="doc-list">{% for h in hum %}
  <li><h3 class="doc-title"><a href="{{ h.url | relative_url }}">{{ h.title }}</a></h3><p class="doc-meta">{% if h.author %}By {{ h.author }} · {% endif %}{{ h.date | date: '%B %-d, %Y' }}</p></li>{% endfor %}
</ul>{% endif %}
