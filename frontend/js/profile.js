// ============================================
// AgriAdvisor - profile.js (Updated)
// ============================================

window.addEventListener("load", loadProfile);

async function loadProfile() {

    requireLogin();

    const token = localStorage.getItem("token");

    if (!token) {
        alert("Session expired. Please login again.");
        window.location.href = "login.html";
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/profile`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Failed to load profile.");
        }

        document.getElementById("profile-name").textContent  = data.name || "N/A";
        document.getElementById("profile-email").textContent = data.email || "N/A";

    } catch (err) {
        console.error("Profile Load Error:", err);
        alert(err.message || "Cannot connect to server.");
    }
}


// ============================================
// Change Password Function
// ============================================

function togglePasswordForm() {
    const container = document.getElementById("password-form-container");
    const btn = document.getElementById("toggle-password-btn");
    if (container.style.display === "none" || container.style.display === "") {
        container.style.display = "block";
        btn.textContent = "Cancel Update";
    } else {
        container.style.display = "none";
        btn.textContent = "Update password";
        // Clear fields on cancel
        document.getElementById("answer1").value = "";
        document.getElementById("answer2").value = "";
        document.getElementById("new-password").value = "";
        document.getElementById("confirm-password").value = "";
    }
}

async function changePassword() {

    const answer1         = document.getElementById("answer1").value.trim();
    const answer2         = document.getElementById("answer2").value.trim();
    const newPassword     = document.getElementById("new-password").value.trim();
    const confirmPassword = document.getElementById("confirm-password").value.trim();

    // Validation
    if (!answer1 || !answer2 || !newPassword || !confirmPassword) {
        alert("Please fill in all fields (security answers and passwords).");
        return;
    }

    if (newPassword.length < 6) {
        alert("Password must be at least 6 characters.");
        return;
    }

    if (newPassword !== confirmPassword) {
        alert("Passwords do not match.");
        return;
    }

    const token = localStorage.getItem("token");

    if (!token) {
        alert("Session expired. Please login again.");
        window.location.href = "login.html";
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/change-password`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                answer1: answer1,
                answer2: answer2,
                new_password: newPassword
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Failed to update password.");
        }

        alert("Password updated successfully!");

        // Clear fields and hide form
        togglePasswordForm();

    } catch (err) {
        console.error("Password Change Error:", err);
        alert(err.message || "Cannot connect to server.");
    }
}