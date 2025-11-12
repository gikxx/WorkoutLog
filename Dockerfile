FROM python:3.11-slim-bookworm AS build

WORKDIR /app

# Копируем production зависимости
COPY requirements.txt ./

# Устанавливаем зависимости в wheels
RUN --mount=type=cache,target=/root/.cache \
    pip install --upgrade pip && \
    pip wheel --wheel-dir=/wheels --no-cache-dir -r requirements.txt

# Финальный образ
FROM python:3.11-slim-bookworm AS runtime

# Переменные окружения для безопасности
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPYCACHEPREFIX=/tmp \
    PATH="/home/appuser/.local/bin:${PATH}"

WORKDIR /app

# Создаем non-root пользователя с фиксированным UID (лучше для ★★2)
RUN groupadd -r -g 1001 appuser && \
    useradd -r -u 1001 -g appuser -d /app -s /bin/bash appuser

# Устанавливаем curl ДО смены пользователя
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Устанавливаем runtime зависимости
COPY --from=build --chown=appuser:appuser /wheels /wheels
RUN --mount=type=cache,target=/root/.cache \
    pip install --no-cache-dir --no-index --find-links=/wheels /wheels/* && \
    rm -rf /wheels

# Копируем код приложения после установки зависимостей
COPY --chown=appuser:appuser . .

# Hardening: настраиваем права
RUN chmod -R go-w /app && \
    find /app -type d -exec chmod 755 {} \; && \
    find /app -type f -exec chmod 644 {} \; && \
    find /app -name "*.pyc" -delete && \
    find /app -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

USER appuser

# Healthcheck для FastAPI (теперь curl доступен)
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
