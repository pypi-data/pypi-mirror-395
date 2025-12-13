from __future__ import absolute_import
import sys
import os

from typing import Dict, List, Any
from fastapi.responses import JSONResponse

from mctech_core import Configure

SECURE_PROP_NAMES = [
    'admin',
    'user',
    'password',
    'pass',
    'pwd',
    'login',
    'username',
    'secret',
    'token',
    'aes'
]


def _prapare_object(src: Any, target: Any, prefix: str):
    if hasattr(src, '__json__'):
        src = src.__json__()

    if isinstance(src, Dict):
        for name, value in src.items():
            # 可能含有敏感信息的字符串属性
            # 递归处理
            _prapare_object(value, target, prefix + name + '.')
    elif isinstance(src, List):
        for i in range(0, len(src)):
            item_value = src[i]
            _prapare_object(item_value, target, f"{prefix}[{i}].")
    else:
        if prefix.endswith('.'):
            prefix = prefix[:-1]

        lower_prefix = prefix.lower()
        match = next(filter(lambda p: p in lower_prefix, SECURE_PROP_NAMES), None)
        if match and isinstance(src, str):
            # hide secure details
            src = '*******'
        target[prefix] = src


def create_env_route(configure: Configure):
    async def health():
        config = {}
        configureSources = {}
        environment = {}
        args = {}
        _prapare_object(configure.get_config(''), config, '')
        # prapareObject(configure.getConfigSourceInfo(), configureSources, '')
        _prapare_object(dict(os.environ), environment, '')
        _prapare_object(list(sys.argv), args, '')

        result = {
            'config': config,
            'configureSources': configureSources,
            'environment': environment,
            'args': args
        }
        return JSONResponse(result)
    return health
