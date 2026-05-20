function() {
            {% if user.is_authenticated %}
                // Пользователь вошел: сохраняем данные
                localStorage.setItem('userId', '{{ user.id }}');
                localStorage.setItem('username', '{{ user.username }}');
                console.log('LocalStorage sync: User {{ user.username }} (ID: {{ user.id }}) is logged in.');
            {% else %}
                // Пользователь вышел: очищаем данные
                localStorage.removeItem('userId');
                localStorage.removeItem('username');
                console.log('LocalStorage sync: No user logged in. Storage cleared.');
            {% endif %}

            // Обработка клика по кнопке выхода для немедленной очистки
            const logoutLink = document.querySelector('a[href="{% url 'logout' %}"]');
            if (logoutLink) {
                logoutLink.addEventListener('click', function() {
                    localStorage.removeItem('userId');
                    localStorage.removeItem('username');
                });
            }
        })();