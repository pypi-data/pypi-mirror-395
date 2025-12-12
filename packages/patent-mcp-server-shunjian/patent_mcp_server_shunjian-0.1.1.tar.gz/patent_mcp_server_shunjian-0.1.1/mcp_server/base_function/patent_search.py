# python/base_function/patent_search.py
import os
import requests
from mcp_server.env_loader import load_env

DEFAULT_BASE_URL = "http://open.baiten.cn"

from typing import Annotated
from pydantic import Field

def custom_search(
        query_string: Annotated[str, Field(description="专利检索式，例如 'TI=人工智能' (标题包含人工智能)")],
        page_index: Annotated[int, Field(description="分页页码，从1开始")] = 1,
        page_size: Annotated[int, Field(description="每页数量，默认10")] = 10,
) -> dict:
    """
    佰腾定制版基础检索接口（nosdkService/search）
    请求地址: /router/nosdkService/search
    参数:
      - queryString: 检索式（原样传入，由 requests 负责编码）
      - pageIndex: 分页页码
      - pageSize: 分页大小
      - app_key: 用户ID（从 env 加载）
    """
    cfg = load_env()
    app_key = cfg["patent_appkey"]

    # base_url 优先从环境变量 PATENT_DB_BASEURL 获取，回退到默认
    base_url = (os.getenv("PATENT_DB_BASEURL") or DEFAULT_BASE_URL).rstrip("/")

    params = {
        "queryString": query_string,   # 不手动编码，交给 requests
        "app_key": app_key,
        "pageIndex": page_index,
        "pageSize": page_size,
    }

    url = f"{base_url}/router/nosdkService/search"
    print("请求地址:", url, "参数:", params)  # 调试输出
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()
