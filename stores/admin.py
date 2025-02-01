from django.contrib import admin
from .models import(
    ProductTypes,Products,ProductPictures,
    Manufacturers
)

# Register your models here.
admin.site.register(
    [ProductTypes, ProductPictures, Products, 
     Manufacturers]
    )