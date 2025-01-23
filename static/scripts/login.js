document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('login-form');
    const responseBanner = document.getElementById('response-banner');

    form.addEventListener('submit', async function(event) {
        event.preventDefault(); // Previene l'invio predefinito del modulo

        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();

        if (!username || !password) {
            responseBanner.style.display = 'block';
            responseBanner.style.color = 'red';
            responseBanner.textContent = 'Tutti i campi sono obbligatori.';
            return;
        }

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ username, password })
            });

            const result = await response.json();

            responseBanner.style.display = 'block';

            if (response.status === 200 && result.success) {
                responseBanner.style.color = 'green';
                responseBanner.textContent = result.message;

                // Redirect a /analisi dopo 3 secondi
                setTimeout(() => {
                    window.location.href = "/analisi";
                }, 3000);
            } else if (response.status === 401) {
                responseBanner.style.color = 'red';
                responseBanner.textContent = result.message;
            } else {
                responseBanner.style.color = 'red';
                responseBanner.textContent = result.message || 'Errore durante il login. Riprova.';
            }
        } catch (error) {
            console.error('Errore:', error);
            responseBanner.style.display = 'block';
            responseBanner.style.color = 'red';
            responseBanner.textContent = 'Errore durante il login. Riprova.';
        }
    });
});