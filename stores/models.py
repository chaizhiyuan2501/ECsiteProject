from django.db import models
from accounts.models import Users

# 商品の種類
class ProductTypes(models.Model):
    name = models.CharField(max_length=1000)

    class Meta:
        db_table = 'product_types'
    
    def __str__(self):
        return self.name

# 生産者
class Manufacturers(models.Model):
    name = models.CharField(max_length=1000)

    class Meta:
        db_table = 'manufacturers'
    
    def __str__(self):
        return self.name

class ProductsManager(models.Manager):
    
    def reduce_stock(self,cart):
        for item in cart.cartitems_set.all():
            update_stock = item.product.stock - item.quantity
            item.product.stock = update_stock
            item.product.save()

#商品
class Products(models.Model):
    name = models.CharField(max_length=1000)
    price = models.IntegerField()
    stock = models.IntegerField()   # 在庫数
    product_type = models.ForeignKey(
        ProductTypes,on_delete=models.CASCADE
        )
    manufacturers = models.ForeignKey(
        Manufacturers,on_delete=models.CASCADE
        )
    objects = ProductsManager()
    
    class Meta:
        db_table = "products"

    def __str__(self):
        return self.name

# 商品の画像
class ProductPictures(models.Model):
    picture = models.FileField(upload_to="product_pictures/")
    product = models.ForeignKey(
        Products,on_delete=models.CASCADE
    )
    order = models.IntegerField()   # 写真が表示する順番
    
    class Meta:
        db_table = "product_pictures"
        ordering = ["order"]

    def __str__(self):
        return self.product.name + ":" +str(self.order)

# カート
class Carts(models.Model):
    user = models.OneToOneField(
        Users,
        on_delete=models.CASCADE,
        primary_key=True
    )
    
    class Meta:
        db_table = "carts"

class CartItemManager(models.Manager):
    
    def save_item(self,product_id,quantity,cart):
        c = self.model(quantity=quantity,product_id=product_id,cart=cart)
        c.save()

# カートの量
class CartItems(models.Model):
    #数量
    quantity = models.PositiveBigIntegerField()
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
    )
    cart = models.ForeignKey(
        Carts,on_delete=models.CASCADE
    )
    objects = CartItemManager()
    
    class Meta:
        db_table = "cart_items"
        unique_together = [["product","cart"]]


class Addresses(models.Model):
    zip_code = models.CharField(max_length=8)
    prefecture = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        )

    class Meta:
        db_table = "addresses"
        unique_together = [
            ["zip_code","prefecture","address","user"]
            ]

    def __str__(self):
        return f"{self.zip_code}{self.prefecture} {self.address}"

class OrdersManager(models.Manager):
    
    def insert_cart(self, cart:Carts, address, total_price):
        return self.create(
            total_price=total_price,
            address=address,
            user=cart.user,
        )

class Orders(models.Model):
    total_price = models.PositiveIntegerField()
    address = models.ForeignKey(
        Addresses,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    objects = OrdersManager()
    
    class Meta:
        db_table = "orders"

class OrderItemsManager(models.Manager):
    #商品を作成
    def insert_cart_items(self, cart, order):
        for item in cart.cartitems_set.all():
            self.create(
                quantity=item.quantity,
                product=item.product,
                order=order
            )

class OrderItems(models.Model):
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(
        Products,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    order = models.ForeignKey(
        Orders,
        on_delete=models.CASCADE
    )
    objects = OrderItemsManager()
    
    class Meta:
        db_table = "order_items"
        unique_together = [["product","order"]]