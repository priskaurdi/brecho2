import re
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from quadros.forms import QuadrosComentarioForm, QuadrosForm
from django.contrib import messages 
from quadros import models
from base.utils import add_form_errors_to_messages, filtrar_modelo
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# Lista de postagem
def lista_quadros(request):
    form_dict = {}
    filtros = {}

    # titulo_busca = request.GET.get("titulo")
    # if titulo_busca:
    #     filtros["titulo"] = titulo_busca
    #     filtros["descricao"] = titulo_busca

    quadro_busca = request.GET.get("quadro")
    descQuadro_busca = request.GET.get("descQuadro")
    #categoria_busca = request.GET.get("categoria")
    valor_busca = request.GET.get("valor")
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")
    ativo = request.GET.get("ativo")

    if quadro_busca:
        filtros["quadro__icontains"] = quadro_busca

    if ativo :
        filtros["ativo"] = ativo

    if descQuadro_busca:
        filtros["descQuadro__icontains"] = descQuadro_busca

    #if categoria_busca:
    #    filtros["categoria__icontains"] = categoria_busca

    if valor_busca:
        filtros["valor__icontains"] = valor_busca

    if data_inicio and data_fim:
        filtros["data_publicacao__range"] = [data_inicio, data_fim]


    if request.path == '/quadros/':
        quadros = models.Quadros.objects.filter(ativo=True)
        template_view = 'lista-quadros.html'
    else:
        user = request.user
        template_view = 'dashboard/dash-lista-quadros.html'
        if ['administrador', 'colaborador'] in user.groups.all() or user.is_superuser:
            quadros = models.Quadros.objects.all()
        else:
            quadros = models.Quadros.objects.filter(usuario=user)

    quadros = filtrar_modelo(quadros, **filtros)  


    for el in quadros:
        form = QuadrosForm(instance=el) 
        form_dict[el] = form 
        
    # Criar uma lista de tuplas (quadros, form) a partir do form_dict
    form_list = [(quadros, form) for quadros, form in form_dict.items()]
    
    # Aplicar a paginação à lista de tuplas
    paginacao = Paginator(form_list, 3) # '3' é numero de registro por pagina
    
    # Obter o número da página a partir dos parâmetros da URL
    pagina_numero = request.GET.get("page")
    page_obj = paginacao.get_page(pagina_numero)
    
    # Criar um novo dicionário form_dict com base na página atual
    form_dict = {quadros: form for quadros, form in page_obj}
    
    context = {'page_obj': page_obj, 'form_dict': form_dict}
    return render(request, template_view, context)

