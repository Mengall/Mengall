import os
os.environ["XFORMERS_FORCE_DISABLE_TRITON"] = "1"
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, message=".*TRANSFORMERS_CACHE.*")
import torch
from diffusers import StableDiffusionPipeline

def generate_lora_img(prompt, seed):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    base_model_id = "D:\Deep-learning\khoya_data\pretrained\dreamlike-photoreal-2.0.ckpt"  # 或你微调用的基础模型
    lora_path = "D:\Deep-learning\khoya_data\model\last.safetensors"  # 替换为你的LoRA权重路径

    # 加载基础模型
    pipe = StableDiffusionPipeline.from_single_file(base_model_id, torch_dtype=torch.float16)
    pipe.to(device)

    # 加载 LoRA 权重
    pipe.load_lora_weights(lora_path)
    if seed is not None and seed >= 0:
        generator = torch.Generator(device).manual_seed(seed)
    else:
        generator = None

    # 提示词生成图片
    with torch.no_grad():
        image = pipe(prompt, generator=generator).images[0]
        # image = pipe(prompt).images[0]

    image.show()
    # image.save("lora_result.png")
    return image

if __name__=="__main__":
    prompt = """a coffe advertisement picture."""

    generate_lora_img(prompt, seed=429496730)