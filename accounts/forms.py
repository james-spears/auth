from django import forms
from django.contrib.auth import forms as auth
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.forms import widgets
from django.contrib.auth.models import Group
from django.forms import ModelForm, ModelMultipleChoiceField, EmailInput
from app.forms import FORM_CLASS
from .models import Team, Membership

User = get_user_model()

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
