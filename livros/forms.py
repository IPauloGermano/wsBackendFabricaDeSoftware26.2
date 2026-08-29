from django import forms
from .models import Livro


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autores', 'capa_url', 'isbn', 'descricao', 'assuntos']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título do livro',
            }),
            'autores': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do(s) autor(es)',
            }),
            'capa_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://exemplo.com/capa.jpg (opcional)',
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ISBN (opcional)',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descrição ou sinopse do livro...',
            }),
            'assuntos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Literatura Brasileira, Romance, Ficção',
            }),
        }
