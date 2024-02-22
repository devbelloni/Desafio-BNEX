from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Produto
from django.urls import reverse_lazy


class ProdutoListView(ListView):
    model = Produto
    template_name = 'produto_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AuthenticationForm()
        return context


class ProdutoDetailView(DetailView):
    model = Produto
    template_name = 'produto_detail.html'


class ProdutoCreateView(CreateView):
    model = Produto
    template_name = 'produto_form.html'
    fields = ['nome', 'descricao', 'valor']
    success_url = reverse_lazy('produto-list')


class ProdutoUpdateView(UpdateView):
    model = Produto
    template_name = 'produto_form.html'
    fields = ['nome', 'descricao', 'valor']
    success_url = reverse_lazy('produto-list')


class ProdutoDeleteView(DeleteView):
    model = Produto
    template_name = 'produto_confirm_delete.html'
    success_url = reverse_lazy('produto-list')