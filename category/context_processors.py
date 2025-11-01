from .models import Category

def menu_links(request):
    links = Category.objects.all() # Lấy toàn bộ các bản ghi Category từ database.
    return dict(links = links)

# Trả về một dictionary.
# Django sẽ thêm dictionary này vào context của mọi template.
# Nghĩa là trong bất kỳ template nào, bạn có thể dùng:
# {% for link in links %}
#     {{ link.name }}
# {% endfor %}
# mà không cần truyền thủ công qua render().