# -*- coding: utf-8 -*-
# @Time    : 2025/12/8 下午1:50
# @Author  : fzf
# @FileName: exceptions.py
# @Software: PyCharm

class FastAutoException(Exception):
    code = 0
    detail = '基础错误'


class HTTPException(FastAutoException):
    code = 404
    detail = "Object not found"


class HTTPPermissionException(FastAutoException):
    code = 403
    detail = 'Permission denied'
