# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  qlv-helper
# FileName:     order_page.py
# Description:  订单页的HTTP响应处理模块
# Author:       ASUS
# CreateDate:   2025/11/28
# Copyright ©2011-2025. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import re
import aiohttp
from datetime import datetime
from bs4 import BeautifulSoup, Tag
from collections import OrderedDict
from typing import Dict, Any, Optional, List
from qlv_helper.utils.type_utils import convert_cn_to_en
from http_helper.client.async_proxy import HttpClientFactory
from qlv_helper.utils.datetime_utils import get_current_dtstr
from qlv_helper.utils.type_utils import get_key_by_index, get_value_by_index, safe_convert_advanced


async def get_order_page_html(
        order_id: int, domain: str, protocol: str = "http", retry: int = 1, timeout: int = 5, enable_log: bool = True,
        cookie_jar: Optional[aiohttp.CookieJar] = None, playwright_state: Dict[str, Any] = None
) -> Dict[str, Any]:
    order_http_client = HttpClientFactory(
        protocol=protocol if protocol == "http" else "https",
        domain=domain,
        timeout=timeout,
        retry=retry,
        enable_log=enable_log,
        cookie_jar=cookie_jar,
        playwright_state=playwright_state
    )
    return await order_http_client.request(
        method="get",
        url=f"/OrderProcessing/NewTicket_show/{order_id}?&r={get_current_dtstr()}",
        is_end=True
    )


def order_info_static_headers() -> OrderedDict[str, str]:
    return OrderedDict([
        ("receipted_ota", "OTA实收"),  # 0
        ("kickback", "佣金"),  # 1
        ("raw_order_no", "平台订单号"),  # 2
        ("trip_type", "行程类型"),  # 3
        ("id", "订单号"),  # 4
        ("stat_opration", "订单操作"),  # 5
        ("stat_order", "订单状态")  # 6
    ])


def parser_order_info(html: str) -> Dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")
    # 找到目标 table
    table = soup.find("table", class_="table no_border")
    if not table:
        return {}

    # 所有 td
    tds = table.find_all("td")
    result = {}

    for td in tds:
        text = td.get_text(strip=True)
        # 如果 td 内没有冒号、也不是按钮，跳过
        if "：" not in text:
            continue
        # 按 "：" 进行分割
        try:
            key, value = text.split("：", 1)
        except (Exception, ValueError):
            continue
        # 去掉换行符、空格
        key = key.strip()
        value = value.strip()

        # 如果 value 为空，尝试取 <b> 或其他控件内文本
        if not value:
            b = td.find("b")
            if b:
                value = b.get_text(strip=True)

        # 去掉尾部不需要的空格
        value = value.replace("\u00a0", "").strip()
        value = value[1:] if isinstance(value, str) and value.startswith("[") else value
        value = value[:-1] if isinstance(value, str) and value.endswith("]") else value
        result[key] = safe_convert_advanced(value)
    return convert_cn_to_en(data=result, header_map=order_info_static_headers())


def flight_static_headers() -> OrderedDict[str, str]:
    return OrderedDict([
        ("ticket_state", "票状态"),  # 0
        ("passenger_info", "乘客信息"),  # 1
        ("price_std", "票面价"),  # 2
        ("price_sell", "销售价"),  # 3
        ("tax_air", "机建费"),  # 4
        ("tax_fuel", "燃油费"),  # 5
        ("pnr", "PNR"),  # 6
        ("itinerary", "行程"),  # 7
        ("ticket_no", "票号"),  # 8
        ("itinerary_no", "行程单号"),  # 9
    ])


def flight_extend_headers() -> OrderedDict[str, str]:
    return OrderedDict([
        ("p_name", "姓名"),  # 0
        ("p_type", "类型"),  # 1
        ("id_type", "证件类型"),  # 2
        ("id_no", "身份证"),  # 3
        ("birth_day", "出生年月"),  # 4
        ("age", "年龄"),  # 5
        ("gender", "性别"),  # 6
        ("new_nation", "国籍"),  # 7
        ("card_issue_place", "签发国"),  # 8
        ("id_valid_dat", " 证件有效期"),  # 9
        ("code_dep", " 起飞机场"),  # 10
        ("code_arr", " 抵达机场"),  # 11
    ])


def parse_order_flight_table_headers(html: Tag) -> OrderedDict[str, str]:
    """解析航班表表头"""
    headers = OrderedDict()
    for th in html.find_all("th"):
        # 获取直接文本，不要子标签中的内容
        direct_texts = th.find_all(text=True, recursive=False)
        header = "".join(t.strip() for t in direct_texts if t.strip()) or th.get_text(strip=True)
        headers[header] = header
    return headers


def clean_order_flight_table(html: Tag) -> str:
    """清理航班表html内容多余的信息"""
    # 移除 script / style / hidden
    for tag in html.find_all(["script", "style"]):
        tag.extract()

    # 尝试去掉 display:none 的标签
    for tag in html.find_all(style=True):
        style = tag["style"].replace(" ", "").lower()
        if "display:none" in style:
            tag.extract()

    return html.get_text(strip=True)


