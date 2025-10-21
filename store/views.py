from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category

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
        product_count = products.count()
    else: # Nếu không chọn danh mục nào
        # Lấy tất cả sản phẩm trong cửa hàng đang có sẵn (is_available=True).
        products = Product.objects.all().filter(is_available = True)
        product_count = products.count()

    # Chuẩn bị dữ liệu để gửi sang template:
    context = {
        'products': products,
        'product_count': product_count,
    }
    # Dữ liệu này sẽ được truyền vào file HTML store/store.html
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug = category_slug, slug=product_slug)
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
    }
    return render(request, 'store/product_detail.html', context)