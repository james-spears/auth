from logging import getLogger
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import PasswordResetView, LoginView, PasswordResetConfirmView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.signing import Signer
from django.utils.crypto import get_random_string
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm

User = get_user_model()
signer = Signer(salt=settings.SIGNER_SALT)
log = getLogger(__name__)


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
