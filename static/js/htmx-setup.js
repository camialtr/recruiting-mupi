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
  // Allow programmatic clicks (isTrusted is false) to pass through
  if (!e.isTrusted) return;

  // Find the closest button or link with button classes
  // Focus specifically on btn-primary (black button) as requested, but generally good for all action buttons
  const btn = e.target.closest('.btn-primary, button[type="submit"]');
  
  // If no button found, or it's a secondary/link that doesn't need forced delay, skip
  // Note: logic can be expanded. Here we target the "black button" emphasis.
  if (!btn) return;

  // Prevent immediate action
  e.preventDefault();
  e.stopImmediatePropagation();

  // Add visual feedback class
  btn.classList.add('simulate-active');

  // Wait for visual feedback (smooth animation), then trigger the actual action
  // 150ms matches the active entry/perception time, allowing the scale down to register
  setTimeout(() => {
    btn.classList.remove('simulate-active');
    btn.click();
  }, 200); // 200ms delay to ensure the "smoothness" is felt before navigation/action
}, true); // Capture phase to intercept before HTMX/Alpine
