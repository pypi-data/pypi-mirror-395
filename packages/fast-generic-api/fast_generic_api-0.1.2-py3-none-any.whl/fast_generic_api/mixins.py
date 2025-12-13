# -*- coding: utf-8 -*-
# @Time    : 2025/12/8 下午12:49
# @Author  : fzf
# @FileName: mixins.py
# @Software: PyCharm
from typing import Any

from fastapi import Request, Body
from fast_generic_api.core import status
from fast_generic_api.core.response import Response


class CreateModelMixin:
    action = "create"

    async def create(self, data=Body(...)):
        """
        通用创建方法
        - request: FastAPI Request 对象
        - data: Pydantic model，自动解析请求体 JSON
        """
        data_dict = self.serialize_input_data(data)
        obj = await self.queryset.create(**data_dict)
        serializer = self.get_serializer(obj)
        return Response(serializer)


class ListModelMixin:
    action = "list"

    async def list(self, request: Request):
        """
        获取对象列表
        - 支持分页
        """
        qs = self.get_queryset()
        # 应用 ordering
        if self.ordering:
            qs = qs.order_by(*self.ordering)
        # 使用过滤器
        if self.filter_class:
            qs = self.filter_class(request, qs)
        # 使用分页器
        if self.pagination_class:
            return Response(await self.pagination_class.get_paginated_response(request, qs, self.get_serializer))
        # 不分页的情况（备用）
        serializer = self.get_serializer(await qs, many=True)
        return Response(serializer)


class RetrieveModelMixin:
    action = "retrieve"

    async def retrieve(self, request: Request, pk: int):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        self.kwargs[lookup_url_kwarg] = pk
        instance = await self.get_object()  # ✅ 注意加 await
        serializer = self.get_serializer(instance)
        return Response(serializer)


class UpdateModelMixin:
    action = "update"

    async def update(self, pk: int, data=Body(...)):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        self.kwargs[lookup_url_kwarg] = pk
        obj = await self.get_object()
        await obj.update_from_dict(self.serialize_input_data(data)).save()
        serializer = self.get_serializer(obj)
        return Response(serializer)


class PartialUpdateModelMixin:
    action = "partial_update"

    async def partial_update(self, pk: int, data=Body(...)):
        """
        部分更新对象
        - 支持部分字段更新
        """
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        self.kwargs[lookup_url_kwarg] = pk
        obj = await self.get_object()
        await obj.update_from_dict(self.serialize_input_data(data)).save()
        serializer = self.get_serializer(obj)
        return Response(serializer)


class DestroyModelMixin:
    action = "destroy"

    async def destroy(self, pk: int):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        self.kwargs[lookup_url_kwarg] = pk
        instance = await self.get_object()
        await self.perform_destroy(instance)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    async def perform_destroy(self, instance):
        await instance.update_from_dict({"is_deleted": True}).save()
