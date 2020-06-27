from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='account/password_change.html', success_url=reverse_lazy('account:password-change-done')), name='password-change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name='password-change-done'),
]