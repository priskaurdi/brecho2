from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def painel_view(request):
    return render(request, 'painel.html')

@login_required
def configuracao_view(request):
    return render(request, 'configuracao.html')