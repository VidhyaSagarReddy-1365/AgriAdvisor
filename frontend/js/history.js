// ============================================
// AgriAdvisor - history.js
// Fetches prediction history from FastAPI
// ============================================


window.onload = async function () {

    requireLogin();

    const token = localStorage.getItem("token");
    const list  = document.getElementById("history-list");

    try {
        const response = await fetch(`${API_URL}/history`, {
            headers: { "Authorization": `Bearer ${token}` }
        });

        const data = await response.json();

        if (!response.ok) {
            list.innerHTML = `<p style="color:#e74c3c;">${data.detail || "Failed to load history."}</p>`;
            return;
        }

        const records = data.history;

        if (records.length === 0) {
            list.innerHTML = `
                <div class="empty-history">
                    <p>No predictions yet.</p>
                    <p>Go to Predict page and submit your first prediction!</p>
                </div>
            `;
            return;
        }

        list.innerHTML = "";

        records.forEach((record, index) => {

            const topCrop = record.result.top_crops[0];
            const date    = new Date(record.timestamp).toLocaleString("en-IN", {
                day:    "2-digit",
                month:  "short",
                year:   "numeric",
                hour:   "2-digit",
                minute: "2-digit"
            });

            const price = typeof topCrop.price === "number"
                ? `₹${topCrop.price}`
                : topCrop.price;

            const card = document.createElement("div");
            card.className = "history-item";
            card.innerHTML = `
                <div class="history-header">
                    <span class="history-crop">🌱 ${topCrop.name}</span>
                    <span class="history-date">${date}</span>
                </div>
                <div class="history-details">
                    <span><strong>Confidence:</strong> ${topCrop.confidence.toFixed(2)}%</span>
                    <span><strong>Price:</strong> ${price}</span>
                    <span><strong>N/P/K:</strong> ${record.inputs.n} / ${record.inputs.p} / ${record.inputs.k}</span>
                    <span><strong>pH:</strong> ${record.inputs.ph}</span>
                    <span><strong>Rainfall:</strong> ${record.inputs.rainfall} mm</span>
                    <span><strong>Water:</strong> ${record.inputs.water_availability}</span>
                </div>
                <p class="history-advice">${record.result.advice}</p>
            `;
            list.appendChild(card);
        });

    } catch (err) {
        list.innerHTML = `<p style="color:#e74c3c;">Cannot connect to server. Make sure FastAPI is running.</p>`;
        console.error(err);
    }
};
