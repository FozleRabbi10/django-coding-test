from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView
from product.models import Variant, Product, ProductVariant
from django.core.paginator import Paginator


class CreateProductView(generic.CreateView):
    model = Product
    template_name = 'products/create.html'
    fields = "__all__"
    success_url = '/product/list/'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True

        context['variants'] = list(variants.all())
        return context


class ProductList(ListView):

    model = Product
    context_object_name = 'product_list'
    template_name = 'products/list.html'
    paginate_by = 2

    def get_queryset(self):
        filter_string = {}
        print(self.request.GET)
        for key in self.request.GET:
            if self.request.GET.get(key):
                filter_string[key] = self.request.GET.get(key)
        return Product.objects.filter(**filter_string)

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context['variants'] = Variant.objects.all()

        context['search'] = 'search'

        # context['request'] = ''
        # if self.request.GET:
        #     context['request'] = self.request.GET['title__icontains']

        return context
