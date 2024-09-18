import re
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages 
from catalogo import models
from base.utils import add_form_errors_to_messages, filtrar_modelo
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# Lista de postagem
def lista_catalogo(request):
    form_dict = {}
    filtros = {}

    # titulo_busca = request.GET.get("titulo")
    # if titulo_busca:
    #     filtros["titulo"] = titulo_busca
    #     filtros["descricao"] = titulo_busca

    produto_busca = request.GET.get("produto")
    descProduto_busca = request.GET.get("descProduto")
    categoria_busca = request.GET.get("categoria")
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")
    ativo = request.GET.get("ativo")

    if produto_busca:
        filtros["produto__icontains"] = produto_busca

    if ativo :
        filtros["ativo"] = ativo

    if descProduto_busca:
        filtros["descProduto__icontains"] = descProduto_busca

    if categoria_busca:
        filtros["categoria__icontains"] = categoria_busca

    if data_inicio and data_fim:
        filtros["data_publicacao__range"] = [data_inicio, data_fim]


    if request.path == '/catalogo/':
        catalogos = models.Catalogo.objects.filter(ativo=True)
        template_view = 'lista-catalogo.html'
    else:
        user = request.user
        template_view = 'dashboard/dash-lista-catalogo.html'
        if ['administrador', 'colaborador'] in user.groups.all() or user.is_superuser:
            catalogos = models.Catalogo.objects.all()
        else:
            catalogos = models.Catalogo.objects.filter(usuario=user)

    catalogos = filtrar_modelo(catalogos, **filtros)  


    for el in catalogos:
        form = PostagemForumForm(instance=el) 
        form_dict[el] = form 
        
    # Criar uma lista de tuplas (postagem, form) a partir do form_dict
    form_list = [(postagem, form) for postagem, form in form_dict.items()]
    
    # Aplicar a paginação à lista de tuplas
    paginacao = Paginator(form_list, 3) # '3' é numero de registro por pagina
    
    # Obter o número da página a partir dos parâmetros da URL
    pagina_numero = request.GET.get("page")
    page_obj = paginacao.get_page(pagina_numero)
    
    # Criar um novo dicionário form_dict com base na página atual
    form_dict = {postagem: form for postagem, form in page_obj}
    
    context = {'page_obj': page_obj, 'form_dict': form_dict}
    return render(request, template_view, context)