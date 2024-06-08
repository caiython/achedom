from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from backend.services.deskmanager import DESKMANAGER


class ClearDataUpdateMode(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if not DESKMANAGER.api_token and not DESKMANAGER.data_update_mode:
            return HttpResponseRedirect(reverse('config'))

        DESKMANAGER.data_update_mode = None
        return HttpResponseRedirect(reverse('config'))
