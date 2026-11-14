/* Carousel controls — progressive enhancement over a native scroll-snap
   track. Each .carousel-controls[data-carousel-for="<id>"] pages that track
   by one card; buttons disable at either end. Without JS the track still
   scrolls horizontally. */
(function () {
  "use strict";

  var groups = Array.prototype.slice.call(document.querySelectorAll(".carousel-controls"));
  if (!groups.length) return;

  groups.forEach(function (controls) {
    var track = document.getElementById(controls.getAttribute("data-carousel-for"));
    if (!track) return;
    var prev = controls.querySelector('[data-dir="-1"]');
    var next = controls.querySelector('[data-dir="1"]');

    function step() {
      var card = track.firstElementChild;
      if (!card) return track.clientWidth;
      var gap = parseFloat(getComputedStyle(track).columnGap) || 0;
      return card.getBoundingClientRect().width + gap;
    }

    function update() {
      var max = track.scrollWidth - track.clientWidth - 2;
      prev.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft >= max;
    }

    function go(dir) { track.scrollBy({ left: dir * step(), behavior: "smooth" }); }

    prev.addEventListener("click", function () { go(-1); });
    next.addEventListener("click", function () { go(1); });

    // Arrow keys page the track when it has focus.
    track.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); go(1); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); go(-1); }
    });

    track.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  });
})();
