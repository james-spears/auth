from django.urls import path

from . import views  # , GitHubCallbackView
from django.contrib.auth import get_user_model
User = get_user_model()


urlpatterns = [
    path("signup/", views.CustomSignUpView.as_view(), name="signup"),
    path("password_reset/", views.CustomPasswordResetView.as_view(),
         name="password_reset"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path(
        "reset/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "verify_email/",
        views.EmailVerificationView.as_view(),
        name="verify_email",
    ),
    path(
        "verify_email_complete/<uidb64>/<token>",
        views.EmailVerificationCompleteView.as_view(),
        name="verify_email_complete",
    ),
    path("", views.BaseView.as_view(), name="accounts"),
    #     path(
    #         "profile/",
    #         views.ProfileView.as_view(),
    #         name="profile",
    #     ),
    #     path("settings", views.SettingUpdateView.as_view(), name="setting_update"),

    path("teams", views.TeamListView.as_view(),
         name="team_list"),
    path("teams/create", views.TeamCreateView.as_view(),
         name="team_create"),
    path("teams/<slug:team_slug>", views.TeamDetailView.as_view(),
         name="team_detail"),
    path("teams/<slug:team_slug>/update", views.TeamUpdateView.as_view(),
         name="team_update"),

    path("teams/<slug:team_slug>/members", views.MembershipListView.as_view(),
         name="membership_list"),
    path("teams/<slug:team_slug>/members/create", views.MembershipCreateView.as_view(),
         name="membership_create"),
    path("teams/<slug:team_slug>/members/<uuid:membership_uuid>", views.MembershipDetailView.as_view(),
         name="membership_detail"),
    path("teams/<slug:team_slug>/members/<uuid:membership_uuid>/update", views.MembershipUpdateView.as_view(),
         name="membership_update"),
]
