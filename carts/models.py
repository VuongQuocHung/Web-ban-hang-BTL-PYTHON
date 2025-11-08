from django.db import models
from store.models import Product, Variation
# Create your models here.

class Cart(models.Model): # giỏ hàng
    cart_id = models.CharField(max_length=200, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    # Khi in đối tượng Cart, nó sẽ hiện cart_id.
    # Dùng cho mục đích hiển thị trong admin.

# Hiểu đơn giản:
# CartItem = 1 sản phẩm trong giỏ + số lượng + các biến thể (variations)
# Bạn thêm vào giỏ Áo thun:
# Màu: Đỏ
# Size: M
# Thì CartItem đó cần lưu cả 2 thông tin biến thể.
# CartItem (Áo thun, quantity = 1)
#  ├── Variation(color=Red)
#  └── Variation(size=M)
class CartItem(models.Model): # từng món hàng trong giỏ hàng
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # Mỗi CartItem gắn với 1 sản phẩm (Product)
    variations = models.ManyToManyField(Variation, blank = True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE) 
    # Mỗi CartItem thuộc 1 Cart (giỏ hàng).
    # Một Cart có thể chứa nhiều CartItem → quan hệ 1-nhiều.
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity
    
    def __unicode__(self):
        return self.product