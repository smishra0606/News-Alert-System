// API Base URL - change this when deploying
const API_BASE_URL = window.location.origin;

// Subscribe Form Handler
document.getElementById('subscribeForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const emailInput = document.getElementById('email');
    const messageDiv = document.getElementById('message');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    const submitBtn = e.target.querySelector('button[type="submit"]');

    const email = emailInput.value.trim();

    // Show loader
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-block';
    submitBtn.disabled = true;
    messageDiv.style.display = 'none';

    try {
        const response = await fetch(`${API_BASE_URL}/api/subscribe`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email })
        });

        const data = await response.json();

        if (data.success) {
            // Redirect to success page
            window.location.href = '/success';
        } else {
            showMessage(messageDiv, data.message, 'error');
        }
    } catch (error) {
        showMessage(messageDiv, 'Network error. Please try again.', 'error');
    } finally {
        // Hide loader
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
        submitBtn.disabled = false;
    }
});

// Unsubscribe Form Handler
document.getElementById('unsubscribeForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const emailInput = document.getElementById('unsubEmail');
    const messageDiv = document.getElementById('unsubMessage');
    const submitBtn = e.target.querySelector('button[type="submit"]');

    const email = emailInput.value.trim();

    submitBtn.disabled = true;
    submitBtn.textContent = 'Processing...';
    messageDiv.style.display = 'none';

    try {
        const response = await fetch(`${API_BASE_URL}/api/unsubscribe`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email })
        });

        const data = await response.json();

        if (data.success) {
            showMessage(messageDiv, data.message, 'success');
            emailInput.value = '';
        } else {
            showMessage(messageDiv, data.message, 'error');
        }
    } catch (error) {
        showMessage(messageDiv, 'Network error. Please try again.', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Unsubscribe';
    }
});

// Helper function to show messages
function showMessage(element, message, type) {
    element.textContent = message;
    element.className = `message ${type}`;
    element.style.display = 'block';

    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            element.style.display = 'none';
        }, 5000);
    }
}

// Email validation
function validateEmail(email) {
    const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return re.test(email);
}
