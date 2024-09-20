import re
from django.forms import ValidationError
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


# Form de criar postagem
@login_required
def criar_quadros(request):
    if request.method == 'POST':
        form = QuadrosForm((request.POST, request.FILES))
        if form.is_valid():
            quadros_imagens = request.FILES.getlist('quadros_imagens') # pega as imagens
            if len(quadros_imagens) > 5: # faz um count
                messages.error(request, 'Você só pode adicionar no máximo 5 imagens.')
            else:
                quadro = form.save(commit=False)
                quadro.usuario = request.user
                form.save()
                for f in quadros_imagens:
                    models.QuadrosImagem.objects.create(quadros=quadro, imagem=f)
                # Redirecionar para uma página de sucesso ou fazer qualquer outra ação desejada
                messages.success(request, 'Seu quadro foi cadastrado com sucesso!')
                return redirect('lista_quadros')
        else:
            add_form_errors_to_messages(request, form)
    else:
        form = QuadrosForm
    return render(request, 'form-quadros.html', {'form': form})

# Detalhe da postagem
def detalhe_quadros(request, slug):
    quadros = get_object_or_404(models.Quadros, slug=slug)
    form = QuadrosForm(instance=quadros)
    form_comentario = QuadrosComentarioForm()
    context = {'form': form,
            'quadros': quadros,
            'form_comentario':form_comentario}
    return render(request,'detalhe-quadros.html', context)


# Editar Postagem (ID)
@login_required 
def editar_quadros(request,slug):
    redirect_route = request.POST.get('redirect_route', '')
    quadros = get_object_or_404(models.Quadros, slug=slug)
    #message = 'Seu Post '+ quadros.quadro +' foi atualizado com sucesso!'
    # Verifica se o usuário autenticado é o autor da postagem
    lista_grupos = ['administrador', 'colaborador']
    if request.user != quadros.usuario and not (
        any(grupo.name in lista_grupos for grupo in request.user.groups.all()) or request.user.is_superuser):
        messages.warning(request, 'Seu usuário não tem permissões para acessar essa pagina.')
        return redirect('lista_quadros')  # Redireciona para uma página de erro ou outra página adequada
    
    if request.method == 'POST':
        form = QuadrosForm(request.POST, request.FILES, instance=quadros)
        if form.is_valid():
            quadros_imagens = request.FILES.getlist('quadros_imagens') # Quantidade de imagens que estou enviando para salvar
            contar_imagens = quadros.quadros_imagens.count() # Quantidade de imagens sque já tenho no post
            if contar_imagens + len(quadros_imagens) > 5:
                messages.error(request, 'Você só pode adicionar no máximo 5 imagens.')
                return redirect(redirect_route)
            else: 
                form.save()
                for f in quadros_imagens:
                    models.QuadrosImagem.objects.create(quadros=quadros, imagem=f)
                messages.success(request, 'O quadro foi atualizado com sucesso!')
                return redirect('detalhe-quadros', slug=quadros.slug)
        else:
            add_form_errors_to_messages(request, form)
    else:
        form = QuadrosForm(instance=quadros)
    return render(request, 'form-quadros.html', {'form': form})

@login_required 
def deletar_quadros(request, slug): 
    redirect_route = request.POST.get('redirect_route', '')
    quadros = get_object_or_404(models.Quadros, slug=slug)
    message = 'Seu quadro '+quadros.quadro+' foi deletado com sucesso!' # atualizei a mesnagem aqui
    if request.method == 'POST':
        quadros.delete()
        messages.success(request, 'O quadro foi deletado com sucesso!')
        if re.search(r'/quadros/detalhe-quadros/([^/]+)/', redirect_route): # se minha rota conter
            return redirect('lista_quadros')
        return redirect(redirect_route)
    return JsonResponse({'status':message})


def remover_imagem(request):
    imagem_id = request.GET.get('imagem_id') # Id da imagem
    verifica_imagem = models.QuadrosImagem.objects.filter(id=imagem_id) # Filtra pra ver se imagem existe...
    if verifica_imagem:
        quadros_imagem = models.QuadrosImagem.objects.get(id=imagem_id) # pega a imagem
        # Excluir a imagem do banco de dados e do sistema de arquivos (pasta postagem-forum/)
        quadros_imagem.imagem.delete()
        quadros_imagem.delete()
    return JsonResponse({'message': 'Imagem removida com sucesso.'})


##Comentarios
def adicionar_comentario(request, slug):
    quadros = get_object_or_404(models.Quadros, slug=slug)
    message = 'Comentário Adicionado com sucesso!'
    if request.method == 'POST':
        form = QuadrosComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.quadros = quadros
            comentario.save() 
            messages.warning(request, message)
            return redirect('detalhe-catalogo', slug=quadros.slug)
    return JsonResponse({'status': message})


def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(models.QuadrosComentario, id=comentario_id)
    message = 'Comentário Editado com sucesso!'
    if request.method == 'POST':
        form = QuadrosComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            messages.info(request, message)
            return redirect('detalhe-quadros',
                            slug=comentario.quadros.slug)
    return JsonResponse({'status': message})


def deletar_comentario(request, comentario_id):
    comentario = get_object_or_404(models.QuadrosComentario, id=comentario_id)
    #postagem_slug = comentario.postagem.slug
    comentario.delete()
    messages.success(request, 'Comentário deletado com sucesso!')
    return redirect('detalhe-quadros', slug=comentario.quadros_slug)


def responder_comentario(request, comentario_id):
    comentario = get_object_or_404(models.QuadrosComentario, id=comentario_id)
    if request.method == 'POST':
        form = QuadrosComentarioForm(request.POST)
        message = 'Comentário Respondido com sucesso!'
        if form.is_valid():
            novo_comentario = form.save(commit=False)
            novo_comentario.usuario = request.user
            novo_comentario.parent_id = comentario_id
            novo_comentario.quadros = comentario.quadros
            novo_comentario.save()
            messages.info(request, message)
            return redirect('detalhe-quadros',
                            slug=comentario.quadros.slug)
    return JsonResponse({'status': message})





