from django.contrib import admin
from .models import Category

# Tạo một lớp quản trị tuỳ chỉnh để điều chỉnh cách hiển thị model Category trong trang admin
class CategoryAdmin(admin.ModelAdmin):
    # Khi nhập category_name, trường slug sẽ tự động sinh ra dựa trên tên đó (ví dụ: "Điện thoại" → "dien-thoai").
    prepopulated_fields = {'slug': ('category_name', )}
    # hiển thị hai cột này trong bảng danh sách của trang admin.
    list_display = ('category_name', 'slug')

# Đăng ký model Category vào trang quản trị Django, sử dụng lớp cấu hình CategoryAdmin.
admin.site.register(Category, CategoryAdmin)

# Kết quả: khi vào /admin/,thấy mục “Categories”, có bảng gồm 2 cột: category_name và slug.