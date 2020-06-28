from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='account/password_change.html', success_url=reverse_lazy('account:password_change_done')), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name='password_change_done'),
    path('password-reset', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html', email_template_name='account/password_reset_email.html', success_url=reverse_lazy('account:password_reset_done')), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html', success_url=reverse_lazy('account:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name='password_reset_complete')
]