function switchTab(tabName) {
  // Hide all tab contents
  const contents = document.querySelectorAll('.tab-content');
  contents.forEach(content => content.style.display = 'none');

  // Remove active class from all buttons
  const buttons = document.querySelectorAll('.nav-tab');
  buttons.forEach(btn => btn.classList.remove('active'));

  // Show selected tab content
  document.getElementById(tabName + '-section').style.display = 'block';

  // Add active class to selected button
  document.getElementById('tab-' + tabName).classList.add('active');
}

// Default to showing the converter
document.addEventListener('DOMContentLoaded', () => {
  switchTab('converter');
});

    const form = document.getElementById("uploadForm");
    const result = document.getElementById("result");
    const startDateInput = document.querySelector('input[name="start_date"]');
    const endDateInput = document.querySelector('input[name="end_date"]');

    // Set default Start Date to 1st of current month, End Date to last day of current month
    const now = new Date();
    const year = now.getFullYear();
    const month = now.getMonth(); // 0-indexed

    const firstDay = new Date(Date.UTC(year, month, 1));
    const lastDay = new Date(Date.UTC(year, month + 1, 0));

    startDateInput.value = firstDay.toISOString().split('T')[0];
    endDateInput.value = lastDay.toISOString().split('T')[0];

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      result.innerHTML = "⏳ Uploading and converting... please wait.";

      const formData = new FormData(form);

      try {
        const response = await fetch("/upload", {
          method: "POST",
          body: formData
        });

        if (!response.ok) {
          result.innerHTML = "❌ Upload failed.";
          return;
        }

        const html = await response.text();
        result.innerHTML = html; // server sends HTML snippet with download link
      } catch (err) {
        result.innerHTML = "⚠️ Error: " + err;
      }
    });