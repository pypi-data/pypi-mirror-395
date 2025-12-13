# -*- coding: utf-8 -*-
# @Time    : 2025/12/8 下午12:50
# @Author  : fzf
# @FileName: main.py
# @Software: PyCharm
from fastapi import APIRouter
from generics import GenericAPIView, CustomViewSet

# 创建路由
router = APIRouter(prefix="/api", tags=["API示例"])


class ExampleViewSet(CustomViewSet,
                     GenericAPIView):
    router = router
    prefix = "/examples"
    queryset = None
    filter_fields = []
    ordering = ["created_at"]
    loop_uuid_field = "uuid"
    serializer_class = None  # ✅ 列表/详情默认序列化器
    serializer_create_class = None
    serializer_update_class = None
    pagination_class = None
    filter_class = None
    permissions = []
