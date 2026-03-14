# Java Rush Bot

Telegram-бот, созданный с использованием `aiogram 3`, `Python` и развернутый через Docker с поддержкой webhook. Бот предоставляет функции: диалог с ИИ, квизы, переводы, факты и другое.

---

## 🚀 Описание

Бот работает в двух режимах:
- **Polling** — стандартный режим опроса Telegram API.
- **Webhook** — используется при развёртывании на сервере (рекомендуется для продакшена).

Развертывание осуществляется через `docker-compose` с интеграцией Traefik для HTTPS и роутинга.

---

## 🔧 Требования

- Docker
- Docker Compose
- Доменное имя (для webhook)
- Traefik (уже настроен как внешняя сеть)

---

## 📦 Установка и запуск

1. Склонируйте репозиторий:
`bash git clone https://github.com/your-repo/java-rush-bot.git cd java-rush-bot`

2. Создайте `.env` файл:
   ```env
   BOT_TOKEN=ваш_токен_от_BotFather
   ADMIN_ID=ваш_telegram_id
   WEBHOOK_PORT=8000
   BOT_DOMAIN=bot.yourdomain.com
   AI_API_KEY=ваш_api_ключ
   AI_BASE_URL=https://api.deepseek.com
   AI_MODEL=deepseek-chat
   ```
3. Запустите бота:
   `bash docker-compose -f docker-compose.java_rush_bot.yml up --build`
4. Бот автоматически запустится в режиме **webhook**, если переменная `WEBHOOK=True`.

---

## 🌐 Архитектура

- **Traefik** — прокси-сервер, управляет HTTPS и роутингом.
- **Docker** — контейнеризация бота.
- **Webhook** — бот принимает обновления от Telegram через HTTPS.
- **aiogram 3** — асинхронная библиотека для Telegram Bot API.

---

## 🛠 Переменные окружения

| Переменная        | Описание |
|-------------------|--------|
| `BOT_TOKEN`       | Токен от @BotFather |
| `ADMIN_ID`        | ID администратора бота |
| `WEBHOOK_PORT`    | Порт, на котором слушает бот (например, 8000) |
| `BOT_DOMAIN`      | Домен, например `bot.example.com` |
| `AI_API_KEY`      | Ключ для доступа к ИИ (DeepSeek, OpenAI и т.п.) |
| `AI_BASE_URL`     | Базовый URL API ИИ |
| `AI_MODEL`        | Модель ИИ (например, `deepseek-chat`) |

---

## 🔄 Режимы работы

### Webhook (по умолчанию в compose)
- Включается автоматически через `WEBHOOK=True`.
- Бот регистрирует вебхук при старте.
- При остановке — вебхук удаляется.

### Polling
Чтобы использовать polling, измените `.env`:
`env WEBHOOK=False`
и запустите бота локально без Docker.

---

## 📎 Логи

Просмотр логов:
`bash docker logs -f java-rush-bot`