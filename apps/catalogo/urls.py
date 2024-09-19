from django.urls import path 
from catalogo import views

urlpatterns = [
    path('', views.lista_catalogo, name='lista-catalogo'),
    path('dashboard/lista-catalogo/', views.lista_catalogo, name='dash-lista-catalogo'), 
    path('criar-catalogo/', views.criar_catalogo, name='criar-catalogo'),
    path('detalhe-catalogo/<str:slug>/', views.detalhe_catalogo, name='detalhe-catalogo'),
    path('editar-catalogo/<str:slug>/', views.editar_catalogo, name='editar-catalogo'),
    path('deletar-catalogo/<str:slug>/', views.deletar_catalogo, name='deletar-catalogo'),
    

    #AJAX
    #path('remover-imagem/', views.remover_imagem, name='remover-imagem'),

    # #Comentarios
    path('adicionar-comentario/<str:slug>/', views.adicionar_comentario, name='adicionar-comentario'),
    path('editar-comentario/<int:comentario_id>/', views.editar_comentario, name='editar-comentario'),
    path('deletar-comentario/<int:comentario_id>/', views.deletar_comentario, name='deletar-comentario'),
    path('responder-comentario/<int:comentario_id>/', views.responder_comentario, name='responder-comentario'),
]