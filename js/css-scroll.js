/* Sticky header: tightens padding and shrinks the logo once the page
   scrolls. Adds .is-scrolled to #masthead. */
(function () {
  "use strict";
  var masthead = document.getElementById("masthead");
  if (!masthead) return;

  function tick() {
    masthead.classList.toggle("is-scrolled", window.scrollY > 60);
  }

  window.addEventListener("scroll", tick, { passive: true });
  tick();
})();
