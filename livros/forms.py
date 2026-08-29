from django import forms
from .models import Livro


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autores', 'ano_publicacao', 'editora', 'isbn', 'capa_url', 'assuntos', 'descricao']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título do livro',
            }),
            'autores': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do(s) autor(es)',
            }),
            'ano_publicacao': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 1899',
            }),
            'editora': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Editora (opcional)',
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ISBN (opcional)',
            }),
            'capa_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://exemplo.com/capa.jpg (opcional)',
            }),
            'assuntos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Literatura Brasileira, Romance, Ficção',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descrição ou sinopse do livro...',
            }),
        }
