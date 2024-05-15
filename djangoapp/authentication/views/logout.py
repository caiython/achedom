from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.views import View
from django.urls import reverse


class Logout(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        return HttpResponseRedirect(reverse('login'))
