from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.models import Cart, CartItem
from django.db.models import Q
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# category_slug là tham số tùy chọn (mặc định = None), dùng để xác định danh mục nào đang được
# Ví dụ URL:
# /store/ → xem tất cả sản phẩm
# /store/shirts/ → xem sản phẩm trong danh mục shirts
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None: # nếu người dùng chọn danh mục
        categories = get_object_or_404(Category, slug=category_slug) # tìm danh mục có slug tương ứng, nếu ko tìm thấy -> 404
        products = Product.objects.filter(category = categories, is_available = True) # lấy tất cả sản phẩm thuộc danh mục đó và còn hàng (is_available=True)
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    else: # Nếu không chọn danh mục nào
        # Lấy tất cả sản phẩm trong cửa hàng đang có sẵn (is_available=True).
        products = Product.objects.all().filter(is_available = True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    # Chuẩn bị dữ liệu để gửi sang template:
    context = {
        'products': paged_products,
        'product_count': product_count,

    }
    # Dữ liệu này sẽ được truyền vào file HTML store/store.html
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug = category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id= _cart_id(request), product = single_product).exists()
        
    
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    products = []
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)