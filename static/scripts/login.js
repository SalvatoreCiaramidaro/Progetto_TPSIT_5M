document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('login-form');
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Impedisce il caricamento della pagina
        
        /** Crea un oggetto FormData contenente i dati del modulo specificato */
        var formData = new FormData(form);
        var xhr = new XMLHttpRequest();
        xhr.open('POST', form.action, true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        xhr.onload = function() {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.success) {
                    window.location.href = '/analisi'; // Reindirizza alla pagina delle analisi
                } else {
                    document.getElementById('error-banner').style.display = 'block'; // Mostra il banner di errore
                }
            } else {
                document.getElementById('error-banner').style.display = 'block'; // Mostra il banner di errore
            }
        };

        xhr.send(formData);
    });
});