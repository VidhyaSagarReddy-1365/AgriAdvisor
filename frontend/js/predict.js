// ============================================
// AgriAdvisor - predict.js
// Sends form data to FastAPI and stores result
// ============================================


async function predictCrop(event) {

    event.preventDefault();

    // --- Read all form values ---
    const data = {
        n:                  parseFloat(document.getElementById("n").value),
        p:                  parseFloat(document.getElementById("p").value),
        k:                  parseFloat(document.getElementById("k").value),
        temperature:        parseFloat(document.getElementById("temperature").value),
        humidity:           parseFloat(document.getElementById("humidity").value),
        ph:                 parseFloat(document.getElementById("ph").value),
        rainfall:           parseFloat(document.getElementById("rainfall").value),
        irrigation_type:    document.getElementById("irrigation").value,
        water_availability: document.getElementById("water").value,
        market_type:        document.getElementById("market").value,
        market_distance:    document.getElementById("distance").value,
    };

    // --- Get JWT token from localStorage ---
    const token = localStorage.getItem("token");
    if (!token) {
        alert("Session expired. Please login again.");
        window.location.href = "login.html";
        return;
    }

    // --- Show loading state ---
    const btn = document.querySelector("button[type='submit']");
    btn.textContent = "⏳ Predicting...";
    btn.disabled = true;

    try {
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: "POST",
            headers: {
                "Content-Type":  "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.detail || "Prediction failed. Try again.");
            btn.textContent = "🌱 Get Recommendation";
            btn.disabled = false;
            return;
        }

        // --- Save result + inputs to localStorage for result.html ---
        localStorage.setItem("predictionResult", JSON.stringify(result));
        localStorage.setItem("predictionInputs", JSON.stringify(data));

        // --- Redirect to result page ---
        window.location.href = "result.html";

    } catch (error) {
        alert("Cannot connect to server. Make sure FastAPI is running.");
        console.error(error);
        btn.textContent = "🌱 Get Recommendation";
        btn.disabled = false;
    }
}
