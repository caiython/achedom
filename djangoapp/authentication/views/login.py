from django.http import HttpRequest, JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import render
from django.urls import reverse
from authentication.forms import LoginForm
from django.contrib import messages


class Login(View):
    def post(self, request: HttpRequest) -> HttpResponse:

        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))

        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(
                request, 'The email address or password is incorrect. Please retry...')
            return HttpResponseRedirect(reverse('login'))

        login(request, user)
        return HttpResponseRedirect(reverse('home'))

    def get(self, request: HttpRequest) -> HttpResponse:

        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))

        ctx = {
            'register_url': reverse('register'),
            'form': LoginForm,
            'back_to': reverse('welcome')
        }
        return render(request, 'authentication/login.html', ctx)
