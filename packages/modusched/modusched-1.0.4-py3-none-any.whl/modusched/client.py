"""
client.py 用于管理client
"""

import requests
import time
import json
import base64
import httpx
import logging
from modusched.utils import save_base64_image, image_to_base64

from tenacity import (
    retry,
    wait_fixed,
    wait_chain,
    wait_exponential,
    stop_after_attempt,
    retry_if_exception_type,
    before_sleep_log,
)
import uuid
import websockets
from modusched.protocols import MsgType, full_client_request, receive_message
from volcenginesdkarkruntime import Ark, AsyncArk


class ArkClient:
    """
    ArkClient
    """

    def __init__(
        self, api_key: str, api_base: str = "",appid: str = "", access_token: str = ""
    ):
        """
        初始化 OpenAI 客户端
        url = 'https://api.bianxie.ai/v1/audio/transcriptions'  asr 语音识别
        """
        self.api_key = api_key
        self.api_base = api_base
        self.client = Ark(api_key=self.api_key)
        self.async_client =AsyncArk(api_key=self.api_key)
        self.appid = appid or "9370139706"
        self.access_token = access_token or "rPnirNKqj-jYwic1yTYpVOUU0xx2g8uj"
        self.endpoint = "wss://openspeech.bytedance.com/api/v1/tts/ws_binary"

    def request(self, data):
        result = self.client.chat.completions.create(**data)
        return result
    
    @retry(
        wait=wait_chain(
            wait_fixed(30),  # 第一次重试等待30秒
            wait_fixed(60),  # 第二次重试等待60秒
            wait_fixed(90)   # 第三次重试等待90秒
            ),
        stop=stop_after_attempt(3),  # 最多尝试5次 (1次初始请求 + 4次重试)
        retry=(
            retry_if_exception_type(httpx.RequestError)  # 匹配网络错误 (连接超时, DNS, SSL等)
            | retry_if_exception_type(httpx.HTTPStatusError)  # 匹配HTTP状态码错误
        ),
        # before_sleep=before_sleep_log(logger, logging.INFO),  # 每次重试前打印日志
        reraise=True,  # 如果所有重试都失败，重新抛出最后一个异常
    )
    async def arequest(self, data):
        result = await self.async_client.chat.completions.create(**data)
        return result

    def request_stream(self, data):
        stream = self.client.chat.completions.create(
            **data
        )
        for chunk in stream:
            if not chunk.choices:
                continue
            yield chunk.choices[0].delta.content
            
    async def arequest_stream(self, data):
        stream = await self.async_client.chat.completions.create(
            **data
        )
        async for chunk in stream:
            if not chunk.choices:
                continue
            yield chunk.choices[0].delta.content


    async def generate2file(self,text: str, 
                            filename = f"tests/resources/work.wav",
                            encoding="wav",
                            voice_type = "zh_female_yuanqinvyou_moon_bigtts"):
        """
        tts text2wav
        """
        cluster = ""
        
        def get_cluster(voice: str) -> str:
            if voice.startswith("S_"):
                return "volcano_icl"
            return "volcano_tts"
        
        # Determine cluster
        cluster = cluster if cluster else get_cluster(voice_type)

        # Connect to server
        headers = {
            "Authorization": f"Bearer;{self.access_token}",
        }

        print(f"Connecting to {self.endpoint} with headers: {headers}")
        websocket = await websockets.connect(
            self.endpoint, additional_headers=headers, max_size=10 * 1024 * 1024
        )
        print(
            f"Connected to WebSocket server, Logid: {websocket.response.headers['x-tt-logid']}",
        )

        try:
            # Prepare request payload
            request = {
                "app": {
                    "appid": self.appid,
                    "token": self.access_token,
                    "cluster": cluster,
                },
                "user": {
                    "uid": str(uuid.uuid4()),
                },
                "audio": {
                    "voice_type": voice_type,
                    "encoding": encoding,
                },
                "request": {
                    "reqid": str(uuid.uuid4()),
                    "text": text,
                    "operation": "submit",
                    "with_timestamp": "1",
                    "extra_param": json.dumps(
                        {
                            "disable_markdown_filter": False,
                        }
                    ),
                },
            }

            # Send request
            await full_client_request(websocket, json.dumps(request).encode())

            # Receive audio data
            audio_data = bytearray()
            while True:
                msg = await receive_message(websocket)

                if msg.type == MsgType.FrontEndResultServer:
                    continue
                elif msg.type == MsgType.AudioOnlyServer:
                    audio_data.extend(msg.payload)
                    if msg.sequence < 0:  # Last message
                        break
                else:
                    raise RuntimeError(f"TTS conversion failed: {msg}")

            # Check if we received any audio data
            if not audio_data:
                raise RuntimeError("No audio data received")

            # Save audio file
            with open(filename, "wb") as f:
                f.write(audio_data)
            print(f"Audio received: {len(audio_data)}, saved to {filename}")

        finally:
            await websocket.close()
            print("Connection closed")


