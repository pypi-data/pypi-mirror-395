"""
模型适配器
"""
from abc import ABC
import os
from typing import Iterator, Generator,AsyncIterator ,AsyncGenerator
from modusched.client import OpenAIClient, ArkClient
from modusched.utils import image_to_base64, is_url_urllib
import logging
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
import os

class ResourceExhaustedError(Exception):
    """Raised when a resource's quota has been exceeded."""

    def __init__(self, message="Token quota has been exhausted."):
        self.message = message
        super().__init__(self.message)

class Adapter():
    """ 总适配器 """
    def __init__(
        self,
        model_name: str = "gemini-2.5-flash-preview-05-20-nothinking",
        type = "openai",
        api_key: str = None,
        api_base: str = "https://api.bianxie.ai/v1/chat/completions",
        tools = [],
        system_prompt = "",
        **kwargs,
    ):
        """初始化
        正常情况下, 这两个参数都不需要传入, 而是会自动寻找环境变量,除非要临时改变api_key.
            api_base 不需要特别指定
        Args:
            api_key (str): API key for authentication.
            api_base (str): Base URL for the API endpoint.
        """
        super().__init__()
        """You are an expert researcher. Your job is to conduct thorough research and then write a polished report.

        You have access to an internet search tool as your primary means of gathering information.

        ## `add_func`

        Use this to add two numbers.

        ## `weather`

        Use this to get the weather.
        """
        self.model_name = model_name
        self.temperature = 0.1
        self.type = type

        if type == "openai":
            self.client = OpenAIClient(api_key=api_key or os.getenv("BIANXIE_API_KEY"), api_base=api_base,**kwargs)
        elif type == "ark":
            self.client = ArkClient(api_key=api_key or os.getenv("ARK_API_KEY"),**kwargs)
        elif type == "agent":
            self.model = init_chat_model(
            model=f"openai:{model_name}",
            api_key=api_key or os.getenv("BIANXIE_API_KEY"),
            base_url="https://api.bianxieai.com/v1",
            )
            self.agent = create_deep_agent(
                model=self.model,
                tools=tools,
                system_prompt=system_prompt,
                **kwargs
            )

    def predict(self, 
                     prompt: str = "", 
                     system_prompt : str = "",
                     messages:list[dict] = None,
                     **kwargs) -> str:

        if messages is None:
            assert prompt
            data = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}] if system_prompt else
                    [{"role": "user", "content": prompt}],
                "temperature": self.temperature,
                **kwargs
            }
        else:
            data = {
                "model": self.model_name,
                "messages": messages,
                "temperature": self.temperature,
                **kwargs
            }

        if self.type == "agent":
            response = self.agent.invoke(data)
        else:
            response = self.client.request(data)
        return self._deal_response(response=response, type = self.type)
        
    async def apredict(self, 
                    prompt: str = None, 
                    system_prompt : str = None,
                    messages:list[dict] = None,
                    **kwargs) -> str:
        
        if messages is None:
            assert prompt
            data = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}] if system_prompt else
                    [{"role": "user", "content": prompt}],
                "temperature": self.temperature,
                **kwargs
            }
        else:
            data = {
                "model": self.model_name,
                "messages": messages,
                "temperature": self.temperature,
                **kwargs
            }
        if self.type == "agent":
            response = await self.agent.ainvoke(data)
        else:
            response = await self.client.arequest(data)
        return self._deal_response(response=response, type = self.type)
    
    def stream(self, 
                prompt: str = None, 
                system_prompt : str = None,
                messages:list[dict] = None,
                **kwargs) -> Iterator[str]:
        
        if messages is None:
            assert prompt
            data = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}] if system_prompt else
                    [{"role": "user", "content": prompt}],
                "temperature": self.temperature,
                "stream": True,
                **kwargs
            }
        else:
            data = {
                "model": self.model_name,
                "messages": messages,
                "temperature": self.temperature,
                "stream": True,
                **kwargs
            }
        if self.type == "agent":
            response = self.agent.stream(data,stream_mode = "messages")
            for msg, metadata in response:
                yield msg.content
        else:
            response = self.client.request_stream(data)
            for i in response:
                yield i
            
    async def astream(self, 
                prompt: str = None, 
                system_prompt : str = None,
                messages:list[dict] = None,
                **kwargs):
        
        if messages is None:
            assert prompt
            data = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}] if system_prompt else
                    [{"role": "user", "content": prompt}],
                "temperature": self.temperature,
                "stream": True,
                **kwargs
            }
        else:
            data = {
                "model": self.model_name,
                "messages": messages,
                "temperature": self.temperature,
                "stream": True,
                **kwargs
            }
        if self.type == "agent":
            response = self.agent.astream(data,stream_mode = "messages")
            async for msg, metadata in response:
                yield msg.content
        else:
            response = self.client.arequest_stream(data)
            async for i in response:
                yield i
        
        
    def _deal_response(self, response, type):
        """
        处理事件的相应
        """
        if type == "openai":
            choices = response.get("choices")
            if choices:
                content = choices[0].get("message").get("content")
                return content
            else:
                raise ResourceExhaustedError(f"{response.get('error')}")
        elif type == "ark":
            return response.choices[0].message.content
        elif type == "agent":
            return response["messages"][-1].content

    # TODO work down
    def product_image_stream(self, prompt: str, image_path: str) -> Iterator[str]:
        """Generate a response from the model based on a single prompt.
        # TODO

        Args:
            prompt (str): The input text prompt to generate a response for.

        Returns:
            str: The response generated by the model.

        image_path : 文件路径 或者 url
        """
        assert self.type == 'openai'
        if is_url_urllib(image_path):
            image_content = image_path
        else:
            image_base64 = image_to_base64(image_path)
            image_content = f"data:image/jpeg;base64,{image_base64}"

        assert self.model_name in [
            "gemini-2.5-flash-image-preview",
            "gemini-2.0-flash-preview-image-generation",
        ]
        data = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_content}},
                    ],
                }
            ],
            "temperature": self.temperature,
            "stream": True,
        }

        if not self._assert_prompt(prompt):
            yield ""
        else:
            result_stream = self.client.request_image_stream(data)
            for i in result_stream:
                yield i

    def image_predict(self,messages):
        result_stream = self.client.request_image_stream(messages)
        for i in result_stream:
            yield i


    async def tts(self,text: str,filename:str, encoding="wav",voice_type = "zh_female_yuanqinvyou_moon_bigtts"):
        """
        
        """
        assert self.type == 'ark'
        await self.client.generate2file(text = text,
                                  filename = filename,
                                  encoding=encoding,
                                  voice_type = voice_type)
      
