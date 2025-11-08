from django.urls import path, reverse_lazy
from . import views

app_name = 'admin_dashboard'

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='admin_dashboard/password_reset_form.html', email_template_name='admin_dashboard/password_reset_email.html', success_url=reverse_lazy('password_reset_done')), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='admin_dashboard/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='admin_dashboard/password_reset_confirm.html', success_url=reverse_lazy('password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='admin_dashboard/password_reset_complete.html'), name='password_reset_complete'),
    path('', views.dashboard, name='dashboard'),
    
    # Project management
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
    
    # Content management
    path('about/edit/', views.about_edit, name='about_edit'),
    path('home/edit/', views.home_edit, name='home_edit'),
    
    # Messages
    path('messages/', views.messages_list, name='messages_list'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),
    path('messages/<int:pk>/delete/', views.message_delete, name='message_delete'),
    
    # AI functionality
    path('ai-rewrite/', views.ai_rewrite, name='ai_rewrite'),
]