from django.shortcuts import render
from products.models import Product
from django.views.generic import ListView

# Create your views here.
class SearchProductListView(ListView):
    template_name="search/view.html"

    def get_queryset(self,*args,**kwargs):
        request=self.request
        method_dict=request.GET
        query=method_dict.get('q',None)
        if query is not None:
            return Product.objects.filter(title__icontains=query)
        return Product.objects.featured()
