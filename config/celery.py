import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') # Garante que o Django esteja configurado antes do Celery inicializar
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY') # Lê as configurações do Celery a partir do settings.py, buscando apenas as variáveis com prefixo CELERY_
app.autodiscover_tasks() # Descobre automaticamente arquivos tasks.py em todos os apps instalados