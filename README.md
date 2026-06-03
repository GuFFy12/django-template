# Django Template

Keywords: django, python, devcontainer, uv, vscode, ruff, dprint, docker, github, github ci, lefthook (precommit), pytest, renovate.

Шаблон предназначен для django проектов в IDE vscode.

## Django рекомендации

1. Есть возможность поставить S3 - используйте. Потом nginx. В базе раздает granian, что немного неправильно.

2. django q2 как вариант очередей и плановых задач. Аналоги: celery, dramatiq + apscheduler, huey. Django 6 tasks framework пока сырой.

3. django-ninja для API, django-simple-history для аудита, django-import-export для импорта/экспорта в формате XLSX, django-private-storage для защищенных медиафайлов, sentry-sdk для интеграции с Sentry, django-auto_instrumentation для OTEL, django-imagekit для картинок в нужном формате, django-compressor + scss для поддержки scss. Я использовал все эти пакеты в разных проектах, но в шаблоне не стал их добавлять, чтобы не навязывать.

4. Вырублена вся типизация mypy ибо очень много ложных срабатываний. Pylance только для IDE ошибок на типы, и там тоже есть ложные срабатывания, но они не влияют на pre commit и CI. Вместо этого надежда на встроенные проверки django.

5. Требуются настройки в compose, settings.py. После granian должен стоять reverse proxy с ЗАГОЛОВКАМИ БЕЗОПАСНОСТИ!

## Установка

1. Установите copier: https://copier.readthedocs.io/en/v5.0.0/

Да вы можете просто сделать git clone и не использовать copier. Он нужен только для синхронизации с шаблоном, что удобно лично для меня.

2. Сделайте копию на основе шаблона:

```bash
copier copy https://github.com/GuFFy12/django-template.git <project-name>
```

3. Через поиск замените все упоминания django-template (и возможно django_template) на имя вашего проекта.

4. Откройте проект в vscode и в терминале инициализируйте git:

```bash
git init
git checkout -b main
git add .
git commit -m "Initial commit"
# Тут команды для push в remote, допустим в github
```

5. Установите docker: https://www.docker.com/products/docker-desktop/. Установите рекомендуемое расширение: devcontainers.

6. Откройте проект в devcontainer: command palette (ctrl shift p) -> reopen in devcontainer.

7. Начинайте разработку. Можете менять уже существующие настройки, но я постарался сделать их максимально стандартными и рабочими для всех.

Если вы изменили настройки devcontainer не забудьте запустить rebuild devcontainer.

## Базовый функционал разработки

Рекомендую просто открыть файлы и почитать комменты.

0. Для запуска проекта нужно установить docker и поднять pg и valkey: command palette -> run task: Start development environment; Create database.

1. .vscode имеет множество настроек: run tasks в command palette (ctrl shift p), debug (f5).

2. lefthook можете расценивать как асинхронный pre-commit. Там много проверок, но можете смело отключать.

3. ruff должен быть вам знаком так же как и uv (если нет почитайте). dprint же это rust аналог prettier для множества файлов.

4. pylance для анализа в ide.

5. Изменили настройки линтера или форматера? Обязательно запустите: run task -> Run pre-commit for all files.

6. Для dprint есть и другие плагины: поддержка js, ts, html. Обновите его если это необходимо.

## CI

1. Проверьте .github. Там есть workflows для докера. При build используется docker, прочитайте dockerfile.

2. Для обновлений зависимостей используйте renovate. Я рекомендую поставить его как github app (mend io). Но можно и как ci.

3. Я не стал включать сканы на secrets, уязвимости.

4. Запуск build on new git tags.
