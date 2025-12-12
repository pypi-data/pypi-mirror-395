# python/base_function/patent_claims.py
import os
import requests
from mcp_server.env_loader import load_env

DEFAULT_BASE_URL = "http://open.baiten.cn"

from typing import Annotated
from pydantic import Field

def get_claims(
        app_num: Annotated[str, Field(description="专利申请号 (如 CN00100001.2)")],
        pat_type: Annotated[str, Field(description="专利类型 (app=公开专利, auth=授权专利, 默认 app)")] = "app"
) -> dict:
    """
    获取专利权利要求详情（原始JSON响应）
    """
    cfg = load_env()
    app_key = cfg["patent_appkey"]

    base_url = (os.getenv("PATENT_DB_BASEURL") or DEFAULT_BASE_URL).rstrip("/")
    url = (
        f"{base_url}/router/openService/claims?"
        f"app_key={app_key}&pat_type={pat_type}&app_num={app_num}"
    )

    print("请求地址:", url)
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def extract_claims(
        app_num: Annotated[str, Field(description="专利申请号 (如 CN00100001.2)")],
        pat_type: Annotated[str, Field(description="专利类型 (app=公开专利, auth=授权专利, 默认 app)")] = "app"
) -> list[str]:
    """
    调用接口并提取权利要求文本列表
    """
    data = get_claims(app_num, pat_type)
    claims = []

    # 返回结果里通常在 document -> field_values -> claims
    try:
        # 优先尝试 patent_claims_list 格式
        if "patent_claims_list" in data:
            claims_list = data["patent_claims_list"]
            # 提取每个claim的文本
            for item in claims_list:
                if "claim" in item:
                    # 移除HTML标签（简单处理）
                    text = item["claim"].replace("<p>", "").replace("</p>", "").strip()
                    claims.append(text)
                # 递归处理子权利要求 (patentClaimses)
                if "patentClaimses" in item and isinstance(item["patentClaimses"], list):
                    for sub_item in item["patentClaimses"]:
                        if "claim" in sub_item:
                            text = sub_item["claim"].replace("<p>", "").replace("</p>", "").strip()
                            claims.append(text)
                            
        elif "document" in data and "field_values" in data["document"]:
            field_values = data["document"]["field_values"]
            # claims 字段可能是一个列表或字符串
            if isinstance(field_values.get("claims"), list):
                claims = field_values["claims"]
            elif isinstance(field_values.get("claims"), str):
                # 按换行或分号拆分
                claims = [c.strip() for c in field_values["claims"].split("\n") if c.strip()]
    except Exception as e:
        print("解析权利要求失败:", e)

    return claims
