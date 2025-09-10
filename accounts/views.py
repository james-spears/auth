import json
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, TemplateView, RedirectView
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.views import PasswordResetView, LoginView, PasswordResetConfirmView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomSignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    logo = settings.LOGO_URL


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    logo = settings.LOGO_URL


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    logo = settings.LOGO_URL


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy("login")
    logo = settings.LOGO_URL


class BaseView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/index.html"


class AuthenticatedView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        return render(request, '200.html', {})


class AuthorizedView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = []

    def get_permission_required(self) -> list[str]:
        permission_list = self.request.GET.getlist('permissions')
        if permission_list:
            return permission_list
        else:
            return super().get_permission_required()

    def get(self, request, *args, **kwargs) -> HttpResponse:
        return render(request, '200.html')
