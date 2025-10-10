# TG Post Generator (OpenAI → Koyeb → Zapier → Telegram)

Сервис генерирует развёрнутые посты по теме через OpenAI API и отдаёт JSON по HTTP.
План: загрузка в GitHub → деплой на Koyeb → триггер из Zapier → отправка в Telegram.

## Локальный запуск
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...                         # Windows: set OPENAI_API_KEY=sk-...
uvicorn app:app --reload
# Открой http://127.0.0.1:8000/health и /generate
```

## Переменные окружения
- `OPENAI_API_KEY` — ключ OpenAI
- `OPENAI_MODEL` — модель (по умолчанию gpt-4o-mini)
- `TOPICS` — темы через `|`, используются, если не передан `?topic=`

## HTTP-эндпоинты
- `GET /health` → `{"ok": true}`
- `GET /generate?topic=<строка>&max_tokens=1600` → JSON с полями `title`, `meta_description`, `post_content`, `topic`

## Деплой на Koyeb (кратко)
1. Подключи GitHub-репозиторий.
2. В variables добавь `OPENAI_API_KEY`, (опц.) `OPENAI_MODEL`, `TOPICS`.
3. После деплоя проверь `/health` и `/generate`.

## Использование с Zapier
- Trigger: Schedule (по расписанию) → Webhooks GET к `/generate` → Telegram: Send Message (берём `post_content`).
