# python/third_party/base_function/patent_images.py
import os
import requests
from mcp_server.env_loader import load_env
from typing import Annotated
from pydantic import Field

DEFAULT_BASE_URL = "http://open.baiten.cn"

def get_patent_images(pub_num: str, width: int = 500, image_type: int = 2) -> dict:
    """
    获取专利附图信息（原始JSON响应）
    """
    cfg = load_env()
    app_key = cfg["patent_appkey"]

    base_url = (os.getenv("PATENT_DB_BASEURL") or DEFAULT_BASE_URL).rstrip("/")
    url = (
        f"{base_url}/router/nosdkService/image?"
        f"pub_num={pub_num}&width={width}&type={image_type}&app_key={app_key}"
    )

    print("请求地址:", url)
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def extract_image_urls(pub_num: str, width: int = 500, image_type: int = 2) -> list[str]:
    """
    调用接口并提取图片地址列表
    返回:
      list[str] 包含所有图片的 URL
    """
    data = get_patent_images(pub_num, width, image_type)
    image_urls = []

    try:
        # 检查返回的数据结构并提取 url 字段
        if isinstance(data, dict):
            # 如果返回单个 url
            if "url" in data:
                image_urls.append(data["url"])
            # 如果返回的是包含多个图片的列表
            elif "images" in data and isinstance(data["images"], list):
                for img in data["images"]:
                    if "url" in img:
                        image_urls.append(img["url"])
        elif isinstance(data, list):
            # 如果直接返回列表
            for item in data:
                if isinstance(item, dict) and "url" in item:
                    image_urls.append(item["url"])
                elif isinstance(item, str):
                    image_urls.append(item)
    except Exception as e:
        print("解析图片地址失败:", e)

    return image_urls
