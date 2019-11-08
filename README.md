# Тестовое задание для Smena
Генерация чеков

Для проверки работоспособности запросов использовался ***Postman***
## Требования для запуска проекта
* Python 3.6
* docker-compose
## Установка зависимостей: 
```
pip install -r smena/requirements.txt
```

## Запуск проекта
Запустить инфраструктурные сервисы:
```
docker-compose up -d
```

Создать таблицы базы данных:
```
python smena/manage.py migrate
```

Загрузить fixtures для принтеров:
```
python smena/manage.py loaddata printers.json
```

Запустить в отдельном терминале воркер django_rq:
```
python smena/manage.py rqworker default
```

Запустить проект:
```
python smena/manage.py runserver
```
