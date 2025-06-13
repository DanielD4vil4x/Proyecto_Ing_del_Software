from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Prenda
from .forms import PrendaForm

class PrendaListView(ListView):
    model = Prenda
    template_name = 'prendas/listar.html'
    context_object_name = 'prendas'

class PrendaCreateView(CreateView):
    model = Prenda
    form_class = PrendaForm
    template_name = 'prendas/crear.html'
    success_url = reverse_lazy('listar_prendas')

class PrendaUpdateView(UpdateView):
    model = Prenda
    form_class = PrendaForm
    template_name = 'prendas/editar.html'
    success_url = reverse_lazy('listar_prendas')

class PrendaDeleteView(DeleteView):
    model = Prenda
    template_name = 'prendas/eliminar.html'
    success_url = reverse_lazy('listar_prendas')

class PrendaDetailView(DetailView):
    model = Prenda
    template_name = 'prendas/detalle.html'
    context_object_name = 'prenda'
