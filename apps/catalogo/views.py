import re
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from catalogo.forms import CatalogoComentarioForm, CatalogoForm
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
    valor_busca = request.GET.get("valor")
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

    if valor_busca:
        filtros["valor__icontains"] = valor_busca

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
        form = CatalogoForm(instance=el) 
        form_dict[el] = form 
        
    # Criar uma lista de tuplas (catalogo, form) a partir do form_dict
    form_list = [(catalogo, form) for catalogo, form in form_dict.items()]
    
    # Aplicar a paginação à lista de tuplas
    paginacao = Paginator(form_list, 3) # '3' é numero de registro por pagina
    
    # Obter o número da página a partir dos parâmetros da URL
    pagina_numero = request.GET.get("page")
    page_obj = paginacao.get_page(pagina_numero)
    
    # Criar um novo dicionário form_dict com base na página atual
    form_dict = {catalogo: form for catalogo, form in page_obj}
    
    context = {'page_obj': page_obj, 'form_dict': form_dict}
    return render(request, template_view, context)


# Form de criar postagem
@login_required
def criar_catalogo(request):
    form = CatalogoForm()
    if request.method == 'POST':
        form = CatalogoForm(request.POST, request.FILES)
        if form.is_valid():
            catalogo_imagens = request.FILES.getlist('catalogo_imagens') # pega as imagens
            if len(catalogo_imagens) > 5: # faz um count
                messages.error(request, 'Você só pode adicionar no máximo 5 imagens.')
            else:
                produto = form.save(commit=False)
                produto.usuario = request.user
                form.save()
                catalogo_imagens = request.FILES.getlist('catalogo_imagens')
                for f in catalogo_imagens:
                    models.CatalogoImagem.objects.create(catalogo=produto, imagem=f)
                # Redirecionar para uma página de sucesso ou fazer qualquer outra ação desejada
                messages.success(request, 'Seu Post foi cadastrado com sucesso!')
                return redirect('lista-catalogo')
        else:
            add_form_errors_to_messages(request, form)
    return render(request, 'form-catalogo.html', {'form': form})

# Detalhe da postagem
def detalhe_catalogo(request, slug):
    catalogo = get_object_or_404(models.Catalogo, slug=slug)
    form = CatalogoForm(instance=catalogo)
    form_comentario = CatalogoComentarioForm()
    context = {'form': form,
            'catalogo': catalogo,
            'form_comentario':form_comentario}
    return render(request,'detalhe-catalogo.html', context)


# Editar Postagem (ID)
@login_required 
def editar_catalogo(request,slug):
    redirect_route = request.POST.get('redirect_route', '')
    catalogo = get_object_or_404(models.Catalogo, slug=slug)
    message = 'Seu Post '+ catalogo.produto +' foi atualizado com sucesso!'
    # Verifica se o usuário autenticado é o autor da postagem
    lista_grupos = ['administrador', 'colaborador']
    if request.user != catalogo.usuario and not (
        any(grupo.name in lista_grupos for grupo in request.user.groups.all()) or request.user.is_superuser):
        messages.warning(request, 'Seu usuário não tem permissões para acessar essa pagina.')
        return redirect('lista-catalogo')  # Redireciona para uma página de erro ou outra página adequada
    
    if request.method == 'POST':
        form = CatalogoForm(request.POST, instance=catalogo)
        if form.is_valid():
            
            contar_imagens = catalogo.catalogo_imagens.count() # Quantidade de imagens sque já tenho no post
            catalogo_imagens = request.FILES.getlist('catalogo_imagens') # Quantidade de imagens que estou enviando para salvar

            if contar_imagens + len(catalogo_imagens) > 5:
                messages.error(request, 'Você só pode adicionar no máximo 5 imagens.')
                return redirect(redirect_route)
            else: 
                form.save()
                for f in catalogo_imagens: # for para pegar as imagens e salvar.
                    models.CatalogoImagem.objects.create(catalogo=catalogo, imagem=f)
                    
                messages.warning(request,message)
                return redirect(redirect_route)
        else:
            add_form_errors_to_messages(request, form) 
    return JsonResponse({'status': message}) # Coloca por enquanto.

@login_required 
def deletar_catalogo(request, slug): 
    redirect_route = request.POST.get('redirect_route', '')
    print(redirect_route)
    catalogo = get_object_or_404(models.Catalogo, slug=slug)
    message = 'Seu Post '+catalogo.produto+' foi deletado com sucesso!' # atualizei a mesnagem aqui
    if request.method == 'POST':
        catalogo.delete()
        messages.error(request, message)
        if re.search(r'/catalogo/detalhe-catalogo/([^/]+)/', redirect_route): # se minha rota conter
            return redirect('lista-catalogo')
        return redirect(redirect_route)
    return JsonResponse({'status':message})


def remover_imagem(request):
    imagem_id = request.GET.get('imagem_id') # Id da imagem
    verifica_imagem = models.CatalogoImagem.objects.filter(id=imagem_id) # Filtra pra ver se imagem existe...
    if verifica_imagem:
        catalogo_imagem = models.CatalogoImagem.objects.get(id=imagem_id) # pega a imagem
        # Excluir a imagem do banco de dados e do sistema de arquivos (pasta postagem-forum/)
        catalogo_imagem.imagem.delete()
        catalogo_imagem.delete()
    return JsonResponse({'message': 'Imagem removida com sucesso.'})


##Comentarios
def adicionar_comentario(request, slug):
    catalogo = get_object_or_404(models.Catalogo, slug=slug)
    message = 'Comentário Adicionado com sucesso!'
    if request.method == 'POST':
        form = CatalogoComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.catalogo = catalogo
            comentario.save() 
            messages.warning(request, message)
            return redirect('detalhe-catalogo', slug=catalogo.slug)
    return JsonResponse({'status': message})


def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(models.CatalogoComentario, id=comentario_id)
    message = 'Comentário Editado com sucesso!'
    if request.method == 'POST':
        form = CatalogoComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            messages.info(request, message)
            return redirect('detalhe-catalogo',
                            slug=comentario.catalogo.slug)
    return JsonResponse({'status': message})


def deletar_comentario(request, comentario_id):
    comentario = get_object_or_404(models.CatalogoComentario, id=comentario_id)
    #postagem_slug = comentario.postagem.slug
    comentario.delete()
    messages.success(request, 'Comentário deletado com sucesso!')
    return redirect('detalhe-catalogo', slug=comentario.catalogo_slug)


def responder_comentario(request, comentario_id):
    comentario = get_object_or_404(models.CatalogoComentario, id=comentario_id)
    if request.method == 'POST':
        form = CatalogoComentarioForm(request.POST)
        message = 'Comentário Respondido com sucesso!'
        if form.is_valid():
            novo_comentario = form.save(commit=False)
            novo_comentario.usuario = request.user
            novo_comentario.parent_id = comentario_id
            novo_comentario.catalogo = comentario.catalogo
            novo_comentario.save()
            messages.info(request, message)
            return redirect('detalhe-catalogo',
                            slug=comentario.catalogo.slug)
    return JsonResponse({'status': message})