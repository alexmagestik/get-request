# CLI-приложение для работы с API

Простое CLI-приложение на Python с меню для работы с HTTP-запросами и API.

## Функциональность

1. **GET по URL** - Выполнение произвольного GET-запроса с возможностью указания параметров
2. **Страна** - Получение информации о стране через API [restcountries.com](https://restcountries.com/)
3. **Случайная собака** - Получение случайного изображения собаки через API [dog.ceo](https://dog.ceo/dog-api/)
4. **Выход** - Выход из программы

## Установка

### Создание виртуального окружения

```bash
python -m venv .venv
```

### Активация виртуального окружения

**macOS/Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

### Установка зависимостей

```bash
pip install -r requirements.txt
```

## Конфигурация

Для работы с API restcountries.com необходим API-ключ. Он хранится в файле `.env`:

```env
RC_API_KEY=your_api_key_here
```

## Запуск

```bash
python main.py
```

## Структура проекта

- `main.py` - Основной файл с CLI-интерфейсом
- `http_client.py` - Модуль с HTTP-функциями (get, базовая проверка статуса)
- `country_info.py` - Модуль для работы с API стран
- `requirements.txt` - Зависимости проекта
- `.env` - Переменные окружения
- `.venv/` - Виртуальное окружение
- `README.md` - Документация
