#!/bin/bash

sudo chown vscode .venv

# Команды которые запустятся после первого запуска devcontainer.

uv run dprint output-resolved-config > /dev/null
uv run lefthook install

uv run python manage.py migrate
uv run python manage.py shell -c "from django.contrib.auth import get_user_model as g; u,_=g().objects.get_or_create(username='admin'); u.set_password('admin'); u.is_superuser=u.is_staff=True; u.save()"
