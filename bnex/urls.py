"""
URL configuration for bnex project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from product.views import ProdutoListView, ProdutoDetailView, ProdutoCreateView, ProdutoUpdateView, ProdutoDeleteView


urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', ProdutoListView.as_view(), name='produto-list'),
    path('product/<int:pk>/', ProdutoDetailView.as_view(), name='produto-detail'),
    path('product/add/', ProdutoCreateView.as_view(), name='produto-add'),
    path('product/<int:pk>/update/', ProdutoUpdateView.as_view(), name='produto-update'),
    path('product/<int:pk>/delete/', ProdutoDeleteView.as_view(), name='produto-delete'),
]
