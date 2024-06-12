from celery import shared_task
from time import sleep
import requests
from django.urls import reverse
from django.conf import settings
from project.celery import app


@shared_task()
def celery_auto_update_data():
    response = requests.get(
        'http://djangoapp:80' + reverse('backend_deskmanager_update_data'),
        headers={'Authorization': f'SecretKey {settings.SECRET_KEY}'},
        params={'auto_update': True}
    )

    print(response.json().get('auto_updated'))
    return 1 if response.json().get('auto_updated') else 0


app.conf.beat_schedule = {
    'periodic-check-deskmanager-auto-update': {
        'task': 'backend.tasks.deskmanager.celery_auto_update_data',
        'schedule': 60.0,
    },
}
