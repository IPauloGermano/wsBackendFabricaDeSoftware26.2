from django.urls import path
from . import views

app_name = 'favoritos'

urlpatterns = [
    path('', views.lista_favoritos, name='lista'),
    path('adicionar/<int:livro_id>/', views.adicionar_favorito, name='adicionar'),
    path('<int:pk>/editar/', views.editar_favorito, name='editar'),
    path('<int:pk>/remover/', views.remover_favorito, name='remover'),
    path('registro/', views.registrar_usuario, name='registro'),
]
