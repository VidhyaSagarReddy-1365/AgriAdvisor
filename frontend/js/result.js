// ============================================
// AgriAdvisor - result.js (Final)
// Confidence bars + Local Crop Images + Advice
// ============================================

// ── CROP EMOJI MAP ──
const CROP_EMOJI = {
    "rice":         "🌾",
    "maize":        "🌽",
    "wheat":        "🌾",
    "chickpea":     "🫘",
    "kidneybeans":  "🫘",
    "pigeonpeas":   "🫘",
    "mothbeans":    "🫘",
    "mungbean":     "🫘",
    "blackgram":    "🖤",
    "lentil":       "🫘",
    "pomegranate":  "🍎",
    "banana":       "🍌",
    "mango":        "🥭",
    "grapes":       "🍇",
    "watermelon":   "🍉",
    "muskmelon":    "🍈",
    "apple":        "🍎",
    "orange":       "🍊",
    "papaya":       "🍈",
    "coconut":      "🥥",
    "cotton":       "🌿",
    "jute":         "🌿",
    "coffee":       "☕",
};

// ── CROP IMAGE MAP — Local assets folder ──
// Exact filenames from your assets folder
const CROP_IMAGES = {
    "rice":        "assets/rice.webp",
    "maize":       "assets/maize.jpeg",
    "wheat":       "assets/wheat.jpg",
    "chickpea":    "assets/chickpea.jpeg",
    "kidneybeans": "assets/kidneybeans.webp",
    "pigeonpeas":  "assets/pegionpeas.webp",
    "mothbeans":   "assets/Mothbeans.jpeg",
    "mungbean":    "assets/Mugbeans.jpeg",
    "blackgram":   "assets/Blackgram.jpeg",
    "lentil":      "assets/lentil.jpeg",
    "pomegranate": "assets/promegranate.jpeg",
    "banana":      "assets/banana .jpeg",
    "mango":       "assets/Mango.jpeg",
    "grapes":      "assets/Grapes.jpg",
    "watermelon":  "assets/Watermelon.webp",
    "muskmelon":   "assets/Muskmelon.webp",
    "apple":       "assets/Apple.jpg",
    "orange":      "assets/Orange.avif",
    "papaya":      "assets/papaya.jpeg",
    "coconut":     "assets/Coconut.jpeg",
    "cotton":      "assets/cotton.jpeg",
    "jute":        "assets/Jute.jpg",
    "coffee":      "assets/Coffee.jpg",
};

// ── CONFIDENCE LEVEL LABEL ──
function getConfidenceLevel(conf) {
    if (conf >= 70) return { label: "Strong Match",   color: "#1e8449" };
    if (conf >= 40) return { label: "Moderate Match", color: "#d68910" };
    return               { label: "Weak Match",      color: "#c0392b" };
}


