from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Favorito(models.Model):
    NOTA_CHOICES = [
        (1, '1 - Ruim'),
        (2, '2 - Regular'),
        (3, '3 - Bom'),
        (4, '4 - Muito Bom'),
        (5, '5 - Excelente'),
    ]

    # relacao com usuario e livro
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoritos')
    livro = models.ForeignKey('livros.Livro', on_delete=models.CASCADE, related_name='favoritos')
    nota = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=NOTA_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    pagina_atual = models.PositiveIntegerField(default=0)
    anotacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-atualizado_em']
        verbose_name = "Favorito"
        verbose_name_plural = "Favoritos"
        # nao deixa o usuario favoritar o mesmo livro duas vezes
        unique_together = ['usuario', 'livro']

    def __str__(self):
        return f"{self.usuario.username} - {self.livro.titulo}"
