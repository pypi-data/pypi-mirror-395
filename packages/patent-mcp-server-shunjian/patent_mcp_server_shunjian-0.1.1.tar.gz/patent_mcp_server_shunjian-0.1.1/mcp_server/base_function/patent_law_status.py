# python/third_party/base_function/patent_law_status.py
import os
import requests
from mcp_server.env_loader import load_env
from typing import Annotated
from pydantic import Field

DEFAULT_BASE_URL = "http://open.baiten.cn"

# The original document had a syntax error with two definitions for get_law_status.
# Assuming the intent was to replace the first with the second, or to use the second.
# I will keep the second (Annotated) definition for get_law_status as it seems to be the intended one,
# and remove the first one to fix the syntax error.
def get_law_status(
        app_num: Annotated[str, Field(description="专利申请号 (如 CN201110030901.1)")],
        law_category: Annotated[str, Field(description="法律类别 (默认 flzt)")] = "flzt"
) -> dict:
    """
    获取专利法律状态（原始JSON响应）
    """
    cfg = load_env()
    app_key = cfg["patent_appkey"]

    base_url = (os.getenv("PATENT_DB_BASEURL") or DEFAULT_BASE_URL).rstrip("/")
    url = (
        f"{base_url}/router/openService/law?"
        f"app_key={app_key}&app_num={app_num}&law_category={law_category}"
    )

    print("请求地址:", url)
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def extract_law_status(app_num: str, law_category: str = "flzt") -> dict:
    """
    调用接口并提取法律状态信息
    返回:
      dict 包含:
        - notice_date: 法律公告日期
        - law_state: 法律状态
        - law_info: 法律状态详情
    """
    data = get_law_status(app_num, law_category)
    law_status = {
        "notice_date": None,
        "law_state": None,
        "law_info": None
    }

    try:
        field_values = data.get("document", {}).get("field_values", {})
        law_status["notice_date"] = field_values.get("notice_date")
        law_status["law_state"] = field_values.get("law_state")
        law_status["law_info"] = field_values.get("law_info")
    except Exception as e:
        print("解析法律状态失败:", e)

    return law_status
