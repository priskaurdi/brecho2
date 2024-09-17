from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from forum.forms import PostagemForumForm
from contas.models import MyUser
from django.core.paginator import Paginator
from django.contrib import messages
from base.utils import filtrar_modelo
from contas.forms import UserChangeForm
from perfil.forms import PerfilForm
from perfil.models import Perfil

# Create your views here.
def perfil_view(request, username):
    modelo = MyUser.objects.select_related('perfil').prefetch_related('user_postagem_forum')
    perfil = get_object_or_404(modelo, username=username)

    perfil_postagens = perfil.user_postagem_forum.all() # Todas as postagens relacionadas com perfil
    filtros = {} # Filtro dict

    # valor_busca = request.GET.get("titulo") # Pego parametro
    # if valor_busca:
    #     filtros["titulo"] = valor_busca # Adiciono no dicionario
    #     filtros["descricao"] = valor_busca # Adiciono no dicionario

    titulo_busca = request.GET.get("titulo")
    autor_busca = request.GET.get("autor")
    categoria_busca = request.GET.get("categoria")
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")
    ativo = request.GET.get("ativo")

    if titulo_busca:
        filtros["titulo__icontains"] = titulo_busca

    if ativo :
        filtros["ativo"] = ativo

    if autor_busca:
        filtros["autor__icontains"] = autor_busca

    if categoria_busca:
        filtros["categoria__icontains"] = categoria_busca

    if data_inicio and data_fim:
        filtros["data_publicacao__range"] = [data_inicio, data_fim]

        # Utiliza o modelo das postagens do perfil
        perfil_postagens = filtrar_modelo(perfil_postagens, **filtros) # Faz o filtro

    form_dict = {}
    for el in perfil_postagens:
        form = PostagemForumForm(instance=el) 
        form_dict[el] = form
    
    # Criar uma lista de tuplas (postagem, form) a partir do form_dict
    form_list = [(postagem, form) for postagem, form in form_dict.items()]
    
    # Aplicar a paginação à lista de tuplas
    paginacao = Paginator(form_list, 3)
    
    # Obter o número da página a partir dos parâmetros da URL
    pagina_numero = request.GET.get("page")
    page_obj = paginacao.get_page(pagina_numero)
    
    # Criar um novo dicionário form_dict com base na página atual
    form_dict = {postagem: form for postagem, form in page_obj}
    context = {'obj': perfil, 'page_obj': page_obj, 'form_dict':form_dict}
    return render(request, 'perfil.html', context)


#Editar perfil (contas e perfil)
@login_required 
def editar_perfil(request, username):
    redirect_route = request.POST.get('redirect_route', '')

    modelo_myuser = MyUser.objects.get(username=username)
    modelo_perfil = Perfil.objects.get(usuario__username=username)

    message = 'Seu Perfil foi atualizado com sucesso!'

    if request.user.username != modelo_myuser.username and not (
        ['administrador', 'colaborador'] in request.user.groups.all() or request.user.is_superuser):
        return redirect('lista-postagem-forum')  # Adicionar uma rota "sem permissão"

    if request.method == 'POST':
        form_contas = UserChangeForm(request.POST, user=request.user, instance=modelo_myuser)
        form_perfil = PerfilForm(request.POST, request.FILES, instance=modelo_perfil)

        if form_perfil.is_valid() and form_contas.is_valid():
            form_contas.save()
            form_perfil.save()
            messages.warning(request, message)
            return redirect(redirect_route)
    else:
        form_contas = UserChangeForm(user=request.user, instance=modelo_myuser)
        form_perfil = PerfilForm(instance=modelo_perfil)

    context = {'form_perfil': form_perfil, 'form_contas': form_contas, 'obj': modelo_myuser}
    return render(request, 'editar-perfil-form.html', context)