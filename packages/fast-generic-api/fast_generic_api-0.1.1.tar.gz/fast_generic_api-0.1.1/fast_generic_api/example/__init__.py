# -*- coding: utf-8 -*-
# @Time    : 2025/12/8 下午1:36
# @Author  : fzf
# @FileName: __init__.py
# @Software: PyCharm
from fastapi import FastAPI

from .example import router as example_route

# 创建应用实例
app = FastAPI(
    title="Fast Generic API",
    description="你的自动化框架的 FastAPI 服务",
    version="0.1.0"
)
# 注册路由
app.include_router(example_route)

import uvicorn

uvicorn.run(app, host="0.0.0.0", port=8000,
            # reload=True  # 热重载，非常适合开发
            )
