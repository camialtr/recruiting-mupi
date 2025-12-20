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

// Button Interaction Delay
// Adds a visual delay to primary buttons to ensure the user perceives the animation smoothness
document.addEventListener('click', function(e) {
  if (!e.isTrusted) return;
  const btn = e.target.closest('[data-delay-click]');
  if (!btn) return;
  e.preventDefault();
  e.stopImmediatePropagation();
  btn.classList.add('simulate-active');
  setTimeout(() => {
    btn.classList.remove('simulate-active');
    btn.click();
  }, 200);
}, true);

document.addEventListener('invalid', function(e) {
  const el = e.target;
  if (!(el instanceof HTMLElement)) return;
  const form = el.closest('form[data-toast-validate]');
  if (!form) return;

  e.preventDefault();

  const now = Date.now();
  if (form.__toastInvalidAt && (now - form.__toastInvalidAt) < 600) return;
  form.__toastInvalidAt = now;

  const label = el.id ? document.querySelector(`label[for="${CSS.escape(el.id)}"]`) : null;
  const labelText = label ? label.textContent.trim().replace(/\s+\*$/, '') : '';
  const msg = labelText ? `${labelText}: ${el.validationMessage}` : el.validationMessage;

  window.dispatchEvent(new CustomEvent('toast-add', { detail: { level: 'error', message: msg } }));
  if (typeof el.focus === 'function') el.focus();
}, true);
