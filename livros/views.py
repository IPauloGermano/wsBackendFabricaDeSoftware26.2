from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Livro
from .forms import LivroForm
from .services import buscar_catalogo, obter_ou_criar_livro


def lista_livros(request):
    termo = request.GET.get('q', '').strip()
    origem = request.GET.get('origem', 'todos')
    buscar_na_api = (origem in ['todos', 'openlibrary'])

    resultado = buscar_catalogo(termo=termo, buscar_na_api=buscar_na_api)

    context = {
        'termo': termo,
        'origem': origem,
        'livros_locais': resultado['livros_locais'],
        'livros_remotos': resultado['livros_remotos'],
        'erro_api': resultado['erro_api'],
        'total_locais': resultado['total_locais'],
        'total_remotos': resultado['total_remotos'],
    }
    return render(request, 'livros/lista.html', context)


def detalhe_livro(request, pk=None, openlibrary_id=None):
    if openlibrary_id:
        livro = obter_ou_criar_livro(openlibrary_id)
        if not livro:
            messages.error(request, "Não foi possível carregar os dados do livro na Open Library.")
            return redirect('livros:lista')
    else:
        livro = get_object_or_404(Livro, pk=pk)

    favorito_usuario = None
    if request.user.is_authenticated:
        favorito_usuario = livro.favoritos.filter(usuario=request.user).first()

    return render(request, 'livros/detalhe.html', {
        'livro': livro,
        'favorito_usuario': favorito_usuario,
    })


@login_required
def criar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            livro = form.save()
            messages.success(request, f"Livro '{livro.titulo}' cadastrado com sucesso.")
            return redirect('livros:detalhe', pk=livro.pk)
        messages.error(request, "Verifique os erros no formulário.")
    else:
        form = LivroForm()

    return render(request, 'livros/form.html', {
        'form': form,
        'titulo_pagina': 'Cadastrar Livro',
        'botao_texto': 'Salvar Livro',
    })


@login_required
def editar_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)

    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            livro = form.save()
            messages.success(request, f"Livro '{livro.titulo}' atualizado com sucesso.")
            return redirect('livros:detalhe', pk=livro.pk)
        messages.error(request, "Verifique os erros no formulário.")
    else:
        form = LivroForm(instance=livro)

    return render(request, 'livros/form.html', {
        'form': form,
        'livro': livro,
        'titulo_pagina': f'Editar {livro.titulo}',
        'botao_texto': 'Atualizar Livro',
    })


@login_required
def excluir_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)

    if request.method == 'POST':
        titulo = livro.titulo
        livro.delete()
        messages.success(request, f"Livro '{titulo}' removido com sucesso.")
        return redirect('livros:lista')

    return render(request, 'livros/confirmar_exclusao.html', {'livro': livro})
