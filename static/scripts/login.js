document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('login-form');
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Impedisce il caricamento della pagina

        var formData = new FormData(form);
        var xhr = new XMLHttpRequest();
        xhr.open('POST', form.action, true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        xhr.onload = function() {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.success) {
                    window.location.href = '/index';
                } else {
                    document.getElementById('error-banner').style.display = 'block';
                }
            } else {
                document.getElementById('error-banner').style.display = 'block';
            }
        };

        xhr.send(formData);
    });
});