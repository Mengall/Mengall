import os
import time
import requests
import warnings
import logging
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import gradio as gr

# 设置日志格式
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
# 屏蔽 FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)
os.environ["XFORMERS_FORCE_DISABLE_TRITON"] = "1"

# 加载环境变量
load_dotenv()
token = os.getenv("DASHSCOPE_API_KEY")
if not token:
    raise ValueError("未检测到 DashScope Token！请设置 DASHSCOPE_API_KEY 环境变量")

# API 配置
API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis"
TASK_QUERY_URL = "https://dashscope.aliyuncs.com/api/v1/tasks/"

def edit_image_with_mask(base_image_url,mask_image_url):
    """使用遮罩编辑图片"""
    headers = {
        "X-DashScope-Async": "enable",  # 启用异步模式
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
#API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis"
#TASK_QUERY_URL = "https://dashscope.aliyuncs.com/api/v1/tasks/"
    payload = {
        "model": "wanx2.1-imageedit",
        "input": {
            "function": "description_edit_with_mask",
            "prompt": "将该区域修改为巧克力。",
            "base_image_url": base_image_url,
            "mask_image_url": mask_image_url
        },
        "parameters": {
            "n": 1  # 生成1张图片
        }
    }

    try:
        # 1. 提交任务
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        task_data = response.json()

        if "output" not in task_data or "task_id" not in task_data["output"]:
            raise ValueError("Invalid API response format")

        task_id = task_data["output"]["task_id"]
        print(f"Task submitted successfully. Task ID: {task_id}")

        # 2. 轮询任务结果
        while True:
            task_response = requests.get(
                f"{TASK_QUERY_URL}{task_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            task_result = task_response.json()
            # print(task_result)
            status = task_result.get("output", {}).get("task_status")
            if status == "SUCCEEDED":
                print("Task completed successfully!")
                # 提取结果图片URL
                result_url = task_result["output"]["results"][0]["url"]
                print(f"Result image URL: {result_url}")
                return result_url
            elif status in ["FAILED", "CANCELED"]:
                raise Exception(f"Task failed with status: {status}")
            else:
                print(f"Task status: {status}, waiting...")
                time.sleep(5)  # 每5秒检查一次

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")


# 执行函数
if __name__ == "__main__":
    base_image_url = "https://mengall.github.io/UP_img/image/user.png"
    mask_image_url = "https://mengall.github.io/UP_img/mask/mask.png"
    # result_image_url = edit_image_with_mask(base_image_url,mask_image_url)

    # 可选：下载结果图片
    # if result_image_url:
    #     try:
    #         image_data = requests.get(result_image_url).content
    #         with open("result_image.jpg", "wb") as f:
    #             f.write(image_data)
    #         print("Image downloaded successfully as 'result_image.jpg'")
    #     except Exception as e:
    #         print(f"Failed to download image: {str(e)}")
