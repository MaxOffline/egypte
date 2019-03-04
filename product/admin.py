from django.contrib import admin
from product.models import product
from product import images_model
admin.site.register(product)
admin.site.register(images_model.productImages)
