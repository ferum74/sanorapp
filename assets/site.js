/* Sanor website — tiny shared script: FAQ accordion + scroll reveal. No tracking, no dependencies. */
(function () {
  'use strict';

  // FAQ accordion (works for the home page .faq-q and the support page .faq-question buttons)
  window.toggleFAQ = function (btn) {
    var item = btn.closest('.faq-item');
    var wasOpen = item.classList.contains('open');
    var scope = item.parentElement;
    scope.querySelectorAll('.faq-item.open').forEach(function (el) {
      el.classList.remove('open');
      var b = el.querySelector('button');
      if (b) b.setAttribute('aria-expanded', 'false');
    });
    if (!wasOpen) {
      item.classList.add('open');
      btn.setAttribute('aria-expanded', 'true');
    }
  };

  document.querySelectorAll('.faq-item > button').forEach(function (b) {
    b.setAttribute('aria-expanded', b.closest('.faq-item').classList.contains('open') ? 'true' : 'false');
    if (!b.getAttribute('onclick')) b.addEventListener('click', function () { window.toggleFAQ(b); });
  });

  // Scroll reveal
  var els = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    els.forEach(function (el) { el.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  els.forEach(function (el) { io.observe(el); });
})();
