
from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.

class Product(models.Model):
    product_name        = models.CharField(max_length=200, unique=True)
    slug                = models.SlugField(max_length=200, unique=True)
    description         = models.TextField(max_length=500, blank=True)
    price               = models.IntegerField()
    images              = models.ImageField(upload_to='photos/products')
    stock               = models.IntegerField()
    is_available        = models.BooleanField(default=True)
    category            = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date        = models.DateTimeField(auto_now_add=True)
    modified_date       = models.DateTimeField(auto_now=True)

    def get_url(self): # tạo URL từ tên route (name) thay vì viết URL thủ công
        return reverse('product_detail', args=[self.category.slug, self.slug])
        # VD: reverse('product_detail', args=['electronics', 'iphone-15'])
        # /electronics/iphone-15/

    def __str__(self):
        return self.product_name

# tạo custom manager dùng để tạo các hàm lọc nhanh cho model Variation
# Custom Manager (hay còn gọi là manager tùy chỉnh) là một lớp Manager do ta tự định nghĩa
class VariationManager(models.Manager): # Manager là lớp cung cấp các phương thức truy vấn cơ sở dữ liệu như .filter(), .all(), .get()
    def colors(self):
        return super(VariationManager, self).filter(variation_category = 'color', is_activate=True)
    
    def size(self):
        return super(VariationManager, self).filter(variation_category = 'size', is_activate=True)
    
variation_category_choice = (
    ('color', 'Màu sắc'),
    ('size', 'Kích thước'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    # Mỗi Variation thuộc về 1 sản phẩm (VD: áo A có size M, L; color Red, Blue,…)

    variation_category = models.CharField(max_length=100, choices = variation_category_choice)
    # Loại variation (color hoặc size). Không cho phép nhập linh tinh.
    
    variation_value = models.CharField(max_length=100)
    # Giá trị của variation (VD: Red, Blue, M, L).

    is_activate = models.BooleanField(default=True)
    created_dated = models.DateTimeField(auto_now=True)

    objects = VariationManager() # Gán custom manager để gọi colors() và size() dễ dàng.
    
    def __str__(self):
        return self.variation_value