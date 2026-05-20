document.querySelectorAll('.status-select').forEach(function(select) {
    select.addEventListener('change', function() {
        var adId = this.dataset.adId;
        var newStatus = this.value;
        var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch('/change-status/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ad_id: adId, status: newStatus})
        })
        .then(function(response) { return response.json(); })
        .then(function(data) {
            if (!data.success) {
                alert('Ошибка: ' + (data.error || 'Неизвестно'));
            }
        });
    });
});