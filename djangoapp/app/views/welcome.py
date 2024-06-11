from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.urls import reverse


class Welcome(View):
    def get(self, request: HttpRequest) -> HttpResponse:

        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))

        ctx = {
            'login_url': reverse('login'),
            'register_url': reverse('register')
        }

        return render(request, 'app/welcome.html', ctx)
