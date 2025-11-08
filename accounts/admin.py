from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


# UserAdmin là class có sẵn của Django cung cấp sẵn các chức năng quản lý user trong admin site.
# Khi kế thừa nó, ta có thể tuỳ chỉnh giao diện hiển thị và hành vi của model Account trong trang /admin.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')

    list_display_links = ('email', 'first_name', 'last_name') # các trường có thể click vào để xem chi tiết
    readonly_fields = ('last_login', 'date_joined') # các trường chỉ đọc
    ordering = ('-date_joined',) # sắp xếp theo thuộc tính, - là giảm dần
    
    # Các tùy chọn ko sử dụng
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# Đăng ký model với admin
admin.site.register(Account, AccountAdmin)
# Đưa model Account (và class AccountAdmin) vào trang admin.
# Nếu không có dòng này thì Account sẽ không xuất hiện trong Django admin.