from django.urls import path, re_path
from product import views
from rest_framework.urlpatterns import format_suffix_patterns




app_name = "product"
urlpatterns = [

    path("cart/", views.cartView.as_view(), name='show'),
    path("", views.beddingCatrgory.as_view(), name='bedding'),
    path("product", views.addToCart.as_view(), name='add'),
    path("Summary/", views.Submitted_View.as_view(), name='summary'),
    path("antiques/", views.antiquesCategory.as_view(), name='antique'),
    path('<int:pk>/itemshow/', views.productDetails.as_view(), name = 'item' ),
    path("upload/", views.upload.as_view(), name='upload'),
    path("productApi/", views.productAPI.as_view(), name='productapi'),



]
urlpatterns = format_suffix_patterns(urlpatterns)