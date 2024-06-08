from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from backend.services.deskmanager import DESKMANAGER


class SetDataUpdateMode(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if not DESKMANAGER.api_token:
            return HttpResponseRedirect(reverse('config'))

        DESKMANAGER.set_data_update_mode(request.POST.get('mode'))
        return HttpResponseRedirect(reverse('config'))
