# -*- coding: utf-8 -*-
# @Time    : 2025/12/8 下午6:30
# @Author  : fzf
# @FileName: schemas.py
# @Software: PyCharm
from typing import Any
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from tortoise.fields.relational import ManyToManyRelation


class AutoSchemas(BaseModel):
    """基础 BaseModel，提供 `.data` 属性返回 JSON 可序列化内容"""

    model_config = {"from_attributes": True}

    @property
    def data(self) -> Any:
        """返回可直接用于 FastAPI JSONResponse 的 dict"""
        return jsonable_encoder(self)

    @classmethod
    def model_post_init(cls, obj):
        if obj is None:
            return  # 防止 None 报错
        # 处理 ManyToManyRelation
        for field_name in getattr(obj, "_meta").fields_map.keys():
            value = getattr(obj, field_name, None)
            from tortoise.fields.relational import ManyToManyRelation
            if isinstance(value, ManyToManyRelation):
                try:
                    value_list = list(value)
                except TypeError:
                    value_list = []
                setattr(obj, field_name, value_list)