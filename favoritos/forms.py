from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Favorito


class RegistroUsuarioForm(UserCreationForm):
    # Form de cadastro com estilização para o template
    username = forms.CharField(
        label="Nome de Usuário",
        max_length=150,
        help_text="Obrigatório. Letras, números e @/./+/-/_ apenas.",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Escolha um nome de usuário',
            'autofocus': True
        })
    )
    email = forms.EmailField(
        label="E-mail",
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu.email@exemplo.com (opcional)'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Digite sua senha'
            })
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Confirme sua senha'
            })


class FavoritoForm(forms.ModelForm):
    # Form para avaliar e atualizar leitura do livro
    class Meta:
        model = Favorito
        fields = ['nota', 'pagina_atual', 'anotacoes']
        widgets = {
            'nota': forms.Select(attrs={
                'class': 'form-control'
            }),
            'pagina_atual': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 120',
                'min': '0'
            }),
            'anotacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escreva suas reflexões, anotações e impressões sobre a leitura...'
            }),
        }

    def clean_pagina_atual(self):
        pagina = self.cleaned_data.get('pagina_atual')
        if pagina is not None and pagina < 0:
            raise forms.ValidationError("A página atual não pode ser negativa.")
        return pagina or 0
