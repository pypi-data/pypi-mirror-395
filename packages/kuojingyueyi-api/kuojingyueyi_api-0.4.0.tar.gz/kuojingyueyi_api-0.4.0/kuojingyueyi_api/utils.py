import os
import json
import time
import datetime
import random
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import functools

import requests
import requests.adapters
from requests.exceptions import ConnectTimeout, ConnectionError, ProxyError
from loguru import logger

from .exception import NeedLoginException

RETRY = requests.adapters.Retry(
    total=3,  # 允许的重试总次数，优先于其他计数
    read=3,  # 重试读取错误的次数
    connect=3,  # 重试多少次与连接有关的错误（请求发送到远程服务器之前引发的错误）
    backoff_factor=0.3,  # 休眠时间： {backoff_factor} * (2 ** ({重试总次数} - 1))
    status_forcelist=[403, 408, 500, 502, 504],  # 强制重试的状态码
)

# 重试次数
DEFAULT_RETRIES = 2


def dict_to_pretty_string_py(the_dict):
    if not the_dict:
        return "{}"
    return json.dumps(the_dict, sort_keys=True, indent=4, separators=(',', ': '))


def need_login(func):
    """
    装饰器。作用于 :class:`.DouYinAPI` 中的某些方法，
    强制它们必须在登录状态下才能被使用。
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.is_login():
            return func(self, *args, **kwargs)
        else:
            raise NeedLoginException(func.__name__)

    return wrapper


def random_sleep(start=1, end=3, debug=True):
    """
    随机延迟，因为如果你访问了很多页面，你的 ip 可能会被封。
    """
    sleep_time = random.randint(start, end)
    if debug:
        print('随机延迟：%s 秒......' % sleep_time)
    time.sleep(sleep_time)


def get_now(fmt="%Y-%m-%d %H:%M:%S"):
    """
    获取当前日期和时间
    :return: 格式 2018-11-28 15:03:08
    """
    return datetime.datetime.now().strftime(fmt)


def second_to_time_str(seconds):
    """
    秒转换为人类阅读的时间显示，用来显示已用时间
    例如：'1小时1分1.099秒'
    """
    time_str = ''
    hour = '%01d小时' % (seconds / 3600)
    minute = '%01d分' % ((seconds % 3600) / 60)

    if hour != '0小时':
        time_str += hour

    if minute != '0分':
        time_str += minute

    # seconds
    time_str += '%01d.%03d秒' % (seconds % 60, (seconds % 1) * 1000)

    return time_str


class Timer:
    """
    计时器，可以当装饰器或者用 with 来对代码计时

    # 例子：
        >>> import time
        >>> def papapa(t):
        >>>     time.sleep(t)
        >>> with Timer() as timer:
        >>>     papapa(1)
        运行时间 1.000 秒
        >>> @Timer.time_it
        >>> def papapa(t):
        >>>     time.sleep(t)
        >>> papapa(1)
        papapa 运行时间 1.001 秒
    """

    def __init__(self, name=None):
        self.start = time.time()

        # 我们添加一个自定义的计时名称
        if isinstance(name, str):
            self.name = name + ' '
        else:
            self.name = ''

        print(f'{get_now()} 开始运行 {self.name}', )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.running_time()
        return exc_type is None

    @staticmethod
    def time_it(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            print(f'{get_now()} 开始运行 {func.__name__}', )
            result = func(*args, **kwargs)
            print(f'{get_now()} 结束运行 {func.__name__}，运行时间 {second_to_time_str(time.time() - start)}', )
            return result

        return wrapper

    def running_time(self):
        stop = time.time()
        cost = stop - self.start
        print(f'{get_now()} 结束运行 {self.name}，运行时间 {second_to_time_str(cost)}', )


class BaseClient:
    def __init__(self, retry=None, retries=None):
        """
        API接口的基础类

        # 来自
        >>> from spider_utils.client import BaseSpiderClient

        """
        self._session = requests.session()

        # 默认超时时间 https://2.python-requests.org//zh_CN/latest/user/advanced.html#timeout
        self.timeout = 5

        # 重试次数
        if retries is None:
            self.retries = DEFAULT_RETRIES
        else:
            self.retries = retries

        self.params = {}
        self.parse_data = {}
        self.load_count = 0

        # 删除SSL验证
        self._session.verify = False
        urllib3.disable_warnings(InsecureRequestWarning)

        # 添加会话自动重试
        if retry is None:
            adapter_with_retry = requests.adapters.HTTPAdapter(max_retries=RETRY)
        else:
            adapter_with_retry = requests.adapters.HTTPAdapter(max_retries=retry)
        self._session.mount('http://', adapter_with_retry)
        self._session.mount('https://', adapter_with_retry)

    def set_proxy(self, proxy):
        """ 设置 http 和 https 代理或者 sock5代理（requests 已经可以支持 socks 代理）

        因为由 :any:`SpiderClient` 生成的爬虫类对象和本对象使用同一session，
        所以设置代理后，对所有由当前对象生成的爬虫对象均会使用设置的代理。

        ..  note:: 如果需要使用 socks 代理，需要安装 pysocks

            ``sudo pip install pysocks>=1.5.6,!=1.5.7``

        :param str|unicode proxy: 形如 'http://user:pass@10.10.1.10:3128/'
          或者 'socks5://user:pass@host:port'。
          传入 None 表示清除代理设置。
        :return: None
        """
        if proxy is None:
            self._session.proxies.clear()
        else:
            self._session.proxies.update({'http': proxy, 'https': proxy})

    def set_headers(self, headers):
        """
        设置 headers（全局），如果是 None，清除数据

        :return: None
        """
        if headers is None:
            self._session.headers.clear()
        else:
            self._session.headers.update(headers)

    def get_headers(self):
        """
        获取 headers（全局）

        :return: Dict(headers)
        """
        return dict(self._session.headers)

    def set_cookies(self, cookies):
        """
        设置 cookies（全局），如果是 None，清除数据

        :return: None
        """
        if cookies is None:
            self._session.cookies.clear()
        else:
            self._session.cookies.update(cookies)

    def get_cookies(self):
        """
        获取 cookies（全局）

        :return: Dict(cookies)
        """
        return requests.utils.dict_from_cookiejar(self._session.cookies)

    def set_params(self, params):
        """
        设置 params（全局），如果是 None，清除数据

        :return: None
        """
        if params is None:
            self.params = {}
        else:
            self.params.update(params)

    def get(self, url, **kwargs):
        r"""发送GET请求。 返回响应对象。

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        kwargs.setdefault('timeout', self.timeout)

        # 合并 params
        params = dict(self.params)
        if 'params' in kwargs:
            params.update(kwargs['params'])
            del kwargs['params']

        return self._session.get(url, params=params, **kwargs)

    def download(self, url, dst, **kwargs):
        """
        下载文件
        """

        req = self.get(url, **kwargs)

        with open(dst, 'ab') as f:
            f.write(req.content)

        file_size = os.path.getsize(dst)
        # 检查文件大小判断是否下载成功
        if file_size >= int(req.headers['content-length']):
            return file_size
        else:
            os.remove(dst)

    def load_page(self, url, **kwargs):

        self.parse_data = {}
        self.load_count += 1
        logger.info(f'[{self.load_count:05}] Starting {url}')

        for i in range(self.retries):
            try:
                r = self.get(url, **kwargs)
                random_sleep()
            except (ConnectTimeout, ConnectionError) as e:
                logger.warning(str(e))
            else:
                return r

    def api(self, method, url, params=None, data=None):
        """
        开发时用的测试某个 API 返回的 JSON 用的便捷接口。

        :param str|unicode method: HTTP 方式， GET or POST or OPTION, etc。
        :param str|unicode url: API 地址。
        :param dict params: GET 参数。
        :param dict data: POST 参数。
        :return: 访问结果。
        :rtype: request.Response
        """
        return self._session.request(method, url, params, data)

    def __repr__(self):
        repr_info = [f"<------------------------------ {type(self).__name__} ------------------------------>",
                     f"timeout = {self.timeout}",
                     f"headers = {dict_to_pretty_string_py(self.get_headers())}",
                     f"cookies = {dict_to_pretty_string_py(self.get_cookies())}",
                     f"params = {dict_to_pretty_string_py(self.params)}",
                     f"<------------------------------ {type(self).__name__} ------------------------------>"]
        return '\n'.join(repr_info)
