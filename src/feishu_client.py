import requests, os
from dotenv import load_dotenv
load_dotenv()

class FeishuBitableClient:
    def __init__(self):
        self.app_id = os.getenv("FEISHU_APP_ID")
        self.base_url = "https://open.feishu.cn/open-apis"
    def list_records(self):
        return []
