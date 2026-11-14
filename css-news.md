---
layout: page
permalink: /css-news/
title: CSS News
wide: true
excerpt: "News, events, podcasts and video from the Center for the Study of Statesmanship."
---

<div class="card-grid">
{% assign items = site.news | sort: "date" | reverse %}{% for item in items %}{% include news-card.html item=item %}{% endfor %}
</div>
