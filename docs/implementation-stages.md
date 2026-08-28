# Состояние реализации

Документ фиксирует не первоначальный план, а текущее состояние проекта.

## Реализовано

### Сайт и CMS

- публичные страницы, адаптивный интерфейс и карта;
- новости, услуги и цены, врачи, отзывы, контакты и обращения;
- управление контентом через Django Admin;
- SQLite для простого локального запуска.

### Контейнеризация

- Django/Gunicorn, PostgreSQL 15 и Nginx в Docker Compose;
- отдельная production-конфигурация;
- persistent volumes для БД, static и media;
- health/readiness endpoints.

### CI/CD и безопасность

- lint и форматирование Ruff;
- Django checks, миграции и автоматические тесты;
- lock-файлы с хешами и `pip-audit`;
- CodeQL и Dependabot;
- deployment через SSH с health checks и автоматическим rollback;
- production security headers и правила работы с секретами.

### Публичный ассистент

- orchestration на NVIDIA NOOA;
- OpenAI-совместимый LLM provider через настройки окружения;
- ограниченные read-only источники клиники;
- CSRF, rate limit, timeout, лимиты payload/history и параллелизма;
- безопасные ответы при отказе провайдера.

## Следующие этапы

Актуальные работы ведутся в [GitHub Issues](https://github.com/Rexarrior/vetirinary/issues).
Ближайшие улучшения: браузерные end-to-end тесты, мониторинг production, резервное
копирование с проверкой восстановления, доступность интерфейса и расширение тестового
покрытия. Выбор лицензии остаётся решением владельца проекта.
