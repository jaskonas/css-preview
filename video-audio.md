---
layout: page
permalink: /video-audio/
title: Video & Audio
parent_title: Resources & Publications
parent_url: /humanitas-journal/
wide: true
excerpt: "Podcasts, conference video and recorded events from the Center for the Study of Statesmanship."
---

<div class="card-grid">
{% assign items = site.news | sort: "date" | reverse %}{% for item in items %}{% if item.youtube or item.soundcloud or item.vimeo %}{% include news-card.html item=item %}{% endif %}{% endfor %}
</div>
