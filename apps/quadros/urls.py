from django.urls import path 
from quadros import views

urlpatterns = [
    path('', views.lista_quadros, name='lista-quadros'),
    path('dashboard/lista-quadros/', views.lista_quadros, name='dash-lista-quadros'), 
    path('criar-quadros/', views.criar_quadros, name='criar-quadros'),
    path('detalhe-quadros/<str:slug>/', views.detalhe_quadros, name='detalhe-quadros'),
    path('editar-quadros/<str:slug>/', views.editar_quadros, name='editar-quadros'),
    path('deletar-quadros/<str:slug>/', views.deletar_quadros, name='deletar-quadros'),
    

    #AJAX
    #path('remover-imagem/', views.remover_imagem, name='remover-imagem'),

    # #Comentarios
    path('adicionar-comentario/<str:slug>/', views.adicionar_comentario, name='adicionar-comentario'),
    path('editar-comentario/<int:comentario_id>/', views.editar_comentario, name='editar-comentario'),
    path('deletar-comentario/<int:comentario_id>/', views.deletar_comentario, name='deletar-comentario'),
    path('responder-comentario/<int:comentario_id>/', views.responder_comentario, name='responder-comentario'),
]