from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.urls import reverse


class Home(View):
    def get(self, request: HttpRequest) -> HttpResponse:

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('welcome'))

        ctx = {
            'home': True,
            'is_staff': request.user.is_staff,
            'logout_url': reverse('logout')
        }
        return render(request, 'app/index.html', ctx)
