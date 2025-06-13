from django.urls import path
from applications.prendas import views

from django.urls import path
from .views import (
    PrendaListView,
    PrendaCreateView,
    PrendaUpdateView,
    PrendaDeleteView,
    PrendaDetailView,
)

urlpatterns = [
    path('', PrendaListView.as_view(), name='listar_prendas'),
    path('crear/', PrendaCreateView.as_view(), name='crear_prenda'),
    path('<int:pk>/editar/', PrendaUpdateView.as_view(), name='editar_prenda'),
    path('<int:pk>/eliminar/', PrendaDeleteView.as_view(), name='eliminar_prenda'),
    path('<int:pk>/', PrendaDetailView.as_view(), name='detalle_prenda'),
]
