document.addEventListener('DOMContentLoaded', function () {
    const body = document.body;

    // ===== DESKTOP SIDEBAR TOGGLE =====
    const navToggle = document.getElementById("navToggle");

    function updateNavToggleIcon(isHidden) {
        if (!navToggle) return;
        const icon = navToggle.querySelector("i");
        if (!icon) return;
        if (isHidden) {
            icon.classList.remove("fa-angle-double-left");
            icon.classList.add("fa-angle-double-right");
            navToggle.title = "Show sidebar";
        } else {
            icon.classList.remove("fa-angle-double-right");
            icon.classList.add("fa-angle-double-left");
            navToggle.title = "Hide sidebar";
        }
    }

    function applySavedNavPreference() {
        const saved = localStorage.getItem("certiNavHidden");
        const shouldHide = saved === "1";
        if (shouldHide) body.classList.add("nav-hidden");
        else body.classList.remove("nav-hidden");
        updateNavToggleIcon(shouldHide);
    }

    if (navToggle) {
        applySavedNavPreference();
        navToggle.addEventListener("click", () => {
            const isHiddenNow = body.classList.toggle("nav-hidden");
            localStorage.setItem("certiNavHidden", isHiddenNow ? "1" : "0");
            updateNavToggleIcon(isHiddenNow);
        });
    }

    // ===== MOBILE SIDEBAR TOGGLE =====
    const menuToggle = document.getElementById("menuToggle");
    const sidebar    = document.getElementById("sidebar");
    const overlay    = document.getElementById("overlay");

    if (menuToggle) {
        menuToggle.addEventListener("click", () => {
            sidebar.classList.toggle("active");
            overlay.classList.toggle("active");
        });
    }

    if (overlay) {
        overlay.addEventListener("click", () => {
            sidebar.classList.remove("active");
            overlay.classList.remove("active");
        });
    }

    // ===== DROPDOWNS =====
    const notifBtn       = document.getElementById("notifBtn");
    const notifDropdown  = document.getElementById("notifDropdown");
    const notifList      = document.getElementById("notifList");
    const notifBadge     = document.querySelector(".notification-badge");
    const clearNotifBtn  = document.getElementById("clearNotifBtn");
    const profileBtn     = document.getElementById("profileBtn");
    const profileDropdown = document.getElementById("profileDropdown");

    function renderNotifications(data) {
        if (!notifList) return;
        notifList.innerHTML = "";

        if (!data || !data.notifications || data.notifications.length === 0) {
            const emptyDiv = document.createElement("div");
            emptyDiv.className = "dropdown-empty";
            emptyDiv.textContent = "No new notifications";
            notifList.appendChild(emptyDiv);
            if (notifBadge) notifBadge.style.display = "none";
            return;
        }

        data.notifications.forEach(n => {
            const item = document.createElement("div");
            item.className = "dropdown-item";

            const title = document.createElement("div");
            title.className = "dropdown-item-title";
            title.textContent = n.title || "Notification";

            const msg = document.createElement("div");
            msg.className = "dropdown-item-message";
            msg.textContent = n.message || "";

            const time = document.createElement("div");
            time.className = "dropdown-item-time";
            time.textContent = n.time || "";

            item.append(title, msg, time);
            notifList.appendChild(item);
        });

        if (notifBadge) notifBadge.style.display = "none";
    }

    function fetchNotifications() {
        // Now safely uses the global URL passed from HTML
        fetch(window.DASHBOARD_URLS.notificationsApi)
            .then(r => r.json())
            .then(data => renderNotifications(data))
            .catch(err => console.error("Notifications error:", err));
    }

    if (notifBtn && notifDropdown) {
        notifBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            const isOpening = !notifDropdown.classList.contains("active");
            if (profileDropdown) profileDropdown.classList.remove("active");
            notifDropdown.classList.toggle("active");
            if (isOpening) fetchNotifications();
        });
    }

    if (clearNotifBtn) {
        clearNotifBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
            
            fetch(window.DASHBOARD_URLS.clearNotificationsApi, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({})
            })
            .then(r => r.json())
            .then(() => renderNotifications({ notifications: [] }))
            .catch(err => console.error("Clear notif error:", err));
        });
    }

    if (profileBtn) {
        profileBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            profileDropdown.classList.toggle("active");
            if (notifDropdown) notifDropdown.classList.remove("active");
        });
    }

    document.addEventListener("click", (e) => {
        if (notifDropdown && notifBtn && !notifDropdown.contains(e.target) && !notifBtn.contains(e.target))
            notifDropdown.classList.remove("active");
        if (profileDropdown && profileBtn && !profileDropdown.contains(e.target) && !profileBtn.contains(e.target))
            profileDropdown.classList.remove("active");
    });

    // ===== UNIFIED MODAL LOGIC =====
    // This handles both the .show method (for logout) and the .active method (for new requests)
    window.openModal = function(e, modalId) {
        // Support calls that don't pass an event
        if (!modalId) {
            modalId = e;
            e = null;
        } else if (e && typeof e.preventDefault === 'function') {
            e.preventDefault();
        }

        const m = document.getElementById(modalId);
        if (m) {
            m.style.display = 'flex';
            setTimeout(() => {
                m.classList.add("show");
                m.classList.add("active");
            }, 10);
        }
    };

    window.closeModal = function(modalId) {
        const m = document.getElementById(modalId);
        if (m) {
            m.classList.remove("show");
            m.classList.remove("active");
            setTimeout(() => m.style.display = 'none', 300);
        }
    };

    // Close modals by clicking outside
    document.querySelectorAll(".modal, .modal-overlay, .nrm__backdrop").forEach(modal => {
        modal.addEventListener("click", e => {
            if (e.target === modal) {
                modal.classList.remove("show");
                modal.classList.remove("active");
                setTimeout(() => modal.style.display = 'none', 300);
            }
        });
    });

    // NEW REQUEST MODAL — Delivery / Shipping toggle
    const nrmDelivPickup  = document.getElementById('nrmDelivPickup');
    const nrmDelivCourier = document.getElementById('nrmDelivCourier');
    const nrmShippingBlock = document.getElementById('nrmShippingBlock');
    const nrmShippingAddr  = document.getElementById('nrmShippingAddr');

    function nrmUpdateDelivery() {
        if (!nrmShippingBlock) return;
        const isCourier = nrmDelivCourier && nrmDelivCourier.checked;
        if (isCourier) {
            nrmShippingBlock.classList.add('nrm__visible');
            if (nrmShippingAddr) nrmShippingAddr.required = true;
        } else {
            nrmShippingBlock.classList.remove('nrm__visible');
            if (nrmShippingAddr) { nrmShippingAddr.required = false; nrmShippingAddr.value = ''; }
        }
    }

    if (nrmDelivPickup)  nrmDelivPickup.addEventListener('change', nrmUpdateDelivery);
    if (nrmDelivCourier) nrmDelivCourier.addEventListener('change', nrmUpdateDelivery);
    nrmUpdateDelivery(); 



    // ===== LOGOUT =====
    const sidebarLogoutBtn  = document.getElementById("sidebarLogoutBtn");
    const dropdownLogoutBtn = document.getElementById("dropdownLogoutBtn");
    const confirmLogout     = document.getElementById("confirmLogout");

    if (sidebarLogoutBtn)
        sidebarLogoutBtn.addEventListener("click", e => { e.preventDefault(); openModal('logoutModal'); });
    if (dropdownLogoutBtn)
        dropdownLogoutBtn.addEventListener("click", e => { e.preventDefault(); profileDropdown.classList.remove("active"); openModal('logoutModal'); });
    
    // Now safely uses the global URL passed from HTML
    if (confirmLogout)
        confirmLogout.addEventListener("click", () => window.location.href = window.DASHBOARD_URLS.logoutUrl);
});