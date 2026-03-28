// ============================================
// AgriAdvisor - auth.js
// Handles login, register, forgot password
// via FastAPI backend with JWT
// ============================================

// // ⚠️ Update this URL after Render deployment
// const API_URL = "https://agriadvisor-qxhj.onrender.com";


/* ================= LOGIN ================= */

async function loginUser(event) {

    event.preventDefault();

    const email    = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!email || !password) {
        alert("Please fill in all fields.");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/login`, {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || "Login failed.");
            return;
        }

        // Save JWT token and user info
        localStorage.setItem("token", data.token);
        localStorage.setItem("userName",  data.name);
        localStorage.setItem("userEmail", data.email);

        window.location.href = "predict.html";

    } catch (err) {
        alert("Cannot connect to server. Make sure FastAPI is running.");
        console.error(err);
    }
}


/* ================= REGISTER ================= */

async function registerUser(event) {

    event.preventDefault();

    const name            = document.getElementById("name").value.trim();
    const email           = document.getElementById("email").value.trim();
    const password        = document.getElementById("password").value.trim();
    const confirmPassword = document.getElementById("confirmPassword").value.trim();
    const answer1         = document.getElementById("answer1").value.trim();
    const answer2         = document.getElementById("answer2").value.trim();

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!name)                        { alert("Name cannot be empty.");            return; }
    if (!emailPattern.test(email))    { alert("Enter a valid email.");             return; }
    if (password.length < 6)          { alert("Password must be 6+ characters.");  return; }
    if (password !== confirmPassword) { alert("Passwords do not match.");          return; }
    if (!answer1 || !answer2)         { alert("Please answer security questions."); return; }

    try {
        const response = await fetch(`${API_URL}/register`, {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify({ name, email, password, answer1, answer2 })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || "Registration failed.");
            return;
        }

        alert("Registration successful! Please login.");
        window.location.href = "login.html";

    } catch (err) {
        alert("Cannot connect to server. Make sure FastAPI is running.");
        console.error(err);
    }
}


/* ================= RESET PASSWORD ================= */

async function resetPassword(event) {

    event.preventDefault();

    const email       = document.getElementById("email").value.trim();
    const answer1     = document.getElementById("answer1").value.trim();
    const answer2     = document.getElementById("answer2").value.trim();
    const newPassword = document.getElementById("newPassword").value.trim();

    if (!email || !answer1 || !answer2 || !newPassword) {
        alert("Please fill in all fields.");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/reset-password`, {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify({
                email,
                answer1,
                answer2,
                new_password: newPassword
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || "Reset failed.");
            return;
        }

        alert("Password reset successful! Please login.");
        window.location.href = "login.html";

    } catch (err) {
        alert("Cannot connect to server. Make sure FastAPI is running.");
        console.error(err);
    }
}


/* ================= LOGOUT ================= */

function logoutUser() {
    localStorage.removeItem("token");
    localStorage.removeItem("userName");
    localStorage.removeItem("userEmail");
    localStorage.removeItem("predictionResult");
    localStorage.removeItem("predictionInputs");
    window.location.href = "login.html";
}


/* ================= SESSION GUARD ================= */
// Call this at the top of any protected page (predict, history, profile)

function requireLogin() {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "login.html";
    }
}