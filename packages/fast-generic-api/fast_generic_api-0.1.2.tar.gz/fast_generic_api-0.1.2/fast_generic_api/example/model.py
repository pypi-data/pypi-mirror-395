# -*- coding: utf-8 -*-
# @Time    : 2025/12/8 下午5:49
# @Author  : fzf
# @FileName: model.py
# @Software: PyCharm
from tortoise import fields, models

class Item(models.Model):
    id = fields.IntField(pk=True)
    # uuid = fields.UUIDField(unique=True, index=True)
    name = fields.CharField(max_length=100)
    description = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "items"