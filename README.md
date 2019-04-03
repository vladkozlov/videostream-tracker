# Сервис отслеживания просмотра видео, реализующий REST API



### Ресурс для отправки уведомления о просмотре видео.
```
Запрос

POST /watching

BODY: 
{
    video_id: '<video identificator>', 
    customer_id: '<customer identificator>'
}
```
```
Ответ

Empty response
```
### Ресурс просмотра числа видеопотоков, просматриваемых пользователем на текущий момент.
```
Запрос
GET /customer/{customer_id}
```
```
Ответ
{
    watching: <number of streams>
}

Особенность: если пользователь customer_id не существует, сервер вернет:
{
    watching: 0
}
```
### Ресурс просмотра числа пользователей, просматривающих видеопоток на текущий момент.
```
Запрос
GET /video/{video_id}
```
```
Ответ
{
    watching: <number of customers>
}

Особенность: если видеопоток video_id не существует, сервер вернет
{
    watching: 0
}
```

## Зависимости
1. Python 3.7
2. docker
3. docker-compose

## Установка и запуск

1. Запустить редис через докер `docker-compose -f docker-compose.yml up -d redis`
2. Установить зависимости `pip install -r requirements.txt`
3. Запустить сервер `python main.py`
