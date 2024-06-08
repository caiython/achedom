from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse
from django.contrib import messages
from backend.services.deskmanager import DESKMANAGER


class SaveKeys(View):
    def post(self, request: HttpRequest) -> HttpResponse:

        if not DESKMANAGER.set_keys(request.POST.get('operator_key'), request.POST.get('ambient_key')):
            messages.error(
                request, 'Error trying to set Desk Manager keys. Please check the keys provided and try again.')

        return HttpResponseRedirect(reverse('config'))
