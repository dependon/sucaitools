import os
from PIL import Image
import os

# 修改 process_image 函数以接受不同参数
def process_image(image_path, mode, **kwargs):
    try:
        with Image.open(image_path) as img:
            if mode == "scale":
                scale = float(kwargs.get('scale', 0.5)) # 默认值以防万一
                new_size = (int(img.width * scale), int(img.height * scale))
            elif mode == "fixed":
                width = int(kwargs.get('width'))
                height = int(kwargs.get('height'))
                new_size = (width, height)
            elif mode == "fixed_width":
                # 固定宽度，按比例调整高度
                width = int(kwargs.get('width'))
                ratio = width / img.width
                height = int(img.height * ratio)
                new_size = (width, height)
            elif mode == "fixed_height":
                # 固定高度，按比例调整宽度
                height = int(kwargs.get('height'))
                ratio = height / img.height
                width = int(img.width * ratio)
                new_size = (width, height)
            else:
                print(f"未知的处理模式: {mode} for {image_path}")
                return # 如果模式未知，则不处理

            # 保持图片模式（针对有透明通道的PNG等格式）
            resized_img = img.resize(new_size, Image.LANCZOS)

            # 获取原始文件的扩展名
            file_extension = os.path.splitext(image_path)[1].lower()

            # 根据扩展名决定保存格式
            save_format = None
            if file_extension in ('.jpg', '.jpeg'):
                save_format = 'jpeg'
                # 如果是RGBA模式，转换为RGB，因为JPEG不支持透明度
                if resized_img.mode == 'RGBA':
                    resized_img = resized_img.convert('RGB')
            elif file_extension == '.png':
                save_format = 'png'
            elif file_extension == '.bmp':
                save_format = 'bmp'
            elif file_extension == '.gif':
                save_format = 'gif'

            if save_format:
                # 覆盖保存原图
                if save_format == 'jpeg':
                    resized_img.save(image_path, format=save_format, quality=95)
                else:
                    resized_img.save(image_path, format=save_format)
            else:
                print(f"不支持的保存格式: {file_extension} for {image_path}")
            print(f"已处理 ({mode}): {image_path}")

    except Exception as e:
        print(f"处理失败 {image_path}: {str(e)}")

# 修改 process_directory 以传递模式和参数
def process_directory(root_dir, mode='scale', **kwargs):
    # 支持的图片格式
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(valid_extensions):
                file_path = os.path.join(root, file)
                # 将模式和参数传递给 process_image
                process_image(file_path, mode, **kwargs)

if __name__ == "__main__":
    # 测试代码（可选，通常由GUI调用）
    target_dir = r'c:\Users\lmh\Desktop\me\素材'  # 修改为需要处理的目录
    # 测试按比例缩放
    # process_directory(target_dir, mode='scale', scale=0.7)
    # 测试固定分辨率
    # process_directory(target_dir, mode='fixed', width=800, height=600)
    print("脚本可以直接运行进行测试，但主要由 gui.py 调用")