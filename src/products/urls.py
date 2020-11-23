
from django.conf.urls import url
from products.views import ProductListView,ProductDetailSlugView

# product_list_view
# ,product_detail_view
# ,ProductDetailView,
# ProductFeaturedListView, 
# ProductFeaturedDetailView,)
urlpatterns = [

    url(r'^$',ProductListView.as_view()),
    url(r'^(?P<slug>[\w-]+)/$',ProductDetailSlugView.as_view()),    
]

