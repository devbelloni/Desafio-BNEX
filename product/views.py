from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Produto

FIELDS = ["nome", "descricao", "valor"]


class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = "produto_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        term = self.request.GET.get("q", "").strip()
        return queryset.filter(nome__icontains=term) if term else queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "").strip()
        return context


class ProdutoDetailView(LoginRequiredMixin, DetailView):
    model = Produto
    template_name = "produto_detail.html"


class ProdutoCreateView(LoginRequiredMixin, CreateView):
    model = Produto
    template_name = "produto_form.html"
    fields = FIELDS
    success_url = reverse_lazy("produto-list")


class ProdutoUpdateView(LoginRequiredMixin, UpdateView):
    model = Produto
    template_name = "produto_form.html"
    fields = FIELDS
    success_url = reverse_lazy("produto-list")


class ProdutoDeleteView(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = "produto_confirm_delete.html"
    success_url = reverse_lazy("produto-list")