############################################################################################


class BianXieAgentAdapter():
    def __init__(
        self,
        model_name: str = "gemini-2.5-flash-preview-05-20-nothinking",
        tools = [],
        system_prompt = "",
        api_key: str = None,
        api_base: str = None,
    ):
        """初始化
        正常情况下, 这两个参数都不需要传入, 而是会自动寻找环境变量,除非要临时改变api_key.
            api_base 不需要特别指定
        Args:
            api_key (str): API key for authentication.
            api_base (str): Base URL for the API endpoint.
        """
        # super().__init__()
        self.model = init_chat_model(
            model=f"openai:{model_name}",
            api_key=api_key or os.getenv("BIANXIE_API_KEY"),
            base_url=api_base or os.getenv("BIANXIE_BASE") or "https://api.bianxieai.com/v1",
        )
        self.agent = create_deep_agent(
            model=self.model,
            tools=tools,
            system_prompt=system_prompt or """You are an expert researcher. Your job is to conduct thorough research and then write a polished report.

You have access to an internet search tool as your primary means of gathering information.

## `add_func`

Use this to add two numbers.

## `weather`

Use this to get the weather.
"""
        )
        logging.warning("即将废弃, 请使用Adapter")
    
    async def apredict(self,prompt):
        # result = agent.invoke({"messages": [{"role": "user", "content": "what weather is it like in new york?"}]})
        result = await self.agent.ainvoke({"messages": [{"role": "user", "content": prompt}]})
        return result["messages"][-1].content

    def predict(self,prompt):
        result = self.agent.invoke({"messages": [{"role": "user", "content": prompt}]})
        return result["messages"][-1].content

    async def apredict_dict(self,messages:list[dict],**kwargs):
        data = {
            "messages": messages,
            **kwargs
                }
        result = await self.agent.ainvoke(data)
        return result["messages"][-1].content

    def predict_dict(self,messages:list[dict],**kwargs):
        data = {
            "messages": messages,
            **kwargs
                }
        result = self.agent.invoke(data)
        return result["messages"][-1].content
    
    async def apredict_stream_dict(self,messages:list[dict],**kwargs):
        data = {
            "messages": messages,
            **kwargs
                }
        return self.agent.astream(data,stream_mode = "updates")
        

    def predict_stream_dict(self,messages:list[dict],**kwargs):
        data = {
            "messages": messages,
            **kwargs
                }
        return self.agent.stream(data,stream_mode = "updates")
        


