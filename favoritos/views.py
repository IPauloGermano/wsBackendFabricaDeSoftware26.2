from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from livros.models import Livro
from .models import Favorito
from .forms import RegistroUsuarioForm, FavoritoForm


def registrar_usuario(request):
    next_url = request.GET.get('next') or request.POST.get('next') or 'livros:lista'

    if request.user.is_authenticated:
        return redirect(next_url)

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Conta criada com sucesso. Bem-vindo, {user.username}!")
            if next_url.startswith('/'):
                return redirect(next_url)
            return redirect('livros:lista')
        messages.error(request, "Erro ao criar conta. Verifique os dados informados.")
    else:
        form = RegistroUsuarioForm()

    return render(request, 'registration/register.html', {'form': form, 'next': next_url})


@login_required
def lista_favoritos(request):
    # pega todos os favoritos do usuario logado
    favoritos = Favorito.objects.filter(usuario=request.user)
    context = {
        'favoritos': favoritos,
        'total_favoritos': favoritos.count(),
    }
    return render(request, 'favoritos/lista.html', context)


@login_required
@require_POST
def adicionar_favorito(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    # cria o favorito se nao existir ainda
    favorito, created = Favorito.objects.get_or_create(usuario=request.user, livro=livro)

    if created:
        messages.success(request, f"'{livro.titulo}' adicionado aos seus favoritos.")
    else:
        messages.info(request, f"'{livro.titulo}' já está na sua lista.")
    return redirect('favoritos:editar', pk=favorito.pk)


@login_required
def editar_favorito(request, pk):
    favorito = get_object_or_404(Favorito, pk=pk, usuario=request.user)

    if request.method == 'POST':
        form = FavoritoForm(request.POST, instance=favorito)
        if form.is_valid():
            form.save()
            messages.success(request, "Favorito atualizado com sucesso.")
            return redirect('favoritos:lista')
        messages.error(request, "Verifique os dados do formulário.")
    else:
        form = FavoritoForm(instance=favorito)

    return render(request, 'favoritos/editar.html', {
        'form': form,
        'favorito': favorito,
        'livro': favorito.livro,
    })


@login_required
@require_POST
def remover_favorito(request, pk):
    favorito = get_object_or_404(Favorito, pk=pk, usuario=request.user)
    titulo = favorito.livro.titulo
    favorito.delete()
    messages.success(request, f"'{titulo}' removido dos favoritos.")
    return redirect('favoritos:lista')
