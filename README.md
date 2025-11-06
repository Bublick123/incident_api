# Incident API

Микросервис для учёта инцидентов от операторов и систем мониторинга.

---

## 🚀 Запуск с Docker Compose (рекомендуется)

1. Соберите и запустите контейнеры:
   ```bash
   docker-compose up --build
   ```

   Сервис будет доступен по адресу: [http://localhost:8000](http://localhost:8000)

---

## ⚙️ Запуск без Docker

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Запустите сервер:
   ```bash
   uvicorn app.main:app --reload
   ```

---

## 📘 Документация API

После запуска откройте:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🔗 Эндпоинты

### Создать инцидент  
**POST** `/incidents/`
```json
{
  "description": "Самокат не в сети",
  "source": "operator"
}
```

### Получить список инцидентов  
**GET** `/incidents/`

Фильтр по статусу:
```
GET /incidents/?status=new
```

### Получить инцидент по ID  
**GET** `/incidents/{id}`

### Обновить статус инцидента  
**PATCH** `/incidents/{id}`
```json
{
  "status": "in_progress"
}
```

---

## 📄 Статусы инцидентов

| Статус       | Описание     |
|---------------|--------------|
| `new`         | Новый        |
| `in_progress` | В работе     |
| `resolved`    | Решён        |
| `closed`      | Закрыт       |

---

## 🏷 Источники инцидентов

| Источник      | Описание              |
|----------------|-----------------------|
| `operator`     | Оператор              |
| `monitoring`   | Система мониторинга   |
| `partner`      | Партнёр               |

---

## 🐳 Команды Docker

| Действие | Команда |
|-----------|----------|
| Остановка сервиса | `docker-compose down` |
| Просмотр логов | `docker-compose logs -f` |
| Пересборка без кэша | `docker-compose build --no-cache` |

---

## ⚙️ Дополнительная конфигурация (опционально)

Если хотите использовать **PostgreSQL** вместо **SQLite**, раскомментируйте соответствующие секции в `docker-compose.yml` и обновите `database.py`.

### Пример `docker-compose.yml` с PostgreSQL
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/incidents
    depends_on:
      - postgres
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: incidents
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

---

## 🧩 Использование

### Запуск проекта:
```bash
# Клонируйте проект (если нужно)
git clone <your-repo>
cd incident_api

# Запустите с Docker Compose
docker-compose up --build

# Или в фоновом режиме
docker-compose up -d --build
```

### Проверка работы:
```bash
# Проверить, что контейнеры запущены
docker-compose ps

# Посмотреть логи
docker-compose logs -f api

# Остановить сервис
docker-compose down
```

---

📦 **Готово!** После запуска откройте [http://localhost:8000/docs](http://localhost:8000/docs), чтобы протестировать API.