class ModelAdapter(ABC):
    """语言大模型的抽象类"""

    def __init__(self):
        self.api_key = None
        self.temperature = 0.7
        self.client = None
        self.model_name = None
        self.model_advice = []

    def set_temperature(self, temperature: float):
        """用于设置模型的temperature

        Args:
            temperature (float): model temperature
        """
        self.temperature = temperature

    def get_model(self) -> list[str]:
        """获得当前的 model_advice

        Returns:
            list[str]: models
        """
        return self.model_advice

    def product(self, prompt: str) -> str:
        """子类必须实现的类, 用于和大模型做非流式交互

        Args:
            prompt (str): 提示词

        Raises:
            NotImplementedError: pass

        Returns:
            str: 大模型返回的结果
        """
        raise NotImplementedError("This method should be implemented by subclasses")

    def chat(self, messages: list) -> str:
        """子类必须实现的类, 用于和大模型做聊天交互

        Returns:
            str: 大模型返回的结果
        """
        raise NotImplementedError("This method should be implemented by subclasses")

class BianXieAdapter(ModelAdapter):
    """BianXie格式的适配器"""

    def __init__(
        self,
        model_name: str = "gemini-2.5-flash-preview-05-20-nothinking",
        api_key: str = None,
        api_base: str = "https://api.bianxie.ai/v1/chat/completions",
    ):
        """初始化
        正常情况下, 这两个参数都不需要传入, 而是会自动寻找环境变量,除非要临时改变api_key.
            api_base 不需要特别指定
        Args:
            api_key (str): API key for authentication.
            api_base (str): Base URL for the API endpoint.
        """
        super().__init__()
        self.client = OpenAIClient(
            api_key=api_key or os.getenv("BIANXIE_API_KEY"), api_base=api_base
        )
        self.model_name = model_name
        self.model_advice = [
            "gemini-2.5-flash-preview-05-20-nothinking",
            "gemini-2.5-flash-preview-04-17-nothinking",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-0125",
            "gpt-4.1",
            "gpt-4.1-2025-04-14",
            "gpt-4.1-mini",
            "gpt-4.1-mini-2025-04-14",
            "gpt-4.1-nano",
            "gpt-4.1-nano-2025-04-14",
            "gpt-4o",
            "gpt-4o-2024-11-20",
            "gpt-4o-audio-preview",
            "gpt-4o-audio-preview-2024-10-01",
            "gpt-4o-audio-preview-2024-12-17",
            "gpt-4o-all",
            "gpt-4o-image",
            "gpt-4o-image-vip",
            "gpt-4o-mini",
            "gpt-4o-mini-2024-07-18",
            "gpt-4o-mini-audio-preview",
            "gpt-4o-mini-audio-preview-2024-12-17",
            "gpt-4o-mini-realtime-preview",
            "gpt-4o-mini-realtime-preview-2024-12-17",
            "gpt-4o-mini-search-preview",
            "gpt-4o-mini-search-preview-2025-03-11",
            "gpt-4o-realtime-preview",
            "gpt-4o-realtime-preview-2024-10-01",
            "gpt-4o-realtime-preview-2024-12-17",
            "gpt-4o-search-preview-2025-03-11",
            "gpt-4o-search-preview",
            "claude-3-5-haiku-20241022",
            "claude-3-5-haiku-latest",
            "claude-3-5-sonnet-20240620",
            "claude-3-5-sonnet-20241022",
            "claude-3-5-sonnet-20241022-all",
            "claude-3-5-sonnet-all",
            "claude-3-5-sonnet-latest",
            "claude-3-7-sonnet-20250219",
            "claude-3-7-sonnet-20250219-thinking",
            "claude-3-haiku-20240307",
            "claude-opus-4-20250514",
            "claude-opus-4-20250514-thinking",
            "claude-sonnet-4-20250514",
            "claude-sonnet-4-20250514-thinking",
            "coder-claude3.5-sonnet",
            "coder-claude3.7-sonnet",
            "gemini-2.0-flash",
            "gemini-2.0-flash-exp",
            "gemini-2.0-flash-exp-image-generation",
            "gemini-2.0-flash-thinking-exp",
            "gemini-2.0-flash-thinking-exp-01-21",
            "gemini-2.0-pro-exp-02-05",
            "gemini-2.5-flash-preview-04-17",
            "gemini-2.5-flash-preview-04-17-thinking",
            "gemini-2.5-pro-exp-03-25",
            "gemini-2.5-pro-preview-03-25",
            "gemini-2.5-pro-preview-03-25-thinking",
            "gemini-2.5-pro-preview-05-06",
            "gemini-2.5-pro-preview-05-06-thinking",
            "gemini-2.5-pro-preview-06-05",
            "gemini-2.5-pro-preview-06-05-thinking",
            "deepseek-ai/DeepSeek-R1",
            "deepseek-ai/DeepSeek-V3",
            "deepseek-chat",
            "deepseek-r1",
            "deepseek-r1-250528",
            "deepseek-reasoner",
            "grok-3",
            "grok-3-beta",
            "grok-3-deepsearch",
            "grok-3-mini-beta",
            "grok-3-fast-beta",
            "grok-3-mini-fast-beta",
            "grok-3-reasoner",
            "grok-beta",
            "grok-vision-beta",
            "o1-mini",
            "o1-mini-2024-09-12",
            "o3-mini",
            "o3-mini-2025-01-31",
            "o3-mini-all",
            "o3-mini-high",
            "o3-mini-low",
            "o3-mini-medium",
            "o4-mini",
            "o4-mini-2025-04-16",
            "o4-mini-high",
            "o4-mini-medium",
            "o4-mini-low",
            "text-embedding-ada-002",
            "text-embedding-3-small",
            "text-embedding-3-large",
            "deepseek-v3",
            "gpt-5",
        ]
        logging.warning("即将废弃, 请使用Adapter")

    def product(self, prompt: str, system_prompt : str = None, **kwargs) -> str:
        """Generate a response from the model based on a single prompt.

        Args:
            prompt (str): The input text prompt to generate a response for.

        Returns:
            str: The response generated by the model.
        """

        data = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}] if system_prompt else
                [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            **kwargs
        }
        response = self.client.request(data)
        return self._deal_response(response=response)
    
    def product_dict(self, messages:list[dict],**kwargs) -> str:
        """Generate a response from the model based on a single prompt.

        Args:
            prompt (str): The input text prompt to generate a response for.

        Returns:
            str: The response generated by the model.
        """

        data = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            **kwargs
        }
        response = self.client.request(data)
        return self._deal_response(response=response)
    
    async def aproduct(self, prompt: str, system_prompt : str = None, **kwargs) -> str:
        """Generate a response from the model based on a single prompt.

        Args:
            prompt (str): The input text prompt to generate a response for.

        Returns:
            str: The response generated by the model.
        """
        data = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}] if system_prompt else
                [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            **kwargs
        }
        response = await self.client.arequest(data)
        return self._deal_response(response=response)

    async def aproduct_dict(self, messages:list[dict], **kwargs) -> str:
        """Generate a response from the model based on a single prompt.

        Args:
            prompt (str): The input text prompt to generate a response for.

        Returns:
            str: The response generated by the model.
        """
        data = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            **kwargs
        }
        response = await self.client.arequest(data)
        return self._deal_response(response=response)

    def product_stream(self, prompt: str, system_prompt : str = None, **kwargs) -> Iterator[str]:
        """Generate a response from the model based on a single prompt.

        Args:
            prompt (str): The input text prompt to generate a response for.

        Returns:
            str: The response generated by the model.
        """
        data = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}] if system_prompt else
                [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "stream": True,
            **kwargs
        }
        if not self._assert_prompt(prompt):
            yield ""
        else:
            result_stream = self.client.request_stream(data)
            for i in result_stream:
                yield i

    async def aproduct_stream(self, prompt: str, system_prompt : str = None,**kwargs) -> AsyncIterator[str]:
        """Generate a response from the model based on a single prompt.

        Args:
            prompt (str): The input text prompt to generate a response for.

        Returns:
            str: The response generated by the model.
        """
        data = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}] if system_prompt else
                [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "stream": True,
            **kwargs
        }
        async for i in self.client.arequest_stream(data):
            yield i

    async def aproduct_stream_dict(self, messages:list[dict],**kwargs) -> AsyncIterator[str]:
        """Generate a response from the model based on a single prompt.

        Args:
            prompt (str): The input text prompt to generate a response for.

        Returns:
            str: The response generated by the model.
        """
        data = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "stream": True,
            **kwargs
        }
        async for i in self.client.arequest_stream(data):
            yield i

    def product_image_stream(self, prompt: str, image_path: str) -> Iterator[str]:
        """Generate a response from the model based on a single prompt.
        # TODO

        Args:
            prompt (str): The input text prompt to generate a response for.

        Returns:
            str: The response generated by the model.

        image_path : 文件路径 或者 url
        """
        if is_url_urllib(image_path):
            image_content = image_path
        else:
            image_base64 = image_to_base64(image_path)
            image_content = f"data:image/jpeg;base64,{image_base64}"

        assert self.model_name in [
            "gemini-2.5-flash-image-preview",
            "gemini-2.0-flash-preview-image-generation",
        ]
        data = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_content}},
                    ],
                }
            ],
            "temperature": self.temperature,
            "stream": True,
        }

        if not self._assert_prompt(prompt):
            yield ""
        else:
            result_stream = self.client.request_image_stream(data)
            for i in result_stream:
                yield i

    def _assert_prompt(self, prompt):
        try:
            assert prompt != ""
            return True
        except AssertionError:
            return False

    def _deal_response(self, response):
        """
        处理事件的相应
        """
        choices = response.get("choices")
        if choices:
            content = choices[0].get("message").get("content")
            return content
        else:
            raise ResourceExhaustedError(f"{response.get('error')}")

