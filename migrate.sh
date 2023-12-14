sudo docker compose exec auth_api alembic upgrade head \
&& sudo docker compose exec admin_panel python manage.py migrate users --fake \
&& sudo docker compose exec admin_panel python manage.py  migrate movies --fake \
&& sudo docker compose exec admin_panel python manage.py migrate sessions \
&& sudo docker compose exec admin_panel python manage.py migrate admin \
&& sudo docker compose exec admin_panel python manage.py migrate contenttypes \
&& sudo docker compose exec admin_panel python manage.py migrate auth \