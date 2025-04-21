import os
import git
from shutil import copy2
from PIL import Image
import tempfile

# GitHub 仓库配置
REPO_PATH = r"D:\GitResponse\UP_img"  # Git 仓库本地路径
REPO_BRANCH = "main"  # GitHub Pages 分支
# UPLOAD_DIR = "image"  # 存放上传图像的文件夹

# 确保上传文件夹存在
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# Git 操作：推送到 GitHub Pages
def push_to_github(file_path,UPLOAD_DIR, file_name):
    try:
        # 克隆仓库并设置 Git
        repo = git.Repo(REPO_PATH)

        # 将文件复制到仓库的相关目录
        destination_path = os.path.join(REPO_PATH, UPLOAD_DIR, file_name)  # 将文件放到 image 目录
        copy2(file_path, destination_path)

        # 执行 Git 操作
        repo.git.add(f"{UPLOAD_DIR}/*")  # 将新文件添加到 Git
        repo.index.commit(f"Add new image: {file_name}")  # 提交更改
        repo.remotes.origin.push()  # 推送到远程仓库
        print(f"Successfully pushed {file_name} to GitHub Pages.")
    except Exception as e:
        print(f"Failed to push {file_name} to GitHub Pages: {str(e)}")

# 给定图片路径并上传到 GitHub Pages
def upload_image_to_github(image_path):
    # 提取文件名
    file_name = os.path.basename(image_path)

    # 确保文件存在
    if not os.path.exists(image_path):
        print(f"Error: The file {image_path} does not exist.")
        return

    # 将图像上传到 GitHub Pages
    push_to_github(image_path, file_name)

# 给定PIL图像并上传到GitHub Pages
def upload_PILimage_to_github(pil_image,UPLOAD_DIR, file_name):
    # 创建一个临时文件路径来保存PIL图像
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        temp_path = tmp.name  # 只取路径，不占用文件
    pil_image.save(temp_path)  # 保存图像

    try:
        # 推送到 GitHub
        push_to_github(temp_path,UPLOAD_DIR, file_name)
    finally:
        # 上传后删除临时文件
        if os.path.exists(temp_path):
            os.remove(temp_path)

# 测试代码
if __name__ == "__main__":
    # 给定图片路径
    image_path = r"C:\Users\Peli\Desktop\test\0.jpg"  # 替换为你本地的图片路径
    img_rgb_pil = Image.new('RGB', (100, 100), color='red')  # 示例图片
    # 上传图片到 GitHub Pages
    # upload_PILimage_to_github(img_rgb_pil,"mask","read.png")
