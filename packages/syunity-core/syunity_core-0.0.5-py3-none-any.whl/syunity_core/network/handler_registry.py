from typing import Callable, Dict, Optional


class HandlerRegistry:
    """
    全局业务函数注册中心
    作用：解耦业务函数的定义与调用，允许通过字符串名称查找函数。
    """
    _handlers: Dict[str, Callable] = {}

    @classmethod
    def register(cls, name: str = None):
        """
        [装饰器] 将函数注册到内存表中
        :param name: 注册名，如果不填则默认使用函数名
        """

        def decorator(func: Callable):
            # 获取注册用的 key
            key = name if name else func.__name__

            if key in cls._handlers:
                # 这里使用 print 或 logger 都可以，考虑到 core 依赖关系，简单 print 即可
                print(f"⚠️ [Registry] Warning: Handler '{key}' is being overwritten!")

            cls._handlers[key] = func
            return func

        return decorator

    @classmethod
    def get_handler(cls, name: str) -> Optional[Callable]:
        """根据名称获取函数对象"""
        return cls._handlers.get(name)

    @classmethod
    def get_all(cls) -> Dict[str, Callable]:
        """获取所有已注册函数"""
        return cls._handlers