from logging import getLogger
from typing import cast
from django.db.models.base import Model as Model
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, TemplateView, RedirectView
from django.contrib.auth.views import PasswordResetView, LoginView, PasswordResetConfirmView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, CreateView, UpdateView, ListView, FormView
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.core.signing import Signer
from django.urls import reverse
from django.shortcuts import get_object_or_404
from app.mixins import PaginatedMixin
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm, TeamForm, MembershipForm, MembershipInvitationForm, EmailVerificationForm
from .models import Team, Membership

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


class TeamListView(LoginRequiredMixin, PaginatedMixin, ListView):
    model = Team

    title = _("Team List")

    def create_url(self):
        return reverse("team_create")

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class TeamDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Team

    title = _("Team Detail")

    slug_field = 'slug'

    slug_url_kwarg = 'team_slug'

    def test_func(self) -> bool:
        team = cast(Team, self.get_object())
        return self.request.user.pk == team.owner.pk

    # def tickets_registered(self):
    #     return sum(map(lambda registrant: registrant.num_of_units, self.get_object().registrant_set.all()))

    # def dict(self):
    #     return model_to_dict(self.get_object())


class TeamCreateView(LoginRequiredMixin, CreateView):
    form_class = TeamForm

    model = Team

    title = _("Create Team")

    def cancel_url(self):
        return reverse('team_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TeamUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = TeamForm
    model = Team

    title = _("Update Team")

    slug_field = 'slug'

    slug_url_kwarg = 'team_slug'

    def test_func(self) -> bool:
        self.team = cast(Team, self.get_object())
        return self.request.user.pk == self.team.owner.pk

    def cancel_url(self):
        return reverse('team_detail', kwargs={'team_slug': self.team.slug})


class MembershipListView(LoginRequiredMixin, PaginatedMixin, ListView):
    model = Membership

    title = _("Membership List")

    def get_queryset(self):
        self.team = get_object_or_404(Team, owner=self.request.user, slug=self.kwargs['team_slug'])
        return super().get_queryset().filter(team=self.team).prefetch_related('team', 'groups')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = self.team
        return context


class MembershipDetailView(LoginRequiredMixin, DetailView):
    model = Membership

    title = _("Membership Detail")

    slug_field = 'uuid'

    slug_url_kwarg = 'membership_uuid'

    def get_queryset(self):
        self.team = get_object_or_404(Team, owner=self.request.user, slug=self.kwargs['team_slug'])
        return super().get_queryset().prefetch_related('groups')

    # def tickets_registered(self):
    #     return sum(map(lambda registrant: registrant.num_of_units, self.get_object().registrant_set.all()))

    # def dict(self):
    #     return model_to_dict(self.get_object())


class MembershipCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = MembershipInvitationForm

    model = Membership

    title = _("Invite Member")

    def test_func(self) -> bool:
        self.team = get_object_or_404(Team, slug=self.kwargs['team_slug'])
        return self.request.user == self.team.owner

    # def get_form_kwargs(self):
    #     kwargs = super(MemberCreateView, self).get_form_kwargs()
    #     kwargs['user'] = self.request.user  # the trick!
    #     return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['membership'] = {'team': self.team}
        context['content'] = {'permissions': _("permissions")}
        return context

    def cancel_url(self):
        return reverse('membership_list', kwargs={'team_slug': self.kwargs['team_slug']})

    def form_valid(self, form):
        form.instance.invited_by = self.request.user
        if self.team.owner != self.request.user:
            raise PermissionDenied('user is not team owner')
        form.instance.team = self.team
        return super().form_valid(form)


class MembershipUpdateView(LoginRequiredMixin, UpdateView):
    form_class = MembershipForm
    model = Membership

    title = _("Update Member")

    slug_field = 'uuid'

    slug_url_kwarg = 'membership_uuid'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('team', 'groups')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     team = cast(Membership, self.get_object()).team
    #     context['team'] = team
    #     return context
    def form_valid(self, form):
        membership = cast(Membership, self.get_object())
        if membership.team.owner != self.request.user:
            raise PermissionDenied('user is not team owner')
        form.instance.team = membership.team
        return super().form_valid(form)

    def cancel_url(self):
        return reverse(
            'membership_detail',
            kwargs={
                'membership_uuid': cast(Membership, self.get_object()).uuid,
                'team_slug': self.kwargs['team_slug']})


class EmailVerificationView(LoginRequiredMixin, FormView):
    form_class = EmailVerificationForm
    email_template_name = "registration/email_verification_email.html"
    extra_email_context = None
    from_email = None
    html_email_template_name = None
    subject_template_name = "registration/email_verification_subject.txt"
    # success_url = reverse_lazy("email_verification_done")
    template_name = "registration/email_verification_form.html"
    title = _("Email Verification")
    token_generator = default_token_generator

    title = _("Email Verification")

    success_url = '/accounts/'

    def get_success_url(self) -> str:
        return cast(str, self.success_url)

    def form_valid(self, form):
        form.user = self.request.user
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        self.object = form.save(**opts)
        return HttpResponseRedirect(self.get_success_url())


class EmailVerificationCompleteView(LoginRequiredMixin, RedirectView):
    url = "/accounts/"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        print(self.request.GET)
        if kwargs['uidb64'] and kwargs['token']:
            # pk = urlsafe_base64_decode(kwargs['uidb64']).decode('utf-8')
            token = kwargs['token']
            if not default_token_generator.check_token(self.request.user, token):
                raise PermissionDenied()
            self.request.user.is_email_verified = True  # type: ignore
            self.request.user.save()
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied()
