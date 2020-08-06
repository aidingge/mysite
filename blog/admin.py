from django.contrib import admin
from .models import BlogType, Blog


@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'blog_type', 'author', 'get_read_num', 'created_time', 'last_updated_time')
    list_display_links = ('title',)   # 设置需要添加<a>标签的字段
    list_filter = ('blog_type', 'author', 'created_time')

    # 限制用户权限，只能看到自己编辑的文章 通过当前登录的用户过滤显示的数据
    def get_queryset(self, request):
        qs = super(BlogAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)


admin.site.site_title = '博客后台管理'
admin.site.site_header = '博客后台管理系统'

