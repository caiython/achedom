from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages


class ServiceOrders(View):
    def get(self, request: HttpRequest) -> HttpResponse:

        if not request.user.is_authenticated:
            messages.warning(
                request, 'The page you are trying to access requires authentication. Please login.')
            return HttpResponseRedirect(reverse('login'))

        ctx = {
            'service_orders': True,
            'is_staff': request.user.is_staff,
            'logout_url': reverse('logout')
        }

        return render(request, 'app/service_orders.html', ctx)