// ── MAIN RENDER ──
window.onload = function () {

    const raw = localStorage.getItem("predictionResult");

    if (!raw) {
        document.querySelector(".result-card").innerHTML = `
            <h2>AgriAdvisor</h2>
            <p style="color:#e74c3c; margin-top:20px;">
                No prediction data found. Please go back and submit the form.
            </p>
            <button onclick="goBack()">Go Back</button>
        `;
        return;
    }

    const result = JSON.parse(raw);
    const crops  = result.top_crops;
    const advice = result.advice;
    const inputs = JSON.parse(localStorage.getItem("predictionInputs") || "{}");

    // ── Summary bar ──
    const topCrop  = crops[0];
    const topConf  = topCrop.confidence.toFixed(1);
    const topPrice = typeof topCrop.price === "number" ? `₹${topCrop.price}` : topCrop.price || "N/A";

    document.getElementById("result-summary").innerHTML = `
        <div class="summary-item">
            <div class="summary-value">${crops.length}</div>
            <div class="summary-label">Crops Found</div>
        </div>
        <div class="summary-item">
            <div class="summary-value">${topConf}%</div>
            <div class="summary-label">Top Confidence</div>
        </div>
        <div class="summary-item">
            <div class="summary-value">${topPrice}</div>
            <div class="summary-label">${topCrop.name} Price (30d)</div>
        </div>
    `;

    // ── Crop cards ──
    const resultBox = document.getElementById("result-box");
    resultBox.innerHTML = "";

    crops.forEach((crop, index) => {

        const rank      = ["🥇", "🥈", "🥉"][index] || "➤";
        const cropKey   = crop.name.toLowerCase();
        const emoji     = CROP_EMOJI[cropKey]  || "🌱";
        const imgUrl    = CROP_IMAGES[cropKey] || null;
        const price     = typeof crop.price === "number" ? `₹${crop.price}` : crop.price || "N/A";
        const conf      = crop.confidence.toFixed(2);
        const confLevel = getConfidenceLevel(crop.confidence);

        // Confidence bar color
        let barColor = "linear-gradient(90deg, #2ecc71, #1e8449)";
        if (crop.confidence < 40)      barColor = "linear-gradient(90deg, #e74c3c, #c0392b)";
        else if (crop.confidence < 70) barColor = "linear-gradient(90deg, #f39c12, #d68910)";

        // Image or emoji fallback
        const imageHTML = imgUrl
            ? `<img class="crop-img" src="${imgUrl}" alt="${crop.name}"
                    onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
               <div class="crop-img-placeholder" style="display:none;">${emoji}</div>`
            : `<div class="crop-img-placeholder">${emoji}</div>`;

        const card = document.createElement("div");
        card.className = "crop-card";
        card.innerHTML = `
            <div class="crop-top">
                ${imageHTML}
                <div class="crop-info">
                    <div class="crop-rank-name">
                        <span class="rank-badge">${rank}</span>${crop.name}
                    </div>
                    <div style="font-size:12px; color:#888; margin-top:3px;">
                        ${emoji} Predicted price (30 days):
                        <strong style="color:#1e8449;">${price}</strong>
                    </div>
                </div>
            </div>

            <div class="confidence-section">
                <div class="confidence-label">
                    <span>Confidence Score
                        <span style="font-size:11px; color:${confLevel.color}; margin-left:6px;">
                            ● ${confLevel.label}
                        </span>
                    </span>
                    <span>${conf}%</span>
                </div>
                <div class="confidence-bar-bg">
                    <div class="confidence-bar-fill"
                         id="bar-${index}"
                         style="background: ${barColor};">
                    </div>
                </div>
            </div>
        `;
        resultBox.appendChild(card);
    });

    // ── Animate confidence bars ──
    setTimeout(() => {
        crops.forEach((crop, index) => {
            const bar = document.getElementById(`bar-${index}`);
            if (bar) bar.style.width = `${Math.min(crop.confidence, 100)}%`;
        });
    }, 100);

    // ── Advice Section ──
    const tags = [];
    if (inputs.water_availability) tags.push(`💧 Water: ${inputs.water_availability}`);
    if (inputs.irrigation_type)    tags.push(`🚿 Irrigation: ${inputs.irrigation_type}`);
    if (inputs.market_type)        tags.push(`🏪 Market: ${inputs.market_type}`);
    if (inputs.rainfall)           tags.push(`🌧️ Rainfall: ${inputs.rainfall}mm`);

    const tagsHTML = tags.map(t =>
        `<span class="advice-tag">${t}</span>`
    ).join("");

    document.getElementById("advice-section").innerHTML = `
        <div class="advice-header">
            <span class="advice-icon">💡</span>
            <span class="advice-title">Farming Advisory</span>
        </div>
        <div class="advice-general">
            <p>${advice}</p>
        </div>
        ${tagsHTML ? `
        <div class="advice-tags">
            ${tagsHTML}
        </div>` : ""}
    `;
};


function goBack() {
    window.location.href = "predict.html";
}