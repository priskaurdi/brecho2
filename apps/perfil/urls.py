from django.urls import path
from contas import views
from perfil.views import perfil_view, editar_perfil

urlpatterns = [
    path('<slug:username>/', perfil_view, name='perfil'),
    #path('atualizar-usuario/<slug:username>/', views.atualizar_usuario, name='atualizar_usuario'),
    path('editar-perfil/<slug:username>/', editar_perfil, name='editar-perfil'),
]