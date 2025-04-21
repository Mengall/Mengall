import gradio as gr

# 文生图功能
def generate_image(prompt):
    # 在这里调用文生图模型生成图像
    return "生成的图像"  # 这里返回生成的图像

# 图像重绘功能
def inpaint_image(image, mask):
    # 在这里调用图像重绘模型
    return "重绘后的图像"  # 这里返回重绘后的图像

with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.Tab("文生图"):
            prompt_input = gr.Textbox(label="输入提示词")
            generated_image = gr.Image(label="生成的图像")
            generate_button = gr.Button("生成图像")  # 点击按钮触发图像生成
            generate_button.click(generate_image, inputs=prompt_input, outputs=generated_image)

        with gr.Tab("图像重绘"):
            image_input = gr.Image(label="上传图像")
            mask_input = gr.Image(label="上传遮罩")
            inpaint_output = gr.Image(label="重绘后的图像")
            inpaint_button = gr.Button("开始重绘")  # 点击按钮触发图像重绘
            inpaint_button.click(inpaint_image, inputs=[image_input, mask_input], outputs=inpaint_output)

demo.launch()
