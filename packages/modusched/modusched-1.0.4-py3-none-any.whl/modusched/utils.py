from urllib.parse import urlparse
import base64
import re


def save_base64_image(markdown_line, filename_prefix="gemini_output"):
    """
    提取 base64 字符串
    """

    match = re.search(r"!\[.*?\]\(data:image/(png|jpeg);base64,(.*?)\)", markdown_line)
    if match:
        image_format = match.group(1)  # png 或 jpeg
        base64_data = match.group(2)

        # 解码并保存
        image_data = base64.b64decode(base64_data)
        filename = f"{filename_prefix}.{image_format}"
        with open(f"{filename}", "wb") as f:
            f.write(image_data)
    else:
        print("未找到合法的 base64 图片数据")


def image_to_base64(image_path:str) ->str:
    """
    以二进制方式读取图片文件
    """
    with open(image_path, "rb") as image_file:
        # 将图像文件内容读取到变量中
        image_data = image_file.read()
        # 使用base64模块进行编码
        base64_encoded_data = base64.b64encode(image_data)
        # 将编码后的数据转换为字符串
        base64_encoded_str = base64_encoded_data.decode("utf-8")
        return base64_encoded_str


def is_url_urllib(url_string: str):
    """
    检查 scheme 和 netloc 是否存在，并且 netloc 不为空
    通常，一个有效的 URL 应该有 scheme (如 http, https) 和 netloc (如 www.example.com)
    """
    try:
        result = urlparse(url_string)
        return all([result.scheme, result.netloc])
    except Exception:
        return False