class OpenAIClient:
    """
    使用 openai 官方包对接 OpenAI API，支持简单对话和流式对话
    """

    def __init__(
        self, api_key: str, api_base: str = "https://api.bianxie.ai/v1/chat/completions"
    ):
        """
        初始化 OpenAI 客户端
        url = 'https://api.bianxie.ai/v1/audio/transcriptions'  asr 语音识别
        """
        self.api_key = api_key
        self.api_base = api_base
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

    def request(self, params: dict) -> dict:
        """
        简单对话：直接调用 OpenAI API 并返回完整响应
        """
        api_base = self.api_base
        try:
            response = requests.post(api_base, headers=self.headers, json=params)
            return response.json()
        except Exception as e:
            raise Exception(f"API request failed: {e}") from e

    @retry(
        wait=wait_exponential(
            multiplier=1, min=1, max=10
        ),  # 首次等待1秒，指数增长，最大10秒
        stop=stop_after_attempt(3),  # 最多尝试5次 (1次初始请求 + 4次重试)
        retry=(
            retry_if_exception_type(httpx.RequestError)  # 匹配网络错误 (连接超时, DNS, SSL等)
            | retry_if_exception_type(httpx.HTTPStatusError)  # 匹配HTTP状态码错误
        ),
        # before_sleep=before_sleep_log(logger, logging.INFO),  # 每次重试前打印日志
        reraise=True,  # 如果所有重试都失败，重新抛出最后一个异常
    )
    async def arequest(self, params: dict) -> dict:
        """
        # 修改后的异步请求函数
        简单对话：直接调用 OpenAI API 并返回完整响应 (异步版本)
        """
        api_base = self.api_base
        try:
            time1 = time.time()
            # 使用 httpx.AsyncClient 进行异步请求
            async with httpx.AsyncClient(headers=self.headers) as client:
                response = await client.post(
                    api_base, json=params, timeout=60.0
                )  # 加上timeout是个好习惯
                response.raise_for_status()  # 检查HTTP状态码，如果不是2xx，会抛出异常

            time2 = time.time()
            
            return response.json()

        except httpx.HTTPStatusError as e:
            
            # 这里不要重新抛出新的Exception类型，而是重新抛出原始异常，或者不捕获让tenacity处理
            # 方式一：直接 raise e，tenacity 会捕捉到 httpx.HTTPStatusError
            raise
        except httpx.RequestError as e:
            raise 
        except Exception as e:
            raise Exception(f"API request failed: {e}") from e

    def request_tts(self, params: dict) -> dict:
        """

        params: dict
            - file_path 音频路径  'tests/resources/speech.mp3'
            - model 模型名称 'tts-1'
            - input 输入文本 "你好"
            - voice 声音    "alloy"
        """
        api_base = "https://api.bianxie.ai/v1/audio/speech"
        try:
            time1 = time.time()
            response = requests.post(
                api_base,
                headers=self.headers,
                json={
                    "model": params.get("model"),
                    "input": params.get("input"),
                    "voice": params.get("voice"),
                },
            )
            time2 = time.time()
            if response.status_code == 200:
                with open(params.get("file_path"), "wb") as file:
                    file.write(response.content)
                print(f"Audio saved successfully as {params.get('file_path')}")
            else:
                print(f"Failed to get audio: {response.status_code} - {response.text}")

        except Exception as e:
            raise Exception(f"API request failed: {e}") from e

    async def arequest_tts(self, params: dict) -> dict:
        """
        params: dict
            - file_path 音频路径  'tests/resources/speech.mp3'
            - model 模型名称 'tts-1'
            - input 输入文本 "你好"
            - voice 声音    "alloy"
        """
        try:

            # # 使用 httpx.AsyncClient 进行异步请求
            # async with httpx.AsyncClient(headers=self.headers) as client:
            #     response = await client.post(api_base, json=params, timeout=30.0) # 加上timeout是个好习惯
            #     response.raise_for_status() # 检查HTTP状态码，如果不是2xx，会抛出异常


            time1 = time.time()
            api_base = "https://api.bianxie.ai/v1/audio/speech"
            params = {
                "model": params.get("model"),
                "input": params.get("input"),
                "voice": params.get("voice"),
            }
            # 使用 httpx.AsyncClient 进行异步请求
            async with httpx.AsyncClient(headers=self.headers) as client:
                response = await client.post(
                    api_base, json=params, timeout=30.0
                )  # 加上timeout是个好习惯
                response.raise_for_status()  # 检查HTTP状态码，如果不是2xx，会抛出异常

            time2 = time.time()
            if response.status_code == 200:
                with open(params.get("file_path"), "wb") as file:
                    file.write(response.content)
                print(f"Audio saved successfully as {params.get('file_path')}")
            else:
                print(f"Failed to get audio: {response.status_code} - {response.text}")

        except httpx.HTTPStatusError as e:
            
            raise Exception(
                f"API request failed with HTTP error: {e.response.status_code}"
            ) from e
        except httpx.RequestError as e:
            raise Exception(
                f"API request failed due to network or connection error: {e}"
            ) from e
        except Exception as e:
            raise Exception(f"API request failed: {e}") from e

    def request_asr(self, params: dict) -> dict:
        """

        params: dict
            - file_path 音频路径
            - model 模型名称 'whisper-1'
        """
        api_base = "https://api.bianxie.ai/v1/audio/transcriptions"
        print(params.get("file_path"), 'params.get("file_path")')
        print(params.get("model"), 'params.get("file_path")')
        try:
            with open(params.get("file_path"), "rb") as audio_file:
                
                time1 = time.time()
                response = requests.post(
                    api_base,
                    headers=self.headers,
                    files={"file": audio_file},
                    data={"model": params.get("model")},
                )
                time2 = time.time()
                
            return response.json()
        except Exception as e:
            
            raise Exception(f"API request failed: {e}") from e

    def request_stream(self, params: dict) -> dict:
        """
        简单对话：直接调用 OpenAI API 并返回流式响应
        request_stream_http2
        """
        try:
            self.headers["Accept"] = "text/event-stream"

            payload = params
            with httpx.Client(http2=True, timeout=None) as client:
                with client.stream(
                    "POST", self.api_base, headers=self.headers, json=payload
                ) as response:
                    response.raise_for_status()
                    buffer = b""
                    for chunk in response.iter_bytes():
                        buffer += chunk
                        while b"\n" in buffer:
                            line_bytes, _, buffer = buffer.partition(b"\n")
                            decoded_line = line_bytes.decode("utf-8")

                            if decoded_line.startswith("data:"):
                                json_str = decoded_line[len("data:") :].strip()

                                if json_str == "[DONE]":
                                    return  # End the generator

                                try:
                                    data = json.loads(json_str)
                                    # Extract content based on common LLM API response structure
                                    if "choices" in data and data["choices"]:
                                        chunk_content = data["choices"][0]["delta"].get(
                                            "content", ""
                                        )
                                        if chunk_content:
                                            yield chunk_content  # Yield the generated content chunk
                                except json.JSONDecodeError:
                                    yield f"[ERROR: Malformed data received: {json_str}]"

        except httpx.RequestError as e:
            error_msg = f"Request failed: {e}"
            raise ConnectionError(
                error_msg
            ) from e  # Re-raise as a custom error or simpler Exception
        except Exception as e:
            error_msg = f"An unexpected error occurred: {e}"
            raise RuntimeError(error_msg) from e

    async def arequest_stream(self, params: dict):
        """
        简单对话：直接调用 OpenAI API 并返回流式响应 (异步版本)
        arequest_stream_http2
        """
        try:
            # 设置 Accept 头为 text/event-stream，表示期望流式事件
            self.headers["Accept"] = "text/event-stream"
            payload = params

            # 使用 httpx.AsyncClient 进行异步 HTTP 请求
            # timeout=None 表示不设置请求超时时间，由底层 TCP/TLS 决定
            async with httpx.AsyncClient(http2=True, timeout=None) as client:
                # 发送 POST 请求并获取异步响应流
                async with client.stream(
                    "POST", self.api_base, headers=self.headers, json=payload
                ) as response:
                    # 检查 HTTP 响应状态码，如果不是 2xx，则抛出异常
                    response.raise_for_status()

                    buffer = b""
                    # 异步迭代响应的字节块
                    async for chunk in response.aiter_bytes():
                        buffer += chunk
                        # 处理可能包含多行或不完整行的缓冲区
                        while b"\n" in buffer:
                            line_bytes, _, buffer = buffer.partition(b"\n")
                            decoded_line = line_bytes.decode("utf-8")

                            if decoded_line.startswith("data:"):
                                json_str = decoded_line[len("data:") :].strip()

                                if json_str == "[DONE]":
                                    return  # 结束生成器

                                try:
                                    data = json.loads(json_str)
                                    # 根据常见的 LLM API 响应结构提取内容
                                    if "choices" in data and data["choices"]:
                                        chunk_content = data["choices"][0]["delta"].get(
                                            "content", ""
                                        )
                                        if chunk_content:
                                            # 异步 yield 生成的内容块
                                            yield chunk_content
                                except json.JSONDecodeError:
                                    yield f"[ERROR: Malformed data received: {json_str}]"

        except httpx.RequestError as e:
            error_msg = f"Request failed: {e}"
            # 异步函数中也抛出异常
            raise ConnectionError(error_msg) from e
        except Exception as e:
            error_msg = f"An unexpected error occurred: {e}"
            # 异步函数中也抛出异常
            raise RuntimeError(error_msg) from e

    def request_image_stream(
        self, params: dict, filename_prefix: str = "gemini_output"
    ) -> dict:
        """
        简单对话：直接调用 OpenAI API 并返回流式响应
        params = {
            'model': 'gemini-2.5-flash-image-preview',
            'messages': [{'role': 'user', 'content': 'two dogs in a tree'}],
            'stream': True
        }
        """
        api_base = self.api_base
        try:
            time1 = time.time()
            response = requests.post(
                api_base, headers=self.headers, json=params, stream=True
            )

            # 检查HTTP状态码
            if response.status_code == 200:
                print("Received streaming response:")
                # 逐行处理响应内容
                # iter_lines() 迭代响应内容，按行分割，并解码
                time2 = time.time()
                for line in response.iter_lines():
                    # lines are bytes, convert to string
                    line = line.decode("utf-8")

                    if "![image](data:image/" in line:
                        print(f"生成图片中到 {filename_prefix}")
                        save_base64_image(line, filename_prefix=filename_prefix)

                    # Server-Sent Events (SSE) messages start with 'data: '
                    # and the stream ends with 'data: [DONE]'
                    if line.startswith("data:"):
                        # Extract the JSON string after 'data: '
                        json_str = line[len("data:") :].strip()

                        if json_str == "[DONE]":
                            break  # End of stream

                        if json_str:  # Ensure it's not an empty data line
                            try:
                                # Parse the JSON string into a dictionary
                                chunk = json.loads(json_str)

                                # Extract the content chunk (similar structure to OpenAI API)
                                # Check if choices and delta exist before accessing content
                                if (
                                    chunk
                                    and "choices" in chunk
                                    and len(chunk["choices"]) > 0
                                ):
                                    delta = chunk["choices"][0].get("delta")
                                    if delta and "content" in delta:
                                        content_chunk = delta["content"]
                                        # Print the chunk without a newline, immediately flushing the output
                                        # print(content_chunk, end='', flush=True)
                                        yield content_chunk

                            except json.JSONDecodeError as e:
                                print(
                                    f"\nError decoding JSON chunk: {e}\nChunk: {json_str}"
                                )
                            except Exception as e:
                                print(
                                    f"\nError processing chunk: {e}\nChunk data: {chunk}"
                                )

                print(
                    f"\n(Streaming finished) {time2-time1}"
                )  # Add a newline after the stream is complete

            else:
                # Handle non-200 responses
                print(f"Error: Received status code {response.status_code}")
                print("Response body:")

        except requests.exceptions.RequestException as e:
            # TODO if "439" in ccc
            print(f"Request Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def request_modal(self):
        # TODO 图像理解
        def get_img_content(inputs=str):
            if 0:  # is_url
                return "https://github.com/dianping/cat/raw/master/cat-home/src/main/webapp/images/logo/cat_logo03.png"
            else:

                def image_to_base64(image_path):
                    with open(image_path, "rb") as image_file:
                        image_data = image_file.read()
                        base64_encoded_data = base64.b64encode(image_data)
                        base64_encoded_str = base64_encoded_data.decode("utf-8")
                        return base64_encoded_str

                image_base64 = image_to_base64(inputs)
                return f"data:image/jpeg;base64,{image_base64}"

        data = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "这张图片的图标是个什么动物？"},
                        {
                            "type": "image_url",
                            "image_url": {"url": get_img_content("111.png")},
                        },
                    ],
                }
            ],
        }

        response = requests.post(self.api_base, headers=self.headers, json=data)
        return response.json()









