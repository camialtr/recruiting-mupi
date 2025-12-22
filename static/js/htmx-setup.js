// Adiciona o token CSRF ao cabeçalho de cada requisição HTMX para proteção contra CSRF
document.addEventListener('htmx:configRequest', function (event) {
    var csrfEl = document.querySelector('meta[name="csrf-token"]');
    if (csrfEl) {
        event.detail.headers['X-CSRFToken'] = csrfEl.getAttribute('content');
    }
});

// Integração Alpine/HTMX para os Modais
document.addEventListener('htmx:afterSwap', function (evt) {
    var tgt = (evt.detail && evt.detail.target) ? evt.detail.target : evt.target;
    if (tgt && tgt.id === 'modal-content') {
        window.dispatchEvent(new CustomEvent('modal-open'));
    }
});

// Exibir erros de resposta no modal em vez de deixar em branco
document.addEventListener('htmx:responseError', function(evt){
    var detail = evt.detail || {};
    var target = (detail.target) ? detail.target : evt.target;
    if (!target || target.id !== 'modal-content') return;
    var status = (detail.xhr && detail.xhr.status) ? detail.xhr.status : 0;
    var msg = 'Erro ao carregar conteúdo (' + status + ').';
    target.innerHTML = '<div class="p-8 text-center text-red-500">' + msg + '</div>';
}, true);

// Abrir modal no clique de elementos que direcionam para #modal-content
document.addEventListener('click', function(evt){
    var el = evt.target.closest('[hx-get],[hx-post],[data-hx-get],[data-hx-post]');
    if (!el) return;
    var targetSel = el.getAttribute('hx-target') || el.getAttribute('data-hx-target');
    if (targetSel === '#modal-content') {
        window.dispatchEvent(new CustomEvent('modal-open'));
        var mc = document.getElementById('modal-content');
        if (mc && !mc.innerHTML.trim()) {
            mc.innerHTML = '<div class="p-8 text-center text-secondary">Carregando...</div>';
        }
    }
}, true);

// Altura dinâmica do painel do modal durante swaps do HTMX
document.addEventListener('htmx:beforeSwap', function (evt) {
    var tgt = (evt.detail && evt.detail.target) ? evt.detail.target : evt.target;
    if (!tgt || tgt.id !== 'modal-content') return;
    var container = document.getElementById('modal-container');
    if (!container || getComputedStyle(container).display === 'none') return;
    var panel = document.getElementById('modal-panel');
    if (!panel) return;
    panel.style.height = panel.offsetHeight + 'px';
    tgt.classList.add('opacity-0');
}, true);

document.addEventListener('htmx:afterSwap', function (evt) {
    var tgt = (evt.detail && evt.detail.target) ? evt.detail.target : evt.target;
    if (!tgt || tgt.id !== 'modal-content') return;
    var container = document.getElementById('modal-container');
    if (!container || getComputedStyle(container).display === 'none') return;
    var panel = document.getElementById('modal-panel');
    if (!panel) return;
    // Measure natural height
    panel.style.height = 'auto';
    requestAnimationFrame(function(){
        var newHeight = panel.offsetHeight + 'px';
        var prevHeight = panel.style.height;
        panel.style.height = prevHeight;
        requestAnimationFrame(function(){
            panel.style.height = newHeight;
            tgt.classList.remove('opacity-0');
            tgt.classList.add('opacity-100');
            setTimeout(function(){
                panel.style.height = 'auto';
                tgt.classList.remove('opacity-100');
            }, 300);
        });
    });
}, true);

