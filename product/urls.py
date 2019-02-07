from django.urls import path, re_path
from product import views



app_name = "product"
urlpatterns = [

    path("cart/", views.showProduct.as_view(), name='show'),
    path("", views.beddingView.as_view(), name='bedding'),
    path("product", views.addToCart.as_view(), name='add'),
    path("Summary/", views.Submitted_View.as_view(), name='summary'),
    path("antiques/", views.Antiques.as_view(), name='antique'),
    path('<int:pk>/itemshow/', views.itemView.as_view(), name = 'item' ),


]
