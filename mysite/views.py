from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from .cache import caches
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.views.decorators.cache import cache_page

from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data
from blog.models import Blog




def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    # 获取近7日每日的阅读数量
    dates, read_nums = get_seven_days_read_data(blog_content_type)

    # 获取7天热门博客的缓存数据
    '''
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = cache.get_7_days_hot_blogs()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3600)
    '''
    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    # 获取缓存数据
    context['hot_blogs_for_7_days'] = caches['seven_days_hot_blogs'].get_cache()
    return render(request, 'home.html', context)


def search(request):
    search_words = request.GET.get('wd', '').strip()
    # 分词 按空格 & | ~ 与或非
    condition = None
    for word in search_words.split(' '):
        # 筛选搜索 合并搜索词 或的关系 Q对象实现复杂搜索
        if condition is None:
            condition = Q(title__icontains=word)
        else:
            condition = Q(title__icontains=word)
    search_blogs = []
    # 部分匹配 忽略大小写
    if condition is not None:
        search_blogs = Blog.objects.filter(condition)
    # 分页
    paginator = Paginator(search_blogs, 7)
    page_num = request.GET.get('page', 1)  # 获取url的页面参数（GET请求）
    page_of_blogs = paginator.get_page(page_num)

    context = {}
    context['search_words'] = search_words
    # context['search_blogs'] = search_blogs
    context['search_blogs_count'] = search_blogs.count()
    context['page_of_blogs'] = page_of_blogs
    return render(request, 'search.html', context=context)
