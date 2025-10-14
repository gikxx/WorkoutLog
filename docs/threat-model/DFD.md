# DFD - Workout Log Threat Model

## Контекстная диаграмма Workout Log API

```mermaid
flowchart TD
    %% Внешние участники
    USER[Пользователь]
    MOBILE[Мобильное приложение]

    %% Граница доверия: Клиент
    subgraph CLIENT[Trust Boundary: Клиент]
        USER --> MOBILE
    end

    %% Граница доверия: Edge
    subgraph EDGE[Trust Boundary: Edge - API Gateway]
        GW[API Gateway<br/>HTTPS]
    end

    %% Граница доверия: Core
    subgraph CORE[Trust Boundary: Core - Workout Log API]
        AUTH[Auth Service<br/>JWT]
        WORKOUTS[Workouts API<br/>/workouts]
        EXERCISES[Exercises API<br/>/exercises]
        STATS[Stats API<br/>/stats]
    end

    %% Граница доверия: Data
    subgraph DATA[Trust Boundary: Data]
        DB[(Database<br/>SQLite/Postgres)]
    end

    %% Потоки данных
    MOBILE -->|F1: HTTPS /auth/login| GW
    MOBILE -->|F2: HTTPS /workouts| GW
    MOBILE -->|F3: HTTPS /exercises| GW
    MOBILE -->|F4: HTTPS /stats| GW

    GW -->|F5: JWT Auth| AUTH
    GW -->|F6: API Calls| WORKOUTS
    GW -->|F7: API Calls| EXERCISES
    GW -->|F8: API Calls| STATS

    AUTH -->|F9: User Validation| WORKOUTS
    WORKOUTS -->|F10: CRUD Operations| DB
    EXERCISES -->|F11: CRUD Operations| DB
    STATS -->|F12: Read Operations| DB

    %% Стили для границ доверия
    style CLIENT stroke:#ff6b6b,stroke-width:3px
    style EDGE stroke:#4ecdc4,stroke-width:3px
    style CORE stroke:#45b7d1,stroke-width:3px
    style DATA stroke:#96ceb4,stroke-width:3px
```

## Описание потоков данных

| Flow ID | Описание | Канал/Протокол | Данные |
|---------|-----------|-----------------|--------|
| F1 | Аутентификация пользователя | HTTPS/JSON | email, password |
| F2 | Запросы тренировок | HTTPS/JSON | workout data, user_id |
| F3 | Запросы упражнений | HTTPS/JSON | exercise data, workout_id |
| F4 | Запросы статистики | HTTPS/JSON | user_id, date range |
| F5 | Валидация JWT токена | Internal | JWT token verification |
| F6 | API Calls тренировки | Internal/JSON | workout operations |
| F7 | API Calls упражнения | Internal/JSON | exercise operations |
| F8 | API Calls статистика | Internal/JSON | stats operations |
| F9 | Проверка прав доступа | Internal | user_id, resource_id |
| F10 | Операции с БД тренировки | SQL | workout CRUD |
| F11 | Операции с БД упражнения | SQL | exercise CRUD |
| F12 | Read Operations статистики | SQL | stats queries |
