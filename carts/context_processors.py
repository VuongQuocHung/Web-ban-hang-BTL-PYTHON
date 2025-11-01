from .models import Cart, CartItem
from .views import _cart_id

def counter(reuqest): # đếm số lượng sản phẩm trong giỏ hàng
    cart_count = 0
    if 'admin' in reuqest.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id= _cart_id(reuqest))
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    
    return dict(cart_count=cart_count)
            
