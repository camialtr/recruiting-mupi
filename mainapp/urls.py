from django.urls import path
from . import views

urlpatterns = [
    path('', views.landpage, name='landpage'),
    path('login/', views.LoginViewCustom.as_view(), name='login'),
    path('logout/', views.logout_confirm, name='logout_confirm'),

    path('messages/', views.messages_list, name='messages_list'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),
    path('messages/<int:pk>/edit/', views.message_edit, name='message_edit'),
    path('messages/<int:pk>/delete/', views.message_delete_confirm, name='message_delete_confirm'),
]