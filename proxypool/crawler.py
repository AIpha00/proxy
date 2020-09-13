import logging


## 日志应该新起一个日志类文件来负责日志的输出
# 通过下面的方式进行简单配置输出方式与日志级别
# log_name = 'log/logging.log'
# fh = logging.FileHandler(encoding='utf-8', mode='a+', filename=log_name)
# logging.basicConfig(handlers=[fh], format='[%(asctime)s %(levelname)s]<%(process)d> %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)


class ProxyMetaclass(type):
    '''
    使用元类的知识，动态的在Crawler类创建之前先创建一个元类，这个元类需要做的就是统计Crawler这个类的所有方法
    '''
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            # 所有的代理获取都以crawl开头，方便管理和统一调用，python的元类， 元类是在初始化实例类之前初始化的，先初始化元类在通过元类去初始化实例类
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        print('name', name)
        print('bases', bases)
        print('attrs', attrs)
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理：{}'.format(proxy))
            proxies.append(proxy)
        return proxies

    def crawl_getProxy(self):
        """
        编写获取代理的代码
        :return: 获取到的代理
        """
        return ['127.0.0.1:22222']
