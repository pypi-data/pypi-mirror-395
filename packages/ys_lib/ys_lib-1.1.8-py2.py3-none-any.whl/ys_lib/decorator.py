# -*- coding: utf-8 -*-
import asyncio
import functools
from loguru import logger


def aioretry(
        max_retries: int = 1,
        retry_interval: float = 1.0,
        log: bool = True
):
    """异步重试装饰器"""

    def decorator(func):
        @functools.wraps(func)
        async def decorated(*args, **kwargs):
            for retry in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if retry == max_retries - 1:
                        if log:
                            logger.error(f'{max_retries}次重试失败: {args} {kwargs}')
                        raise e
                    else:
                        if log:
                            logger.error(f'[{e.__class__.__name__}]{e}')
                        await asyncio.sleep(retry_interval)

        return decorated

    return decorator
