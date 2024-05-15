from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from django.template.context_processors import csrf
from authentication.forms import RegisterForm
from authentication.models import User
import logging


class Register(FormView):

    def post(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))

        form = RegisterForm(request.POST or None)

        if form.is_valid():

            try:
                User.objects.create_user(  # type: ignore
                    email=request.POST['email'],
                    password=request.POST['password']
                )
                messages.success(
                    request, 'Your account has been successfully created.')
                return HttpResponseRedirect(reverse('login'))

            except Exception as e:
                messages.warning(
                    request, 'Internal server error. Please contact system administrator.')
                logging.error(e)
                return HttpResponseRedirect(reverse('register'))

        ctx = {
            'login_url': reverse('login'),
            'form': form
        }
        ctx.update(csrf(request))
        return render(request, 'authentication/register.html', ctx)

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        form = RegisterForm()
        ctx = {
            'login_url': reverse('login'),
            'form': form
        }
        return render(request, 'authentication/register.html', ctx)
