# coding:utf-8
import datetime
from django.core.cache import cache
from django.utils import timezone
from django.db.models import Sum
from blog.models import Blog


# 获取和设置缓存的类 其他地方要使用缓存只需要生成该类的实例(key缓存键名，timeout超时时间，get_data_method获取数据的方法)，传入参数调用实例方法即可
# （后面两个参数是调用获取数据方法的参数）
class RedisCache:
    def __init__(self, key, get_data_method, timeout, args=None, kw=None):
        self.key = key
        self.get_data_method = get_data_method
        self.timeout = timeout
        self.args = [] if args is None else args
        self.kw = {} if kw is None else kw

    # 获取缓存
    def get_cache(self):
        data = ''
        try:
            if cache.has_key(self.key):  # 判断是否存在缓存
                data = cache.get(self.key)
            else:
                self.set_cache()
        except Exception as e:
            # 使用缓存出错，可能没有开启redis
            data = self.get_data_method(*self.args, **self.kw)
        finally:
            return data

    # 设置缓存
    def set_cache(self):
        data = self.get_data_method(*self.args, **self.kw)
        cache.set(self.key, data, self.timeout)
        return data


# 获取缓存数据的方法：获取近7日热门博客数据
def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
        .filter(read_details__date__lt=today, read_details__date__gte=date) \
        .values('id', 'title') \
        .annotate(read_num_sum=Sum('read_details__read_num')) \
        .order_by('-read_num_sum')
    return blogs[:7]


# 获取一个缓存字典方便获取，key:缓存的键名 value：缓存的实例
def get_caches():
    # 设置缓存超时时间3小时 实例化
    seven_days_hot_blogs_cache = RedisCache(key='seven_days_hot_blogs',
                                            get_data_method=get_7_days_hot_blogs,
                                            timeout=3 * 60 * 60)
    caches = {}
    # 键：实例化对象 存入字典
    caches[seven_days_hot_blogs_cache.key] = seven_days_hot_blogs_cache
    return caches


# 执行获取缓存管理器，方便使用  在views中使用caches
caches = get_caches()
