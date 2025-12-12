# python/base_function/patent_similar.py
import os
import requests
from mcp_server.env_loader import load_env
from typing import Annotated
from pydantic import Field

from typing import Annotated
from pydantic import Field

DEFAULT_BASE_URL = "http://open.baiten.cn"

def get_similar_patents(
        doc_id: Annotated[str, Field(description="专利号 (如 CN112233445A)")],
        page_index: Annotated[int, Field(description="分页页码")] = 1,
        page_size: Annotated[int, Field(description="每页数量")] = 10
) -> dict:
    """
    相似专利查询 (接口 17)
    请求地址: /router/openService/related
    参数:
      - patent_id: 专利公开号 (pid)，例如 'CN112233445A'
      - page_index: 分页页码
      - page_size: 每页数量
      - app_key: 用户 ID
    """
    cfg = load_env()
    app_key = cfg["patent_appkey"]

    base_url = (os.getenv("PATENT_DB_BASEURL") or DEFAULT_BASE_URL).rstrip("/")
    url = f"{base_url}/router/openService/related?doc_id={doc_id}&app_key={app_key}"

    print("请求地址:", url)
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()
