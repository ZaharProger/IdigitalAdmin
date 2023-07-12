# IdigitalAdmin
Админ-панель для сайта форума Idigital38

### Кратко о том, что я уже сделал
Я более менее настроил проект под дальнейшую работу + настроил подключение к MYSQL на хостинге
### Как запустить (с учетом, что используется винда)
Для запуска нужно проделать следующее:
1. Клонировать репозиторий
2. Создать виртуальное окружение с помощью **python -m venv venv**
3. Активировать виртуальное окружение с помощью **.\venv\Scripts\activate**
4. Установить все пакеты из requirements.txt с помощью **pip install -r \.requirements.txt**
5. Запустить dev-сервер с помощью **python .\idigital38\manage.py runserver_plus --cert-file cert.pem --key-file key.pem**

Если все сделано правильно, то по адресу 127.0.0.1:8000 появится веб-страница с летящей вверх ракетой :)


### Дополнительно
Для установки сертификата нужно проделать следующие шаги:
1. Установить mkcert (если у вас винда можно поставить через choco install mkcert, при этом choco нужно предварительно установить через PowerShell, ну это уже расписано в гугле на оф сайте) 
2. После установки mkcert в терминале написать **mkcert -install**
3. Затем после установки сертификата перейти в корень django проекта и написать **mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1**

На этом все. Можно запускать сервер командой из пункта 5 раздела выше, однако все сработает при условии, что установлены все зависимости из requirements.txt
Если что-то не получилось по SSL, можно проделать все напрямую по шагам на сайте https://timonweb.com/django/https-django-development-server-ssl-certificate/