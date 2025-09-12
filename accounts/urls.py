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
    path("", views.BaseView.as_view(), name="accounts"),
    #     path(
    #         "profile/",
    #         views.ProfileView.as_view(),
    #         name="profile",
    #     ),
    #     path("settings", views.SettingUpdateView.as_view(), name="setting_update"),

    #     path("teams", views.TeamListView.as_view(),
    #          name="team_list"),
    #     path("teams/create", views.TeamCreateView.as_view(),
    #          name="team_create"),
    #     path("teams/<slug:team_slug>", views.TeamDetailView.as_view(),
    #          name="team_detail"),
    #     path("teams/<slug:team_slug>/update", views.TeamUpdateView.as_view(),
    #          name="team_update"),

    #     path("teams/<slug:team_slug>/members", views.MemberListView.as_view(),
    #          name="member_list"),
    #     path("teams/<slug:team_slug>/members/create", views.MemberCreateView.as_view(),
    #          name="member_create"),
    #     path("teams/<slug:team_slug>/members/<slug:member_slug>", views.MemberDetailView.as_view(),
    #          name="member_detail"),
    #     path("teams/<slug:team_slug>/members/<slug:member_slug>/update", views.MemberUpdateView.as_view(),
    #          name="member_update"),
]