def parse_order_flight_table_passenger_info(raw: Tag, headers: OrderedDict[str, str]) -> Dict[str, Any]:
    """
    解析包含 copyFn(...) 的乘客信息 TD，返回 dict
    """
    # -------------------------------
    # 1. 解析 <img onclick="copyFn('吴世勇||身份证|140104194702241336|男||1947/2/24 0:00:00||1900/1/1 0:00:00')" src="/images/nav_assistant.png" style="width:20px; height:20px; margin:0px;"/>
    # -------------------------------
    img = raw.find("img", onclick=True)
    if not img:
        return {}

    # 提取里面的参数内容
    onclick = img["onclick"]
    m = re.search(r"copyFn\('(.+?)'\)", onclick)
    if not m:
        return {}

    group = m.group(1)  # "吴世勇||身份证|140104194702241336|男||1947/2/24 0:00:00||1900/1/1 0:00:00"
    parts = group.split("|")

    # 字段参考：
    # 0: 姓名
    # 1: 空
    # 2: 证件类型
    # 3: 证件号
    # 4: 性别
    # 5: 空
    # 6: 出生日期
    # 7: 空
    # 8: 证件有效期（可能无）
    name = parts[0]
    id_type = parts[2]
    id_no_raw = parts[3]
    sex = parts[4]
    birth_raw = parts[6]
    id_valid_raw = parts[8] if len(parts) > 8 else ""

    # -------------------------------
    # 2. 证件号加掩码（如页面显示一致）
    # -------------------------------
    # if len(id_no_raw) >= 8:
    #     id_no_masked = id_no_raw[:6] + "****" + id_no_raw[-4:]
    # else:
    #     id_no_masked = id_no_raw

    # -------------------------------
    # 3. 出生日期格式化 1947/2/24 → 1947-02-24
    # -------------------------------
    def fmt_date(value: str) -> str:
        try:
            dt = datetime.strptime(value.split(" ")[0], "%Y/%m/%d")
            return dt.strftime("%Y-%m-%d")
        except (Exception,):
            return ""

    birth = fmt_date(birth_raw)
    id_valid = fmt_date(id_valid_raw)

    # -------------------------------
    # 4. 年龄计算
    # -------------------------------
    def calc_age(birth_str: str) -> Optional[int]:
        try:
            birthday = datetime.strptime(birth_str, "%Y-%m-%d")
            today = datetime.today()
            return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
        except (Exception,):
            return None

    age = calc_age(birth)

    # -------------------------------
    # 5. 类型（成人/儿童）需要从页面中取
    # -------------------------------
    type_span = raw.find(name="span", text=re.compile(r"(成人|儿童|婴儿)"))
    ptype = ""
    if type_span:
        ptype = type_span.get_text(strip=True).replace("【", "").replace("】", "")

    # -------------------------------
    # 6. 国籍、签发国 从 name="guobie" 的两个 span 获取
    # -------------------------------
    guobies = raw.find_all("span", attrs={"name": "guobie"})
    nationality = guobies[0].get_text(strip=True) if len(guobies) > 0 else ""
    issue_country = guobies[1].get_text(strip=True) if len(guobies) > 1 else ""

    return {
        get_key_by_index(index=0, ordered_dict=headers): name,  # 姓名
        get_key_by_index(index=1, ordered_dict=headers): ptype,  # 类型: 成人/儿童
        get_key_by_index(index=2, ordered_dict=headers): id_type,  # 证件类型
        get_key_by_index(index=3, ordered_dict=headers): id_no_raw,  # 身份证
        get_key_by_index(index=4, ordered_dict=headers): birth,  # 出生年月
        get_key_by_index(index=5, ordered_dict=headers): age,  # 年龄
        get_key_by_index(index=6, ordered_dict=headers): sex,  # 性别
        get_key_by_index(index=7, ordered_dict=headers): nationality,  # 国籍
        get_key_by_index(index=8, ordered_dict=headers): issue_country,  # 签发国
        get_key_by_index(index=9, ordered_dict=headers): id_valid  # 证件有效期
    }


def parse_order_flight_table_row(
        tr: Tag, headers: OrderedDict, extend_headers: OrderedDict
) -> Dict[str, Any]:
    """解析航班表每一行的数据"""
    tds = tr.find_all("td", recursive=False)
    values = {}

    for idx, td in enumerate(tds):
        if idx >= len(headers):
            continue

        key = get_key_by_index(ordered_dict=headers, index=idx)
        value = get_value_by_index(ordered_dict=headers, index=idx)
        # 如果是 “乘客信息” → 使用结构化解析
        if "乘客" in value or "乘客信息" in value:
            passenger_info = parse_order_flight_table_passenger_info(raw=td, headers=extend_headers)
            values.update(passenger_info)
        else:
            raw = clean_order_flight_table(html=td)
            if "行程" in value:
                code_dep_key = get_key_by_index(index=10, ordered_dict=extend_headers)
                code_arr_key = get_key_by_index(index=11, ordered_dict=extend_headers)
                raw_slice = raw.split("-")
                if len(raw_slice) == 2:
                    values[code_dep_key] = raw_slice[0]
                    values[code_arr_key] = raw_slice[-1]
            elif "PNR" in value:
                values[key] = raw
            else:
                values[key] = safe_convert_advanced(raw)

    return values


def extract_structured_table_data(table: Tag) -> List[Optional[Dict[str, Any]]]:
    """提取结构化的表格数据"""
    # headers = parse_order_flight_table_headers(html=table)
    headers = flight_static_headers()
    extend = flight_extend_headers()
    rows = list()
    for tr in table.find_all("tr")[1:]:  # 跳过表头
        rows.append(parse_order_flight_table_row(tr=tr, headers=headers, extend_headers=extend))

    return rows


def parser_order_flight_table(html: str) -> List[Optional[Dict[str, Any]]]:
    """解析航班表"""
    soup = BeautifulSoup(html, 'html.parser')
    # 三个主要的order_sort div
    order_sections = soup.find_all('div', class_='order_sort')
    section = order_sections[3] if len(order_sections) > 3 else Tag(name="")
    results = list()

    tables = section.find_all('table', class_='table table_border table_center')
    for table in tables:
        table_data = extract_structured_table_data(table)
        if table_data:
            results.extend(table_data)

    return results
