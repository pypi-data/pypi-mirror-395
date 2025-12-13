# -*- coding: utf-8 -*-
# @Time    : 2025/12/8 下午5:41
# @Author  : fzf
# @FileName: main.py
# @Software: PyCharm
# main.py
from fastapi import APIRouter, FastAPI
from fast_generic_api.generics import GenericAPIView, CustomViewSet
from fast_generic_api.core.pagination import LimitOffsetPagination
from tortoise.contrib.fastapi import register_tortoise

from model import Item
from serializers import ItemSerializer, ItemCreateSerializer, ItemUpdateSerializer

import uvicorn

router = APIRouter(prefix="/api", tags=["API示例"])


class ItemViewSet(CustomViewSet, GenericAPIView):
    router = router
    prefix = "/items"
    queryset = Item
    filter_fields = []
    ordering = ["created_at"]
    lookup_field = "id"

    serializer_class = ItemSerializer
    serializer_create_class = ItemCreateSerializer
    serializer_update_class = ItemUpdateSerializer
    pagination_class = LimitOffsetPagination

app = FastAPI(
    title="Fast Generic API",
    description="你的自动化框架的 FastAPI 服务",
    version="0.1.0"
)

# 注册路由
app.include_router(router)

# 注册数据库
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["model"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
