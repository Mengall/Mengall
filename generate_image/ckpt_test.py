import os
os.environ["XFORMERS_FORCE_DISABLE_TRITON"] = "1"
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, message=".*TRANSFORMERS_CACHE.*")
from diffusers import StableDiffusionPipeline
import torch
import time

# 加载 .ckpt 文件并转换为 diffusers 格式
model_path = "D:\Deep-learning\khoya_data\pretrained\dreamlike-photoreal-2.0.ckpt"
pipe = StableDiffusionPipeline.from_single_file(model_path, torch_dtype=torch.float16)
pipe.to("cuda")

start_time = time.time()
seed = 42
generator = torch.Generator("cuda").manual_seed(seed)

# 生成食品广告图像
prompt = """
a bread advertisement picture.
        """
with torch.no_grad():
    image = pipe(prompt,generator=generator).images[0]
    # image = pipe(prompt).images[0]

end_time = time.time()
elapsed_time = end_time - start_time
# 输出推理时间
print(f"Inference Time: {elapsed_time:.2f} seconds")

# 保存和显示图片
# image.save("generated_food_ad.jpg")
image.show()

