## Установка

1. Клонировать репозиторий:

   ```bash
   git clone https://github.com/epifanovamur-cyber/telegram-shop-bot.git
   ```

1. Перейти в папку проекта:

   ```bash
   cd telegram-shop-bot
   ```

1. Создать виртуальное окружение:

   ```bash
   python -m venv .venv
   ```

1. Активировать виртуальное окружение:

   ```bash
   .venv\Scripts\activate
   ```

1. Установить зависимости:

   ```bash
   pip install -r requirements.txt
   ```

1. Создать файл `.env` по примеру `.env.example`:

   ```env
   BOT_TOKEN=your_bot_token_here
   ADMIN_ID=your_telegram_id_here
   ```

1. Запустить бота:

   ```bash
   python bot.py
   ```