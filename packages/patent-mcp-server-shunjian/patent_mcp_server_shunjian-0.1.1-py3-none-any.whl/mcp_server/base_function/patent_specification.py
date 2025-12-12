# python/third_party/base_function/patent_specification.py
import os
import requests
from mcp_server.env_loader import load_env
from typing import Annotated
from pydantic import Field
from typing import Annotated
from pydantic import Field

DEFAULT_BASE_URL = "http://open.baiten.cn"

def get_specification(
        doc_id: Annotated[str, Field(description="专利文档号 (如 CN201220454416.7)")]
) -> dict:
    """
    获取专利说明书（原始JSON响应）
    返回:
      dict 包含:
        - qTime: 查询返回时间毫秒
        - total_hits: 查询返回记录数量
        - grouped_hits: 保留字段暂不使用
        - des_1: 技术领域
        - des_2: 背景技术
        - des_3: 发明内容
        - des_4: 附图说明
        - des_5: 具体实施方式
        - des_f: 说明书全文
    """
    cfg = load_env()
    app_key = cfg["patent_appkey"]

    base_url = (os.getenv("PATENT_DB_BASEURL") or DEFAULT_BASE_URL).rstrip("/")
    url = (
        f"{base_url}/router/openService/get_spec?"
        f"app_key={app_key}&doc_id={doc_id}"
    )

    print("请求地址:", url)
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def extract_specification(
        doc_id: Annotated[str, Field(description="专利文档号 (如 CN201220454416.7)")]
) -> dict:
    """
    调用接口并提取说明书信息
    返回:
      dict 包含:
        - qTime: 查询返回时间毫秒
        - total_hits: 查询返回记录数量
        - grouped_hits: 保留字段暂不使用
        - des_1: 技术领域
        - des_2: 背景技术
        - des_3: 发明内容
        - des_4: 附图说明
        - des_5: 具体实施方式
        - des_f: 说明书全文
    """
    data = get_specification(doc_id)
    spec_info = {
        "qTime": None,
        "total_hits": None,
        "grouped_hits": None,
        "des_1": None,
        "des_2": None,
        "des_3": None,
        "des_4": None,
        "des_5": None,
        "des_f": None
    }

    try:
        # 提取顶层字段
        spec_info["qTime"] = data.get("qTime")
        spec_info["total_hits"] = data.get("total_hits")
        spec_info["grouped_hits"] = data.get("grouped_hits")
        
        # 提取说明书各部分
        field_values = data.get("document", {}).get("field_values", {})
        spec_info["des_1"] = field_values.get("des_1")
        spec_info["des_2"] = field_values.get("des_2")
        spec_info["des_3"] = field_values.get("des_3")
        spec_info["des_4"] = field_values.get("des_4")
        spec_info["des_5"] = field_values.get("des_5")
        spec_info["des_f"] = field_values.get("des_f")
    except Exception as e:
        print("解析说明书失败:", e)

    return spec_info
