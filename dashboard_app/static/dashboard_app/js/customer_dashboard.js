// static/dashboard_app/js/customer_dashboard.js

// --- DASHBOARD ANIMATIONS & TOASTS ONLY ---
document.addEventListener('DOMContentLoaded', function () {

    // Auto-dismiss toast messages after 5 seconds
    document.querySelectorAll('.alert').forEach(function (alertEl) {
        setTimeout(function () {
            alertEl.style.transition = 'opacity 0.5s, transform 0.5s';
            alertEl.style.opacity = '0';
            alertEl.style.transform = 'translateX(30px)';
            setTimeout(function () { alertEl.remove(); }, 500);
        }, 5000);
    });

    // Animate pipeline bars using data-width
    document.querySelectorAll('.pipeline-bar-fill').forEach(function (bar) {
        const targetWidth = bar.getAttribute('data-width') || '0';
        bar.style.width = '0%';
        setTimeout(function () {
            bar.style.width = targetWidth + '%';
        }, 400);
    });

});