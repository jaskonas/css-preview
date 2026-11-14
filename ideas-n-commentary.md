---
layout: page
permalink: /ideas-n-commentary/
title: Ideas and Commentary
parent_title: Resources & Publications
parent_url: /humanitas-journal/
wide: true
excerpt: "Essays and commentary from scholars of the Center for the Study of Statesmanship."
---

<div class="card-grid">
{% assign items = site.commentary | sort: "date" | reverse %}{% for item in items %}{% include news-card.html item=item %}{% endfor %}
</div>
