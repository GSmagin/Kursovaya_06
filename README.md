Для запуска проекта вам необходимо выполнить следующие шаги:

Склонировать репозиторий:

git clone https://github.com/Nudlik/mailer_service.git
Перейти в каталог проекта:
Создать виртуальное окружение:

python -m venv venv
Активировать виртуальное окружение:

Для Windows:
.\venv\Scripts\activate
Для Linux/macOS:

source venv/bin/activate
Установить зависимости:

pip install -r requirements.txt
Создать файл настроек .env:

Скопировать пример файла:

cp .env.example .env
Открыть .env файл и прописать ваши настройки.
Применить миграции:

python manage.py migrate
Настроить и запустить Redis (если требуется):

В .env файле установить:

CACHES_ENABLED=True
Для Linux с WSL:

sudo service redis-server start
Запустить сервер разработки:

python manage.py runserver
Запуск ежедневной периодической рассылки:

python manage.py runapscheduler
Запуск скрипта рассылки из консоли (тестовый запуск):


python manage.py start_send_mail
Эти шаги помогут вам настроить и запустить проект на вашем локальном компьютере.