'''


asyncio.run(test_client_arequest_retry_function())

def test_client_request_tts():
    client = OpenAIClient(api_key=os.getenv("BIANXIE_API_KEY"))

    data = {
            "model": "tts-1",
            "input": "你好 世界",
            "voice": "alloy",
            "file_path": 'tests/resources/speech2.mp3',
        }
    response = client.request_tts(data)
    print(response)

async def test_client_arequest_tts():
    client = OpenAIClient(api_key=os.getenv("BIANXIE_API_KEY"))

    params = {
            "model": "tts-1",
            "input": "你好 世界 天气不错",
            "voice": "alloy",
            "file_path": 'tests/resources/speech.mp3',
        }
    response = await client.arequest_tts(params = params)
    print(response)

def test_client_request_asr():
    # 未通过
    client = OpenAIClient(api_key=os.getenv("BIANXIE_API_KEY"))
    params = {
            "model": "whisper-1",
            "file_path": 'tests/resources/speech2.mp3',
        }
    response = client.request_asr(params = params)
    print(response)


def test_client_request_stream():
    client = OpenAIClient(api_key=os.getenv("BIANXIE_API_KEY"))

    params = {
            'model': 'gemini-2.5-flash-image-preview',
            'messages': [{'role': 'user', 'content': '绘制两个小孩的照片'}],
            "temperature": 0.7,
            'stream': True
        }
    response = client.request_image_stream(params,filename_prefix ="tests/resources/gemini_output" )
    for i in response:
        print(i)


'''