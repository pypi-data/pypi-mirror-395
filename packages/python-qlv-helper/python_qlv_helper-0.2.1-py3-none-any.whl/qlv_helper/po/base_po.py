# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  qlv-helper
# FileName:     base_po.py
# Description:  po对象基础类
# Author:       ASUS
# CreateDate:   2025/11/25
# Copyright ©2011-2025. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from typing import List
from playwright.async_api import Page


class BasePo(object):
    __page: Page

    def __init__(self, page: Page, url: str):
        self.url = url
        self.__page = page
        if self.is_current_page() is False:
            raise ValueError("page参数值无效")

    def get_page(self) -> Page:
        return self.__page

    def is_current_page(self) -> bool:
        url = self.__page.url.split("?")[0]
        if isinstance(self.__page, Page) and url.endswith(self.url):
            return True
        else:
            return False

    def get_url_domain(self) -> str:
        if isinstance(self.__page, Page):
            page_slice: List[str] = self.__page.url.split("/")
            return f"{page_slice[0]}://{page_slice[2]}"
        else:
            raise AttributeError("PO对象中的page属性未被初始化")
