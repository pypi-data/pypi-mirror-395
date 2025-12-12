# industrio/__init__.py
"""industrio - 物联网网关控制库（支持闪烁、常亮及新增硬件）"""

# 全局网关IP变量
ip = None

# 延迟导入，避免循环依赖
def __getattr__(name):
    if name in ["post", "get", "GatewayClient", "blink", "ston"]:
        from .core import post, get, GatewayClient, blink, ston
        globals()[name] = globals().get(name) or locals()[name]
        return globals()[name]
    raise AttributeError(f"module 'industrio' has no attribute '{name}'")

__version__ = "0.2.0"
__all__ = ["post", "get", "GatewayClient", "blink", "ston", "ip", "__version__"]