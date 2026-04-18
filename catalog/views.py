from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Product
from .forms import ProductForm

# Общедоступный список продуктов
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

# Детальный просмотр (доступен только авторизованным)
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'

# Создание продукта (только авторизованные, владелец назначается автоматически)
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        product = form.save(commit=False)   # не сохраняем сразу
        product.owner = self.request.user   # назначаем владельца
        product.save()                      # теперь сохраняем
        return super().form_valid(form)     # редирект

# Редактирование продукта (только владелец или модератор)
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return user == product.owner or user.has_perm('catalog.can_unpublish_product')

# Удаление продукта (владелец или модератор с правом удаления)
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return user == product.owner or user.has_perm('catalog.delete_product')

# Переключение статуса публикации (только модераторы)
class ProductTogglePublishView(LoginRequiredMixin, UserPassesTestMixin, RedirectView):
    pattern_name = 'catalog:product_detail'

    def test_func(self):
        return self.request.user.has_perm('catalog.can_unpublish_product')

    def get_redirect_url(self, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        product.is_published = not product.is_published
        product.save()
        return reverse(self.pattern_name, kwargs={'pk': product.pk})
