from celery import shared_task
from time import sleep
import requests
from django.urls import reverse
from django.conf import settings
from django.middleware.csrf import get_token
from django.contrib.sessions.backends.base import SessionBase


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
