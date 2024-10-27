# 🎶 Witaj w swojej nowej, imponującej aplikacji muzycznej!

Ten projekt został stworzony przy użyciu Django REST API, umożliwiając dostęp do personalizowanych rekomendacji muzycznych dzięki zaawansowanym algorytmom uczenia maszynowego.

### Uruchomienie aplikacji lokalnie

Aby uruchomić aplikację lokalnie, wykonaj poniższe kroki:

1. **Zainstaluj zależności**:
   pip install -r requirements.txt

2. **Wykonaj migracje bazy danych**:
   python manage.py migrate

3. **Uruchom serwer deweloperski**:
   python manage.py runserver

   Aplikacja będzie dostępna pod adresem `http://localhost:8000`.

### Endpointy API

Aplikacja udostępnia poniższe endpointy REST API:

- **GET /api/music/recommendations** - pobiera rekomendacje muzyczne dla zalogowanego użytkownika
- **POST /api/music/track** - dodaje nowy utwór do bazy danych
- **GET /api/music/track/{id}** - pobiera szczegóły konkretnego utworu
- **DELETE /api/music/track/{id}** - usuwa utwór z bazy danych

Szczegółowa dokumentacja API znajduje się pod `/api/docs`.

### Testowanie

Aby uruchomić testy jednostkowe, użyj poniższego polecenia:

   python manage.py test

---

Dzięki za skorzystanie z naszej aplikacji muzycznej! 🎧
