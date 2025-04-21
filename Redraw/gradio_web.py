import gradio as gr
import numpy as np
from PIL import Image
from git_IMG import upload_PILimage_to_github
from draw_api import edit_image_with_mask
from generate_image.khoya_test import generate_lora_img
import time
import torch
import requests


def text_to_image(prompt, seed):
    print(seed)
    if seed == 0:
        seed = None
    img = generate_lora_img(prompt, seed)
    return img

def process(data,image_name,mask_name):
    try:
        #异常处理
        if data is None or "background" not in data or data['background'] is None:
            print("请上传图像！")
        # 获取背景图像
        img = np.array(data["background"], dtype=np.uint8)
        img = np.squeeze(img)  # 移除批量维度
        img_rgb = img[:, :, :3]  # 只保留 RGB 通道
        img_rgb_pil = Image.fromarray(img_rgb)
        # img_rgb_pil.show()
        # print("img:", img_rgb_pil)

        # 获取掩码图像
        if "layers" not in data or data["layers"] is None:
            raise ValueError("请先绘制遮罩")

        # 获取掩码图像
        mask = np.array(data["layers"], dtype=np.uint8)
        mask = np.squeeze(mask)  # 移除批量维度
        mask_rgb = mask[:, :, :3]  # 只保留 RGB 通道
        # 确保掩码是一个二值图像
        mask_rgb_pil = Image.fromarray(mask_rgb)
        # print("mask:", mask_rgb_pil)

        upload_PILimage_to_github(img_rgb_pil, "image", image_name)
        upload_PILimage_to_github(mask_rgb_pil, "mask", mask_name)
    except Exception as e:
        return f"发生错误：{e}"
    return "上传成功！"

def output_PILimage(image_name,mask_name):
    timestamp = int(time.time())
    base_image_url = f"https://mengall.github.io/UP_img/image/{image_name}"
    mask_image_url = f"https://mengall.github.io/UP_img/mask/{mask_name}"
    print(base_image_url)
    print(mask_image_url)

    img_result = wait_for_image(base_image_url, timestamp)
    mask_result = wait_for_image(mask_image_url, timestamp)

    if img_result and mask_result:
        img_link = edit_image_with_mask(img_result, mask_result)
    else:
        img_link = None
        print("图片未上传")

    return img_link

def hand_link(data):
    image_name = genrate_filename("user")
    mask_name = genrate_filename("mask")

    status = process(data, image_name, mask_name)
    if status == "上传成功！":
        img_link = output_PILimage(image_name, mask_name)
        # print(img_link)
        return status, img_link
    else:
        return status, None

def genrate_filename(name):
    return time.strftime(f"{name}_%Y%m%d_%H%M%S.png")

def wait_for_image(url,timestamp, timeout=15, interval=3):
    """
    轮询检测图像是否可以访问。
    - timeout: 最长等待时间（秒）
    - interval: 每次轮询间隔时间（秒）
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            url = f"{url}?v={timestamp}"
            res = requests.get(url)
            print(res)
            if res.status_code == 200:
                return url
        except Exception as e:
            print(f"等待图像可访问时出错: {e}")
        time.sleep(interval)
    return None


with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.Tab("文生图"):
            prompt_input = gr.Textbox(label="请输入提示词", placeholder="请输入文本描述")
            seed_input = gr.Number(label="选择种子（可选）", precision=0, value=None, interactive=True, minimum=0)  # 可以选择输入种子
            image_show = gr.Image(label="生成的图像")

            # 为按钮设置不同的名字，避免冲突
            generate_button = gr.Button("图像生成")
            generate_button.click(fn=text_to_image, inputs=[prompt_input, seed_input], outputs=image_show)

        with gr.Tab("图像重绘"):
            image_mask = gr.ImageEditor(label="图像重绘区域",
                                       show_share_button=True,
                                       layers=False,
                                       height=512)
            output_image = gr.Image(label="重绘后的图像")

            # 为按钮设置不同的名字，避免冲突
            upload_button = gr.Button("开始重绘")
            status_text = gr.Textbox(label="上传状态", interactive=False)
            upload_button.click(fn=hand_link, inputs=image_mask, outputs=[status_text, output_image])

demo.launch()