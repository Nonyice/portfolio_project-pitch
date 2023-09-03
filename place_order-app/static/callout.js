// Get the callout element
const callout = document.getElementById('callout');

// Function to toggle visibility of the callout
function toggleCallout() {
  callout.style.display = callout.style.display === 'none' ? 'block' : 'none';
}

// Function to redirect the user to the order page or program
function redirectToOrderPage() {
  window.location.href = 'your-order-page-url'; // Replace 'your-order-page-url' with the actual URL of your order page or program
}

// Add a click event listener to the callout element
callout.addEventListener('click', redirectToOrderPage);

// Flash the callout every 1 second
setInterval(toggleCallout, 1000);
