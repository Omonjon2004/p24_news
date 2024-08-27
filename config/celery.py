# config/celery.py

import os
from celery import Celery

# Django sozlamalari modulini belgilash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Celery ilovasini yaratish
app = Celery('config')  # 'config' o‘rniga loyihangiz nomini yozing

# Django sozlamalaridan Celery konfiguratsiyasini yuklash
app.config_from_object('django.conf:settings', namespace='CELERY')

# Broker URL manzilini sozlash (Redis)
app.conf.broker_url = 'redis://localhost:6379/0'

# Django ilovalaridagi vazifalarni avtomatik topish
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
