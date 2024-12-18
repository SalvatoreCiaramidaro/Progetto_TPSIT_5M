document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('login-form');
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Impedisce il caricamento della pagina

        var formData = new FormData(form);
        var xhr = new XMLHttpRequest();
        xhr.open('POST', form.action, true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        xhr.onload = function() {
            var responseBanner = document.getElementById('response-banner');
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.success) {
                    responseBanner.style.display = 'block'; // Mostra il banner di risposta
                    responseBanner.style.color = 'green'; // Colore verde per il messaggio di successo
                    responseBanner.textContent = response.message; // Mostra il messaggio di successo
                } else {
                    responseBanner.style.display = 'block'; // Mostra il banner di risposta
                    responseBanner.style.color = 'red'; // Colore rosso per il messaggio di errore
                    responseBanner.textContent = response.message; // Mostra il messaggio di errore
                }
            } else {
                responseBanner.style.display = 'block'; // Mostra il banner di risposta
                responseBanner.style.color = 'red'; // Colore rosso per il messaggio di errore
                responseBanner.textContent = 'Errore durante la registrazione. Riprova.'; // Mostra un messaggio di errore generico
            }
        };

        xhr.send(formData);
    });
});