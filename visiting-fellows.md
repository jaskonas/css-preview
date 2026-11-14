---
layout: page
permalink: /visiting-fellows/
title: Visiting Fellows
wide: true
excerpt: "Current and previous visiting fellows of the Center for the Study of Statesmanship."
---

{% for key in site.data.groups.visiting-fellows-page.sections %}{% assign g = site.data.groups[key] %}
<h2 class="group-title">{{ g.title }}</h2>
{% include team-group.html group=key %}
{% endfor %}
