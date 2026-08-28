# Участие в разработке

## Рабочий процесс

1. Создайте ветку от актуального `main`.
2. Делайте небольшие тематические commits.
3. Добавьте или обновите тесты для изменённого поведения.
4. Не добавляйте реальные персональные данные, секреты и production-дампы.
5. Откройте pull request с описанием изменения и способом проверки.

## Подготовка окружения

```bash
python3.12 -m venv venv
source venv/bin/activate
python -m pip install --require-hashes -r requirements-dev.txt
```

## Проверка перед pull request

```bash
ruff check .
ruff format --check .
python manage.py check
python manage.py test
pip-audit --no-deps --disable-pip -r requirements.txt
```

Если меняются модели, создайте миграции командой `python manage.py makemigrations`
и включите их в pull request. Изменения публичного чат-ассистента не должны
расширять его доступ до операций записи в БД без отдельного security review.

Прямые зависимости редактируются в `requirements.in` и `requirements-dev.in`.
После этого оба lock-файла пересобираются через `uv pip compile` с флагом
`--generate-hashes`; вручную редактировать сгенерированные lock-файлы не нужно.
