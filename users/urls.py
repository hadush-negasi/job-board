from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/select-role/', views.select_role_view, name='select_role'),
    path("signup/", views.signup_view, name="signup"),
    path("complete-profile/", views.complete_profile, name="complete_profile"),  # First-time completion
    path("edit-profile/", views.complete_profile, {"edit": True}, name="edit_profile"),  # Editing profile later
    path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("account/", views.account_view, name="account"),
]
