import os
from celery import Celery  # type: ignore


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery("project")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True

# ⚠️ OTIMIZADO: Sem result backend (fire-and-forget tasks)
# Evita auto-consumo de Redis mantendo só o broker ativo

