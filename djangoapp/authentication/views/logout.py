from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.views import View
from django.urls import reverse
from django.shortcuts import render
from authentication.forms import LogoutForm


class Logout(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        logout(request)
        return HttpResponseRedirect(reverse('login'))

    def get(self, request: HttpRequest) -> HttpResponse:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        form = LogoutForm()
        ctx = {
            'form': form
        }
        return render(request, 'authentication/logout.html', ctx)
