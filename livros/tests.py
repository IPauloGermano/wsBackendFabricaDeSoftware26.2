from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Livro


class LivroModelTest(TestCase):
    def setUp(self):
        self.livro = Livro.objects.create(
            titulo="Dom Casmurro",
            autores="Machado de Assis",
            ano_publicacao=1899,
            capa_url="https://covers.openlibrary.org/b/id/12345-M.jpg"
        )

    def test_livro_str(self):
        self.assertEqual(str(self.livro), "Dom Casmurro — Machado de Assis")

    def test_tem_capa(self):
        self.assertTrue(self.livro.tem_capa)
        livro_sem_capa = Livro.objects.create(titulo="Sem Capa")
        self.assertFalse(livro_sem_capa.tem_capa)


class LivroViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="teste", password="password123")
        self.livro = Livro.objects.create(
            titulo="Memórias Póstumas de Brás Cubas",
            autores="Machado de Assis"
        )

    def test_lista_livros_status_200(self):
        response = self.client.get(reverse('livros:lista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Memórias Póstumas de Brás Cubas")

    def test_detalhe_livro_status_200(self):
        response = self.client.get(reverse('livros:detalhe', kwargs={'pk': self.livro.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.livro.titulo)

    def test_criar_livro_requer_autenticacao(self):
        url = reverse('livros:criar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username="teste", password="password123")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
