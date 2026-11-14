---
layout: page
permalink: /events/
title: Events
excerpt: "Events hosted and co-sponsored by the Center for the Study of Statesmanship."
---

{% assign today = site.time | date: "%Y-%m-%d" %}{% assign upcoming = "" | split: "" %}{% assign past = "" | split: "" %}
{% assign evs = site.events | sort: "date" %}{% for e in evs %}{% assign d = e.date | date: "%Y-%m-%d" %}{% if d >= today %}{% assign upcoming = upcoming | push: e %}{% else %}{% assign past = past | unshift: e %}{% endif %}{% endfor %}

{% if upcoming.size == 0 %}<p class="notice">There are no upcoming events.</p>{% else %}
<ul class="doc-list">{% for e in upcoming %}{% include event-item.html event=e %}{% endfor %}</ul>
{% endif %}

<h2>Latest Past Events</h2>
<ul class="doc-list">{% for e in past %}{% include event-item.html event=e %}{% endfor %}</ul>
