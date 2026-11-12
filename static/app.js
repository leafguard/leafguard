// LeafGuard skeleton frontend
const fileInput = document.getElementById("leafInput");
const scanBtn = document.getElementById("scanBtn");
const output = document.getElementById("output");
const statusMsg = document.getElementById("statusMsg");

scanBtn.addEventListener("click", async () => {
  const file = fileInput.files[0];
  if (!file) {
    statusMsg.textContent = "Please select or capture a photo first.";
    return;
  }

  scanBtn.disabled = true;
  statusMsg.textContent = "Uploading and scanning...";
  output.textContent = "Processing...";

  const formData = new FormData();
  formData.append("file", file);
  formData.append("lang", "en");

  try {
    const res = await fetch("/predict", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    if (!res.ok) {
      statusMsg.textContent = `Error: ${data.detail || "Upload failed"}`;
      output.textContent = JSON.stringify(data, null, 2);
    } else {
      statusMsg.textContent = `Status: ${data.status}`;
      output.textContent = JSON.stringify(data, null, 2);
    }
  } catch (err) {
    statusMsg.textContent = `Network error: ${err.message}`;
    output.textContent = "";
  } finally {
    scanBtn.disabled = false;
  }
});

