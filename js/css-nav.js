/* Mobile menu toggle. Below the nav breakpoint the menu is hidden (only when
   JS runs — see html.js in _css-header.scss) and opened by .menu-open.
   Same-page anchor links close the menu after navigating. */
(function () {
  "use strict";
  var masthead = document.getElementById("masthead");
  var btn = document.getElementById("menu-toggle");
  if (!masthead || !btn) return;

  function setOpen(open) {
    masthead.classList.toggle("menu-open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  }

  btn.addEventListener("click", function () {
    setOpen(!masthead.classList.contains("menu-open"));
  });

  masthead.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest(".top-nav a");
    if (a && a.hash && a.pathname === location.pathname) setOpen(false);
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && masthead.classList.contains("menu-open")) {
      setOpen(false);
      btn.focus();
    }
  });
})();
