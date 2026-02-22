document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("txnForm");
    const resultSection = document.getElementById("resultSection");
    const resultLabel = document.getElementById("predictionLabel");
    const resultScore = document.getElementById("predictionScore");
    const resultReason = document.getElementById("predictionReason");
    const analyzeBtn = document.getElementById("analyzeBtn");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        analyzeBtn.disabled = true;
        analyzeBtn.textContent = "Analyzing...";

        const data = Object.fromEntries(new FormData(form).entries());

        try {
            const res = await fetch("/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            const result = await res.json();

            if (result.error) {
                alert(result.error);
                return;
            }

            resultSection.classList.remove("hidden");
            resultLabel.textContent = result.label;
            resultScore.textContent = (result.score * 100).toFixed(2) + "%";
            resultReason.textContent = result.reason;

        } catch (err) {
            alert("Error: " + err.message);
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = "Analyze Transaction";
        }
    });
});

// after showing result in your existing handler
// create Save button (only if user logged in)
function showSaveButton(payload){
  const saveBtnId = "saveHistoryBtn";
  let saveBtn = document.getElementById(saveBtnId);
  if (!saveBtn) {
    saveBtn = document.createElement('button');
    saveBtn.id = saveBtnId;
    saveBtn.type = 'button';
    saveBtn.textContent = 'Save to History';
    saveBtn.className = 'save-btn';
    document.querySelector('.form-section').appendChild(saveBtn);

    saveBtn.addEventListener('click', async () => {
      try {
        const res = await fetch("/save", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.success) {
          alert("Saved to history.");
        } else {
          alert("Please login to save or error occurred.");
          // optional: redirect to login if 401
          if (res.status === 401) window.location.href = "/login";
        }
      } catch (err){
        alert("Save failed: " + err.message);
      }
    });
  }
}

const payloadToSave = {
  description: data.description,
  amount: data.amount,
  sender_country: data.sender_country,
  receiver_country: data.receiver_country,
  payment_method: data.payment_method,
  merchant_category: data.merchant_category,
  label: result.label,
  score: result.score,
  reason: result.reason
};
showSaveButton(payloadToSave);
