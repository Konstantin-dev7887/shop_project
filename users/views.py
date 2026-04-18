from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import LoginView
from .forms import UserRegisterForm
from .models import User

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        send_mail(
            subject='Добро пожаловать в наш магазин!',
            message=f'Здравствуйте, {user.email}!\nСпасибо за регистрацию.',
            from_email=settings.DEFAULT_FROM_EMAIL or 'admin@example.com',
            recipient_list=[user.email],
            fail_silently=False,
        )
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
