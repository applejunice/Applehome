import requests
import urllib3
import ssl
from requests.adapters import HTTPAdapter
from urllib3.connectionpool import HTTPSConnectionPool
from urllib3.poolmanager import PoolManager

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 指定域名和 IP 地址
domain = "bubble.freelink.co.jp"
ip_address = "162.159.35.39"


class CustomHTTPSConnectionPool(HTTPSConnectionPool):
    """自定义 HTTPS 连接池，在 SSL 握手时使用正确的 server_hostname"""
    def __init__(self, server_hostname, *args, **kwargs):
        self._server_hostname = server_hostname
        kwargs['assert_hostname'] = False
        kwargs['cert_reqs'] = ssl.CERT_NONE
        super().__init__(*args, **kwargs)
    
    def _new_conn(self):
        """创建新连接，在 SSL 握手时使用正确的 server_hostname"""
        # 调用父类创建连接
        conn = super()._new_conn()
        # 关键：在 SSL 握手之前设置正确的 hostname
        # 这样 SNI 会使用域名而不是 IP
        conn.hostname = self._server_hostname
        return conn


class CustomPoolManager(PoolManager):
    """自定义 PoolManager，创建自定义的 HTTPS 连接池"""
    def __init__(self, server_hostname=None, *args, **kwargs):
        self.server_hostname = server_hostname
        # 移除 server_hostname，因为我们要在连接池中处理
        super().__init__(*args, **kwargs)
    
    def connection_from_url(self, url, **kw):
        """重写以使用自定义的连接池"""
        return super().connection_from_url(url, **kw)
    
    def _new_pool(self, scheme, host, port, **kwargs):
        if scheme == 'https' and self.server_hostname:
            # 创建自定义的 HTTPS 连接池
            return CustomHTTPSConnectionPool(
                server_hostname=self.server_hostname,
                host=host,
                port=port,
                **kwargs
            )
        return super()._new_pool(scheme, host, port, **kwargs)


class CustomHTTPAdapter(HTTPAdapter):
    """自定义适配器，使用自定义的 PoolManager"""
    def __init__(self, server_hostname=None, *args, **kwargs):
        self.server_hostname = server_hostname
        super().__init__(*args, **kwargs)
    
    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        """使用自定义的 PoolManager"""
        self.poolmanager = CustomPoolManager(
            server_hostname=self.server_hostname,
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            **pool_kwargs
        )


# 创建会话并使用自定义适配器
session = requests.Session()
adapter = CustomHTTPAdapter(server_hostname=domain)
session.mount("https://", adapter)

# 使用 IP 地址访问，并在请求头中指定原始域名
url = f"https://{ip_address}/"
headers = {
    "Host": domain
}

# 发送 HTTP GET 请求
response = session.get(url, headers=headers, verify=False)

# 打印返回结果
print("状态码:", response.status_code)
print("\n响应头:")
for key, value in response.headers.items():
    print(f"{key}: {value}")

print("\n响应内容:")
print(response.text)
