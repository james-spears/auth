from logging import getLogger
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import PasswordResetView, LoginView, PasswordResetConfirmView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.signing import Signer
from django.urls import reverse
from django.shortcuts import get_object_or_404
from app.mixins import PaginatedMixin
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm, TeamForm, MembershipForm, MembershipInvitationForm
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


class TeamListView(PaginatedMixin, ListView):
    model = Team

    title = _("Team List")

    def create_url(self):
        return reverse("team_create")

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class TeamDetailView(DetailView):
    model = Team

    title = _("Team Detail")

    slug_field = 'slug'

    slug_url_kwarg = 'team_slug'

    # def tickets_registered(self):
    #     return sum(map(lambda registrant: registrant.num_of_units, self.get_object().registrant_set.all()))

    # def dict(self):
    #     return model_to_dict(self.get_object())


class TeamCreateView(CreateView):
    form_class = TeamForm

    model = Team

    title = _("Create Team")

    # def get_form_kwargs(self):
    #     kwargs = super(TeamCreateView, self).get_form_kwargs()
    #     kwargs['user'] = self.request.user  # the trick!
    #     return kwargs

    def cancel_url(self):
        return reverse('team_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TeamUpdateView(UpdateView):
    form_class = TeamForm
    model = Team

    title = _("Update Team")

    slug_field = 'slug'

    slug_url_kwarg = 'team_slug'

    def cancel_url(self):
        return reverse('team_detail', kwargs={'team_slug': self.get_object().slug})


class MembershipListView(PaginatedMixin, ListView):
    model = Membership

    title = _("Membership List")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = get_object_or_404(Team, slug=self.kwargs['team_slug'])
        context['team'] = team
        return context

    def get_queryset(self):
        team = get_object_or_404(Team, owner=self.request.user, slug=self.kwargs['team_slug'])
        return super().get_queryset().filter(team=team)


class MembershipDetailView(DetailView):
    model = Membership

    title = _("Membership Detail")

    slug_field = 'uuid'

    slug_url_kwarg = 'membership_uuid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = get_object_or_404(Team, slug=self.kwargs['team_slug'])
        context['team'] = team
        return context

    # def tickets_registered(self):
    #     return sum(map(lambda registrant: registrant.num_of_units, self.get_object().registrant_set.all()))

    # def dict(self):
    #     return model_to_dict(self.get_object())


class MembershipCreateView(CreateView):
    form_class = MembershipInvitationForm

    model = Membership

    title = _("Invite Member")

    # def get_form_kwargs(self):
    #     kwargs = super(MemberCreateView, self).get_form_kwargs()
    #     kwargs['user'] = self.request.user  # the trick!
    #     return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = get_object_or_404(Team, slug=self.kwargs['team_slug'])
        context['team'] = team
        context['content'] = {'permissions': _("permissions")}
        return context

    def cancel_url(self):
        return reverse('membership_list', kwargs={'team_slug': self.kwargs['team_slug']})

    def form_valid(self, form):
        team = get_object_or_404(Team, slug=self.kwargs['team_slug'])
        form.instance.team = team
        return super().form_valid(form)


class MembershipUpdateView(UpdateView):
    form_class = MembershipForm
    model = Membership

    title = _("Update Member")

    slug_field = 'uuid'

    slug_url_kwarg = 'membership_uuid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = get_object_or_404(Team, slug=self.kwargs['team_slug'])
        context['team'] = team
        return context

    def cancel_url(self):
        return reverse(
            'membership_detail',
            kwargs={
                'membership_uuid': self.get_object().uuid,
                'team_slug': self.kwargs['team_slug']})
