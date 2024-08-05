��� ������� ������� ��� ���������� ��������� ��������� ����:

������������ �����������:

git clone https://github.com/Nudlik/mailer_service.git
������� � ������� �������:
������� ����������� ���������:

python -m venv venv
������������ ����������� ���������:

��� Windows:
.\venv\Scripts\activate
��� Linux/macOS:

source venv/bin/activate
���������� �����������:

pip install -r requirements.txt
������� ���� �������� .env:

����������� ������ �����:

cp .env.example .env
������� .env ���� � ��������� ���� ���������.
��������� ��������:

python manage.py migrate
��������� � ��������� Redis (���� ���������):

� .env ����� ����������:

CACHES_ENABLED=True
��� Linux � WSL:

sudo service redis-server start
��������� ������ ����������:

python manage.py runserver
������ ���������� ������������� ��������:

python manage.py runapscheduler
������ ������� �������� �� ������� (�������� ������):


python manage.py start_send_mail
��� ���� ������� ��� ��������� � ��������� ������ �� ����� ��������� ����������.


