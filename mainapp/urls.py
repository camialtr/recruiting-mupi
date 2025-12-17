from django.urls import path
from . import views

urlpatterns = [
    path('', views.landpage, name='landpage'),
    path('logout/', views.logout_confirm, name='logout_confirm'),

    path('admin/', views.dashboard, name='admin'),
    path('admin/stats/', views.dashboard_stats, name='dashboard_stats'),
    path('messages/', views.redirect_to_admin, name='messages_redirect'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),
    path('messages/<int:pk>/edit/', views.message_edit, name='message_edit'),
    path('messages/<int:pk>/delete/', views.message_delete_confirm, name='message_delete_confirm'),
    path('messages/<int:pk>/toggle-read/', views.toggle_message_read, name='toggle_message_read'),
    
    # Gerenciamento de usuários (apenas devs)
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/change-password/', views.user_change_password, name='user_change_password'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),

    # Override allauth urls to restrict access (only HTMX allowed)
    path('accounts/password/reset/', views.password_reset_modal, name='account_reset_password'),
    path('accounts/signup/', views.signup_modal, name='account_signup'),
]