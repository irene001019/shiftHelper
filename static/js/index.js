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
