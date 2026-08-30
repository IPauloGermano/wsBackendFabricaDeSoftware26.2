from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contas/', include('django.contrib.auth.urls')),
    path('favoritos/', include('favoritos.urls')),
    path('', include('livros.urls')),
]
