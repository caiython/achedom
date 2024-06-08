from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from backend.services.deskmanager import DESKMANAGER
from django.contrib import messages


class ClearKeys(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if not DESKMANAGER.reset_config():
            messages.error(
                request, 'Error trying to reset Desk Manager configs. Please, message the system administrator.')

        return HttpResponseRedirect(reverse('config'))
