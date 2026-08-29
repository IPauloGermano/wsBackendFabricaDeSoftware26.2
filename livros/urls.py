from django.urls import path
from . import views

app_name = 'livros'

urlpatterns = [
    path('', views.lista_livros, name='lista'),
    path('<int:pk>/', views.detalhe_livro, name='detalhe'),
    path('ol/<str:openlibrary_id>/', views.detalhe_livro, name='detalhe_openlibrary'),
    path('novo/', views.criar_livro, name='criar'),
    path('<int:pk>/editar/', views.editar_livro, name='editar'),
    path('<int:pk>/excluir/', views.excluir_livro, name='excluir'),
]
