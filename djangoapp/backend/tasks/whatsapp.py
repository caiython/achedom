from celery import shared_task
from time import sleep
import requests
from django.urls import reverse
from django.conf import settings
import json


@shared_task
def celery_update_qr_code():

    while True:
        sleep(5)
        response = requests.get(
            'http://djangoapp:80' + reverse('update_qr_code'))

        if response.json()['is_authenticated'] is True:
            return 1

        if response.json()['is_running'] is False:
            break

    return 0
