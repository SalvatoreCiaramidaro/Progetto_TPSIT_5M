document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('login-form');
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Impedisce il caricamento della pagina

        /** Crea un oggetto FormData contenente i dati del modulo specificato */
        var formData = new FormData(form);
        var xhr = new XMLHttpRequest();
        xhr.open('POST', form.action, true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        

        // Gestisce la risposta della richiesta AJAX e aggiorna il banner di risposta in base al risultato.
        xhr.onload = function() {
            var responseBanner = document.getElementById('response-banner');
            if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.success) {
                responseBanner.style.display = 'block';
                responseBanner.style.color = 'green';
                responseBanner.textContent = response.message;
            } else {
                responseBanner.style.display = 'block';
                responseBanner.style.color = 'red';
                responseBanner.textContent = response.message;
            }
            } else {
            responseBanner.style.display = 'block';
            responseBanner.style.color = 'red';
            responseBanner.textContent = 'Errore durante la registrazione. Riprova.';
            }
        };

        xhr.send(formData);
    });
});