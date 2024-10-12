from django.urls import path, include
from config import views

urlpatterns = [
    path('', views.painel_view, name='painel'), 
    path('configuracao/', views.configuracao_view, name='configuracao'), 
    path('relatorio/', views.relatorio_view, name='relatorio'),
    path('catalogo/', views.catalogo_view, name='catalogo'),
    path('quadros/', views.quadros_view, name='quadros'),
    path('pagamentos/', include('apps.pagamentos.urls')),
]