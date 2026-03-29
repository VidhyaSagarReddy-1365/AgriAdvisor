const API_BASE_URL = "https://agriadvisor-qxhj.onrender.com";

// ============================================
// Global Custom Alert UI
// ============================================

function injectCustomAlert() {
    if (document.getElementById("custom-alert-overlay")) return;

    const overlay = document.createElement("div");
    overlay.id = "custom-alert-overlay";
    overlay.className = "custom-alert-overlay";

    overlay.innerHTML = `
        <div class="custom-alert-box">
            <div class="custom-alert-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
            </div>
            <p id="custom-alert-message"></p>
            <button id="custom-alert-btn">OK</button>
        </div>
    `;

    document.body.appendChild(overlay);

    document.getElementById("custom-alert-btn").addEventListener("click", () => {
        overlay.classList.remove("visible");
        setTimeout(() => overlay.classList.add("hidden"), 300); // Wait for transition
    });
}

function showAlertQueue(message) {
    injectCustomAlert();
    const overlay = document.getElementById("custom-alert-overlay");
    const msgEl = document.getElementById("custom-alert-message");
    
    // reset visibility logic allowing consecutive calls
    overlay.classList.remove("hidden");
    msgEl.textContent = message;
    
    // trigger animation
    setTimeout(() => {
        overlay.classList.add("visible");
    }, 10);
}

// Override native alert
window.alert = function(message) {
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", () => showAlertQueue(message));
    } else {
        showAlertQueue(message);
    }
};