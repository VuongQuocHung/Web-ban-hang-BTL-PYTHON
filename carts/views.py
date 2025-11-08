from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Variation
from .models import Cart, CartItem
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

# lấy ra hoặc tạo ra một ID giỏ hàng (cart_id) dựa vào phiên làm việc (session) của người dùng.
def _cart_id(request):
    cart = request.session.session_key # Lấy session id hiện tại của user

    # Mỗi người truy cập website đều có một session.
    # session_key chính là ID phiên đó.
    # Nếu user chưa có session (lần đầu vào web), giá trị sẽ là None

    if not cart:
        cart = request.session.create() # Tạo session mới nếu chưa có (session_key = None)

    return cart  # Trả lại session_id để dùng làm cart_id

# Hàm nút + tăng số lượng sản phẩm và thêm vào giỏ hàng
# Nhận product_id từ nút “Add to Cart”.
# Lấy sản phẩm tương ứng.
# Lấy các option/variation (color, size…) từ form nếu có.
# Kiểm tra session: Lấy giỏ hàng của người dùng hoặc tạo mới.
# Kiểm tra giỏ hàng:
    # Nếu sản phẩm đã có → tăng quantity.
    # Nếu chưa có → tạo cart item mới với quantity = 1.
# Lưu các thay đổi vào DB.
# Chuyển hướng về trang giỏ hàng.

def add_cart(request, product_id): # product_id là ID sản phẩm mà người dùng bấm nút "Add to Cart".
    product = Product.objects.get(id = product_id) # Lấy sản phẩm dựa theo product_id
    product_variation = []
    if request.method == 'POST': # Nếu form gửi lên có lựa chọn như color / size, vòng lặp lấy từng key=value
        for item in request.POST:
            key = item
            value = request.POST[key]
            
            try:
                variation = Variation.objects.get(product = product, variation_category__iexact = key, variation_value__iexact = value)
                product_variation.append(variation)
            except:
                pass
        
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request)) # Lấy giỏ hàng theo cart_id lưu trong session
    except Cart.DoesNotExist: # nếu giỏ hàng ko tồn tại thì tạo mới
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    # Nếu sản phẩm đã có trong giỏ -> tăng quantity thêm 1.
    try: 
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1 # cart_item.quantity = cart_item.quantity + 1
        cart_item.save()
    # Nếu sản phẩm chưa có trong giỏ -> tạo mới 1 cart item với số lượng = 1.
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    return redirect('cart') # chuyển hướng về trang giỏ hàng

# nút - giảm số lượng sản phẩm
def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

# xóa 1 sản phẩm trong giỏ hàng
def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')

def cart(request, total = 0, quantity = 0, cart_items = None):
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart, is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    return HttpResponse('checkout')
    