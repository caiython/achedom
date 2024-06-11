from celery import shared_task
from time import sleep
import requests
from django.urls import reverse


# Verificar erro: Task handler raised error: TimeLimitExceeded(1800)
@shared_task(time_limit=None)
def celery_auto_update_data(csrf_token, sleep_time=60):

    while True:
        sleep(sleep_time)
        response = requests.post(
            'http://djangoapp:80' + reverse('backend_deskmanager_update_data'),
            headers={'X-CSRFToken': csrf_token},
            cookies={'csrftoken': csrf_token},
            data={'auto_update': True}
        )

        if response.json().get('auto_updated') == False:
            return 1
