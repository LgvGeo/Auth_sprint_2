# Запуска проекта  
Создаем .env файл в корневой директории с содержимым  
REDIS_HOST=redis  
REDIS_PORT=6379  

POSTGRES_PASSWORD=postgres  
POSTGRES_USER=postgres  
POSTGRES_DB=postgres  
POSTGRES_HOST=db  
POSTGRES_PORT=5432  

DB_NAME=postgres  
DB_HOST=db  
DB_USER=postgres  
DB_PASSWORD=postgres  
DB_PORT=5432  

DEBUG=True  
SECRET_KEY=ll  
UWSGI_PROCESSES=1  
UWSGI_THREADS=16  
UWSGI_HARAKIRI=240  

ACCESS_TOKEN_TTL=300  
REFRESH_TOKEN_TTL=1000  

ELASTIC_HOST=elastic  
ELASTIC_PORT=9200  

REQUEST_RATE_LIMIT=15  
YANDEX_CLIENT_ID=ef3fe64262ac40a29beef2431669a261  
YANDEX_CLIENT_SECRET=dd4fb71e89ff4f4ea19752fe6666e01c  
YANDEX_TOKEN_URL=https://oauth.yandex.ru/token  
YANDEX_USER_INFO_URL=https://login.yandex.ru/info  

После этого docker compose up --build  

Когда все запустилось накатываем миграции в alembic и django  
bash migrate.sh


В микросервисах request rate limit контролируется с помощью redis  
В django добавлена кастомная модель User, авторизация реализована через микросервис авторизации.
Добавлена возможность авторизации через Yandex Id. Предварительно ожидается что пользователь зарегестрирован на нашем ресурсе.  
В микросервисы добалена трассировка, используется jaeger





# Проектная работа 7 спринта

1. Создайте интеграцию Auth-сервиса с сервисом выдачи контента и панелью администратора Django, используя контракт, который вы сделали в прошлом задании.
  
    При создании интеграции не забудьте учесть изящную деградацию Auth-сервиса. Как вы уже выяснили ранее, Auth сервис один из самых нагруженных, потому что в него ходят большинство сервисов сайта. И если он откажет, сайт отказать не должен. Обязательно учтите этот сценарий в интеграциях с Auth-сервисом.
2. Добавьте в Auth трасировку и подключите к Jaeger. Для этого вам нужно добавить работу с заголовком x-request-id и отправку трасировок в Jaeger.
3. Добавьте в сервис механизм ограничения количества запросов к серверу.
4. Упростите регистрацию и аутентификацию пользователей в Auth-сервисе, добавив вход через социальные сервисы. Список сервисов выбирайте исходя из целевой аудитории онлайн-кинотеатра — подумайте, какими социальными сервисами они пользуются. Например, использовать [OAuth от Github](https://docs.github.com/en/free-pro-team@latest/developers/apps/authorizing-oauth-apps){target="_blank"} — не самая удачная идея. Ваши пользователи не разработчики и вряд ли имеют аккаунт на Github. А вот добавить VK, Google, Yandex или Mail будет хорошей идеей.

    Вам не нужно делать фронтенд в этой задаче и реализовывать собственный сервер OAuth. Нужно реализовать протокол со стороны потребителя.
    
    Информация по OAuth у разных поставщиков данных: 
    
    - [Yandex](https://yandex.ru/dev/oauth/?turbo=true){target="_blank"},
    - [VK](https://vk.com/dev/access_token){target="_blank"},
    - [Google](https://developers.google.com/identity/protocols/oauth2){target="_blank"},
    - [Mail](https://api.mail.ru/docs/guides/oauth/){target="_blank"}.
    
## Дополнительное задание
    
Реализуйте возможность открепить аккаунт в соцсети от личного кабинета. 
    
Решение залейте в репозиторий текущего спринта и отправьте на ревью.
