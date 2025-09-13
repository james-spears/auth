from django import forms
from django.contrib.auth import forms as auth
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.forms import widgets
from django.contrib.auth.models import Permission
from django.forms import ModelForm, ModelMultipleChoiceField, EmailInput
from app.forms import FORM_CLASS
from .models import Team, Membership

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
        model = get_user_model()
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
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get distinct content_types from your related model
        content_types = ContentType.objects.all().distinct()

        for content_type in content_types:
            # Create a separate field for each content_type
            field_name = content_type.model
            queryset = Permission.objects.filter(content_type=content_type)

            self.fields[field_name] = CustomModelMultipleChoiceField(
                queryset=queryset,
                required=False,
                widget=widgets.CheckboxSelectMultiple(
                    attrs={
                        "class": "mt-1 mr-2 space-y-2"}))

            self.fields[field_name].initial = self.instance.permissions.filter(content_type=content_type)

    def clean(self):
        # Call the parent's clean method to ensure default validation runs
        val = super().clean()
        print(val, self.is_valid(), self.errors)

    def save(self, commit=True):
        # Get the instance without saving it to the database yet
        instance = super().save(commit=False)
        content_types = ContentType.objects.all().distinct()

        permissions = []
        for content_type in content_types:
            permissions += list(self.cleaned_data[content_type.model])

        instance.permissions.set(permissions)

        # Save the instance to the database if commit is True
        if commit:
            instance.save()
            # If you have ManyToMany fields and commit=False was used
            # you need to call save_m2m() manually after saving the instance
            self.save_m2m()

        return instance
    # permissions = CustomModelMultipleChoiceField(
    #     queryset=Permission.objects.filter(codename__startswith="external"),
    #     widget=widgets.CheckboxSelectMultiple(
    #         attrs={
    #             "class": "mt-1 mr-2 space-y-2",
    #             "placeholder": "Permissions"}))
