# -*- coding: utf-8 -*-
# @Time    : 2025/12/8 下午2:24
# @Author  : fzf
# @FileName: filter.py
# @Software: PyCharm
from tortoise.queryset import QuerySet
from typing import Dict, Any, Callable


class FilterSet:
    """
    基础 Tortoise FilterSet
    - 支持自定义方法过滤
    - 支持精确匹配 / 多选 __in
    - 自动排除 offset、limit 等分页参数
    """

    model = None
    filters: Dict[str, Callable] = {}  # 自定义过滤方法
    exclude_fields = {"offset", "limit"}  # 自动排除字段

    def __init__(self, queryset: QuerySet, data: Dict[str, Any]):
        if self.model is None:
            raise ValueError("model must be defined")
        self.queryset = queryset
        self.data = data or {}

    def _apply_filter(self, qs: QuerySet, field: str, value: Any) -> QuerySet:
        """根据字段和值应用过滤"""
        if field in self.filters:
            return self.filters[field](qs, field, value)

        if value is None:
            return qs

        # 自动处理多选字符串
        if isinstance(value, str) and ',' in value:
            return qs.filter(**{f"{field}__in": value.split(',')})

        return qs.filter(**{field: value})

    def qs(self) -> QuerySet:
        """返回过滤后的 QuerySet，自动跳过 exclude_fields"""
        qs = self.queryset
        for field, value in self.data.items():
            if field in self.exclude_fields:
                continue
            qs = self._apply_filter(qs, field, value)
        return qs
