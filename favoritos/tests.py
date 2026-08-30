from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from livros.models import Livro
from .models import Favorito


class FavoritoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="leitor", password="password123")
        self.livro = Livro.objects.create(titulo="O Cortiço", autores="Aluísio Azevedo")
        self.favorito = Favorito.objects.create(
            usuario=self.user,
            livro=self.livro,
            nota=5,
            pagina_atual=42,
            anotacoes="Excelente clássico naturalista."
        )

    def test_favorito_str(self):
        self.assertEqual(str(self.favorito), "leitor - O Cortiço")

    def test_favorito_nota_choices(self):
        self.assertEqual(self.favorito.get_nota_display(), "5 - Excelente")


class FavoritoViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="leitor1", password="password123")
        self.livro = Livro.objects.create(titulo="Capitães da Areia", autores="Jorge Amado")

    def test_lista_favoritos_requer_login(self):
        response = self.client.get(reverse('favoritos:lista'))
        self.assertEqual(response.status_code, 302)

    def test_adicionar_favorito(self):
        self.client.login(username="leitor1", password="password123")
        url = reverse('favoritos:adicionar', kwargs={'livro_id': self.livro.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Favorito.objects.filter(usuario=self.user, livro=self.livro).exists())

    def test_editar_favorito(self):
        self.client.login(username="leitor1", password="password123")
        favorito = Favorito.objects.create(usuario=self.user, livro=self.livro)
        url = reverse('favoritos:editar', kwargs={'pk': favorito.pk})
        response = self.client.post(url, {
            'nota': 4,
            'pagina_atual': 50,
            'anotacoes': 'Muito bom até aqui'
        })
        self.assertEqual(response.status_code, 302)
        favorito.refresh_from_db()
        self.assertEqual(favorito.nota, 4)
        self.assertEqual(favorito.pagina_atual, 50)

    def test_remover_favorito(self):
        self.client.login(username="leitor1", password="password123")
        favorito = Favorito.objects.create(usuario=self.user, livro=self.livro)
        url = reverse('favoritos:remover', kwargs={'pk': favorito.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Favorito.objects.filter(pk=favorito.pk).exists())
