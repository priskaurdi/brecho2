from django.urls import path
from contas import views
from perfil.views import perfil_view

urlpatterns = [
    path('<slug:username>/', perfil_view, name='perfil'),
    path('atualizar-usuario/<slug:username>/', views.atualizar_usuario, name='atualizar_usuario'),
]