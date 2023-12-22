# Ела Java Python'a
### Setup
1. Рекомендуется создать локальное окружение, затем:
```bash
python -m pip install -r requirements.txt
```
2. Необходимо создать config.py на основе config-example.py
   - **Не добавляйте config.py в репозиторий, т к он содержит уникальный токен**
### Run
```bash
cd app
python -m uvicorn main:app --reload 
```
### Contents
```
├── app
│   ├── api
│   │   ├── routes
│   │   │   ├── router.py - Все эндпоинты и их руты
│   │   │   └── ships.py - Пример эндпоинтов
│   │   └── dependencies.py - Настройка fastapi магии с зависимостями
│   ├── core - Основная логика
│   ├── crud - Create Read Update Delete функции
│   ├── models - Модели сущностей
│   ├── schemas - Схемы объектов для обмена данными
│   ├── utils - Вспомогательные функции
│   ├── config-example.py - Пример конфига
│   ├── database.py - Настройка коннекта к БД
│   └── main.py - Точка входа
├── tests - Автотесты
│   ├── test_api - Тестирование эндпоинтов
│   └── conftest.py - Настройка автотестов, фикстуры
├── .gitignore - Список игнорируемых файлов в git
├── pytest.ini - Конфиг для автотестов
├── requirements.txt - Cписок используемых библиотек
└── test_main.http - Тесты эндпоинтов
```



