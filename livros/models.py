from django.db import models
from django.urls import reverse


class Livro(models.Model):
    openlibrary_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        verbose_name='Open Library ID'
    )
    titulo = models.CharField(
        max_length=255,
        verbose_name='Título'
    )
    autores = models.CharField(
        max_length=255,
        verbose_name='Autores'
    )
    capa_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name='URL da Capa'
    )
    isbn = models.CharField(
        max_length=32,
        blank=True,
        verbose_name='ISBN'
    )
    descricao = models.TextField(
        blank=True,
        verbose_name='Descrição'
    )
    assuntos = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='Assuntos'
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'

    def __str__(self):
        if self.autores:
            return f"{self.titulo} — {self.autores}"
        return self.titulo

    def get_absolute_url(self):
        return reverse('livros:detalhe', kwargs={'pk': self.pk})

    @property
    def tem_capa(self):
        return bool(self.capa_url and self.capa_url.strip())
