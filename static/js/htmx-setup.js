document.addEventListener('htmx:configRequest', function(event) {
  var csrfEl = document.querySelector('meta[name="csrf-token"]');
  if (csrfEl) {
    event.detail.headers['X-CSRFToken'] = csrfEl.getAttribute('content');
  }
});

// Alpine/HTMX Integration for Modals
document.addEventListener('htmx:afterSwap', function (evt) {
  var tgt = (evt.detail && evt.detail.target) ? evt.detail.target : evt.target;
  if (tgt && tgt.id === 'modal-content') {
    window.dispatchEvent(new CustomEvent('modal-open'));
  }
});