class ArkAdapter(ModelAdapter):
    def __init__(
        self,
        model_name: str = "doubao-1-5-pro-256k-250115",
        api_key: str = None,
        api_base: str = None,
    ):
        """初始化

        Args:
            api_key (str): API key for authentication.
            api_base (str): Base URL for the API endpoint.
        """
        super().__init__()

        self.client = ArkClient(api_key=api_key or os.getenv("ARK_API_KEY"))
        self.model_advice = ["doubao-1-5-pro-256k-250115","doubao-1-5-pro-32k-250115"]
        self.model_name = model_name
        logging.warning("即将废弃, 请使用Adapter")
        

    def product(self, prompt: str, system_prompt : str = None, **kwargs) -> str:
        """Generate a response from the model based on a single prompt.

        Args:
            prompt (str): The input text prompt to generate a response for.

        Returns:
            str: The response generated by the model.
        """
        data = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}] if system_prompt else
                [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            **kwargs
        }
        response = self.client.request(data)

        return response.choices[0].message.content
        # return self._deal_response(response=response)

    async def aproduct(self, prompt: str, system_prompt : str = None, **kwargs) -> str:
        """Generate a response from the model based on a single prompt.

        Args:
            prompt (str): The input text prompt to generate a response for.

        Returns:
            str: The response generated by the model.
        """
        data = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}] if system_prompt else
                [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            **kwargs
        }
        response = await self.client.arequest(data)

        return response.choices[0].message.content
        # return self._deal_response(response=response)


    def product_stream(self, prompt: str, system_prompt : str = None, **kwargs) -> Generator[str, None, None]:
        """Generate a response from the model based on a single prompt.

        Args:
            prompt (str): The input text prompt to generate a response for.

        Returns:
            str: The response generated by the model.
        """
        data = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}] if system_prompt else
                [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "stream": True,
            **kwargs
        }
        response = self.client.request_stream(data)
        for chunk in response:
            yield chunk

    async def aproduct_stream(self, prompt: str, system_prompt : str = None,**kwargs) -> AsyncGenerator[str, None]:
        """Generate a response from the model based on a single prompt.

        Args:
            prompt (str): The input text prompt to generate a response for.

        Returns:
            str: The response generated by the model.
        """
        data = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}] if system_prompt else
                [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "stream": True,
            **kwargs
        }
        response = self.client.arequest_stream(data)
        async for chunk in response:
            yield chunk
    

    async def tts(self,text: str,filename:str, encoding="wav",voice_type = "zh_female_yuanqinvyou_moon_bigtts"):
        """
        
        """
        await self.client.generate2file(text = text,
                                  filename = filename,
                                  encoding=encoding,
                                  voice_type = voice_type)

