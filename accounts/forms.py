import logging
from django import forms
from django.contrib.auth import forms as auth
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.forms import widgets
from django.contrib.auth.models import Group
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
# from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.forms import ModelForm, ModelMultipleChoiceField, EmailInput
from app.forms import FORM_CLASS
from .models import Team, Membership

User = get_user_model()
logger = logging.getLogger("accounts.forms")

INPUT_CLASS = "block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-primary-600 sm:text-sm/6"


class CustomAuthenticationForm(auth.AuthenticationForm):
    username = auth.UsernameField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={'autofocus': True, "class": INPUT_CLASS, "placeholder": "Email"})
    )

    password = forms.CharField(
        label=_("Password"),
        max_length=254,
        widget=forms.PasswordInput(
            attrs={'autofocus': True, "class": INPUT_CLASS, "placeholder": "Password"})
    )


class CustomUserCreationForm(auth.UserCreationForm):
    class Meta():
        model = User
        fields = ['email']

    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", "class": INPUT_CLASS, "placeholder": "Email"}),
    )

    password1 = forms.CharField(
        label=_("Password"),
        max_length=254,
        widget=forms.PasswordInput(
            attrs={'autofocus': True, "class": INPUT_CLASS, "placeholder": "Password"})
    )

    password2 = forms.CharField(
        label=_("Password confirm"),
        max_length=254,
        widget=forms.PasswordInput(
            attrs={'autofocus': True, "class": INPUT_CLASS, "placeholder": "Password Confirm"})
    )


class CustomPasswordResetForm(auth.PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", "class": INPUT_CLASS, "placeholder": "Reset Password"}),
    )


class CustomSetPasswordForm(auth.SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("Password"),
        max_length=254,
        widget=forms.PasswordInput(
            attrs={'autofocus': True, "class": INPUT_CLASS})
    )

    new_password2 = forms.CharField(
        label=_("Password confirm"),
        max_length=254,
        widget=forms.PasswordInput(
            attrs={'autofocus': True, "class": INPUT_CLASS})
    )


class CustomContentTypeAdminForm(forms.ModelForm):
    class Meta:
        model = ContentType
        fields = '__all__'  # Or specify a list of fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom initialization logic here, e.g., modifying field attributes
        self.fields['model'].label = "Model"


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": FORM_CLASS, "placeholder": "Name"}),
        }


class MembershipInvitationForm(ModelForm):
    class Meta:
        model = Membership
        fields = ["email"]
        widgets = {
            "email": EmailInput(attrs={"class": FORM_CLASS, "placeholder": "Email"}),
        }


class CustomModelMultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, member):
        return member.name.title()  # f"{member.content_type.name} | {member.name}"


class MembershipForm(ModelForm):
    class Meta:
        model = Membership
        fields = ['groups']

    groups = CustomModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=widgets.CheckboxSelectMultiple(
            attrs={
                "class": "mt-1 mr-2 space-y-2",
                "placeholder": "Groups"}))


class EmailVerificationForm(forms.Form):
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        try:
            email_message.send()
        except Exception:
            logger.exception(
                "Failed to send password reset email to %s", context["user"].pk
            )

    def save(
        self,
        domain_override=None,
        subject_template_name="registration/email_verification_subject.txt",
        email_template_name="registration/email_verification_email.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        user = request.user  # type: ignore
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        user_email = user.email
        user_pk_bytes = force_bytes(str(user.pk))
        context = {
            "email": user_email,
            "domain": domain,
            "site_name": site_name,
            "uid": urlsafe_base64_encode(user_pk_bytes),
            "user": user,
            "token": token_generator.make_token(user),
            "protocol": "https" if use_https else "http",
            **(extra_email_context or {}),
        }
        self.send_mail(
            subject_template_name,
            email_template_name,
            context,
            from_email,
            user_email,
            html_email_template_name=html_email_template_name,
        )
