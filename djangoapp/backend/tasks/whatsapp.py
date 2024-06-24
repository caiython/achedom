from celery import shared_task
from time import sleep
import requests
from django.urls import reverse
from django.conf import settings
from django.middleware.csrf import get_token
from django.contrib.sessions.backends.base import SessionBase
from project.celery import app


@shared_task
def celery_update_qr_code(csrf_token):

    while True:
        sleep(5)
        response = requests.post(
            'http://djangoapp:80' + reverse('backend_whatsapp_update_qr_code'),
            headers={'X-CSRFToken': csrf_token},
            cookies={'csrftoken': csrf_token},
        )

        if response.json()['is_authenticated'] is True:
            return 1

        if response.json()['is_running'] is False:
            break

    return 0


@shared_task
def celery_send(target, message, csrf_token):

    response = requests.post(
        'http://djangoapp:80' + reverse('backend_whatsapp_send'),
        data={"target": target, "message": message},
        headers={'X-CSRFToken': csrf_token},
        cookies={'csrftoken': csrf_token},
    )

    if response.json()['sent'] is True:
        return 1

    if response.json()['sent'] is False:
        return 0


@shared_task()
def celery_prevent_selenium_session_timeout():
    response = requests.get(
        'http://djangoapp:80' +
        reverse('backend_whatsapp_prevent_selenium_session_timeout'),
        headers={'Authorization': f'SecretKey {settings.SECRET_KEY}'},
    )

    return 1 if response.status_code == 200 else 0


app.conf.beat_schedule = app.conf.beat_schedule | {
    'periodic-prevent-selenium-session-timeout': {
        'task': 'backend.tasks.whatsapp.celery_prevent_selenium_session_timeout',
        'schedule': settings.SE_NODE_SESSION_TIMEOUT/2,
    },
}