// Delay na interação com os botões
// Adiciona um delay visual na interação dos botões para melhor resposta visual
document.addEventListener('click', function (e) {
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

// Implementação do toast personalizado para as interações gerais
document.addEventListener('invalid', function (e) {
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

// Inicialização de animações "reveal" e reobservação após swaps do HTMX
(function(){
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var revealObserver = new IntersectionObserver(function(entries){
        entries.forEach(function(entry){
            var el = entry.target;
            if (entry.isIntersecting) {
                var d = el.getAttribute('data-reveal-delay');
                if (d) el.style.transitionDelay = String(parseInt(d, 10)) + 'ms';
                el.classList.add('reveal-visible');
                var once = el.getAttribute('data-reveal-once');
                if (once === null || once === 'true') revealObserver.unobserve(el);
            } else {
                if (el.getAttribute('data-reveal-reset') === 'true') {
                    el.classList.remove('reveal-visible');
                }
            }
        });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });

    function initReveals(root){
        var scope = root || document;
        var items = scope.querySelectorAll('.reveal');
        if (reduce) {
            items.forEach(function(el){ el.classList.add('reveal-visible'); });
            return;
        }
        items.forEach(function(el){ revealObserver.observe(el); });
    }

    document.addEventListener('DOMContentLoaded', function(){ initReveals(document); });
    document.addEventListener('htmx:afterSwap', function(evt){
        var tgt = (evt.detail && evt.detail.target) ? evt.detail.target : evt.target;
        initReveals(tgt || document);
    });
})();

// Delegação para o widget de estatísticas sem inline scripts
document.addEventListener('click', function(e){
    var el = e.target.closest('.dashboard-stats [data-status]');
    if (!el) return;
    var detail = { status: el.getAttribute('data-status') || '', label: el.getAttribute('data-label') || '' };
    window.dispatchEvent(new CustomEvent('set-status', { detail: detail }));
}, true);

// Componente da notificação flutuante
function toastComponent(){
    return {
        toast: null,
        pushToast(detail) {
            var message = (detail && (detail.message || detail.text)) ? String(detail.message || detail.text) : '';
            if (!message) return;
            var levelRaw = (detail && (detail.level || detail.tags)) ? String(detail.level || detail.tags) : 'info';
            var level = levelRaw.split(' ')[0] || 'info';
            var duration = (detail && detail.duration) ? Number(detail.duration) : 6000;
            var id = String(Date.now()) + '-' + Math.random().toString(16).slice(2);
            if (this.toast && this.toast.timeoutId) clearTimeout(this.toast.timeoutId);
            this.toast = { id: id, level: level, message: message, open: true, duration: duration, timeoutId: null };
            this.toast.timeoutId = setTimeout(() => this.closeToast(), duration);
        },
        closeToast() {
            if (!this.toast) return;
            if (this.toast.timeoutId) clearTimeout(this.toast.timeoutId);
            this.toast.open = false;
            setTimeout(() => { this.toast = null; }, 220);
        }
    };
}

// Leitura de mensagem Django inicial e erro de login
document.addEventListener('DOMContentLoaded', function(){
    var t = document.querySelector('#django-last-message span');
    if (t) {
        var level = t.getAttribute('data-level') || 'info';
        var message = t.getAttribute('data-message') || '';
        if (message) window.dispatchEvent(new CustomEvent('toast-add', { detail: { level: level, message: message } }));
    }
    var le = document.getElementById('login-error');
    if (le) {
        var msg = le.getAttribute('data-message') || '';
        if (msg) window.dispatchEvent(new CustomEvent('toast-add', { detail: { level: 'error', message: msg } }));
    }
});

// Smooth scroll para âncoras internas (links com href="#..." ou [data-scroll-target])
document.addEventListener('click', function(e){
    var link = e.target.closest('a[href^="#"], [data-scroll-target]');
    if (!link) return;
    var selector = link.getAttribute('href') || link.getAttribute('data-scroll-target');
    if (!selector || selector.charAt(0) !== '#') return;
    var target = document.querySelector(selector);
    if (!target) return;
    e.preventDefault();
    target.scrollIntoView({ behavior: 'smooth' });
}, true);

// Componente do Hero
function heroComponent(){
    var state = { scroll: 0, loaded: false, heroHeight: 0, badgeClicks: 0, revealLogin: false };
    setTimeout(function(){ state.loaded = true; window.scrollTo(0, 1); }, 100);
    requestAnimationFrame(function(){
        var el = document.getElementById('lp-hero');
        if (el) state.heroHeight = el.offsetHeight;
    });
    window.addEventListener('scroll', function(){ state.scroll = window.pageYOffset || 0; }, { passive: true });
    window.addEventListener('resize', function(){
        var el = document.getElementById('lp-hero');
        if (el) state.heroHeight = el.offsetHeight;
    }, { passive: true });
    document.addEventListener('click', function(e){
        var b = e.target.closest('[data-hero-badge]');
        if (!b) return;
        state.badgeClicks += 1;
        if (state.badgeClicks >= 3) state.revealLogin = true;
    }, true);
    return state;
}

// Componente do Console
function consoleSwitchComponent(){
    return {
        mode: 'joycon',
        swapping: false,
        swapTimer: null,
        init(){
            var root = this.$el;
            var initial = root.getAttribute('data-mode');
            if (initial) this.mode = initial;
            root.addEventListener('click', (e) => {
                var btn = e.target.closest('[data-switch-mode]');
                if (!btn) return;
                var next = btn.getAttribute('data-switch-mode');
                if (!next || next === this.mode) return;
                this.mode = next;
                root.setAttribute('data-mode', this.mode);
                root.classList.add('swapping');
                clearTimeout(this.swapTimer);
                this.swapTimer = setTimeout(() => { root.classList.remove('swapping'); }, 450);
            });
        }
    };
}

// Utilitário: aplicar classes padronizadas em inputs
function applyInputClasses(scope){
    var root = scope || document;
    var inputs = root.querySelectorAll('input[type="text"], input[type="email"], input[type="search"], input[type="date"], textarea');
    inputs.forEach(function(input){
        if (!input.classList.contains('input')) input.classList.add('input');
        if (!input.classList.contains('w-full')) input.classList.add('w-full');
    });
}
document.addEventListener('DOMContentLoaded', function(){ applyInputClasses(document); });
document.addEventListener('htmx:afterSwap', function(evt){
    var tgt = (evt.detail && evt.detail.target) ? evt.detail.target : evt.target;
    applyInputClasses(tgt || document);
}, true);
