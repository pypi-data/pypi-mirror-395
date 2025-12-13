import requests
import json
from typing import Iterator, Dict, Any, Optional, Union, AsyncIterator
import aiohttp
import time
from loguru import logger
from whoischarman.struct.schedule import AIRawConfig

class AIConfig(AIRawConfig):
    def get_instance(self) -> 'AI':
        return AI(self)

class AI:
    def __init__(self, conf:AIConfig):
        """
        初始化 AI 客户端

        Args:
            model: 模型名称 (如 "gpt-3.5-turbo", "claude-3-sonnet")
            api: API 端点 URL
            api_key: API 密钥
            temperature: 温度参数 (0.0-2.0)
            max_tokens: 最大生成 token 数
            timeout: 请求超时时间(秒)
            max_retries: 最大重试次数
        """
        self.conf = conf
        self.api_key = self.conf.api_key
        self.model = self.conf.model
        self.api = self.conf.api.rstrip('/')  # 移除末尾的斜杠
        self.temperature = self.conf.temperature
        self.max_tokens = self.conf.max_tokens
        self.timeout = self.conf.timeout
        self.max_retries = self.conf.max_retries

        # 设置请求头
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "whoischarman-ai-client/1.0"
        }

        if self.conf.api_key:
            self.headers["Authorization"] = f"Bearer {self.conf.api_key}"

        # 创建会话
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _make_request_with_retry(self, method: str, url: str, **kwargs) -> requests.Response:
        """带重试机制的请求方法"""
        for attempt in range(self.max_retries):
            try:
                # 如果传入了自定义headers，需要与默认headers合并
                if 'headers' in kwargs:
                    # 合并默认headers和自定义headers
                    merged_headers = self.headers.copy()
                    merged_headers.update(kwargs['headers'])
                    kwargs['headers'] = merged_headers

                response = self.session.request(method.lower(), url, timeout=self.timeout, **kwargs)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    logger.error(f"Request failed after {self.max_retries} attempts: {e} in {url}")
                    raise
                logger.warning(f"Request attempt {attempt + 1} failed, retrying: {e} in {url}")
                import time
                time.sleep(2 ** attempt)  # 指数退避
        return None

    def chat(self, messages: list[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        非流式聊天 API 调用

        Args:
            messages: 消息列表，格式 [{"role": "user", "content": "..."}, ...]
            **kwargs: 其他参数 (如 stream=False, top_p, frequency_penalty等)

        Returns:
            API 响应的完整内容
        """
        # 构建请求数据
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": False,
            **kwargs
        }

        # 发送请求
        # 检查是否已经包含完整路径
        if "/v1/chat/completions" in self.api:
            url = self.api
        else:
            
            url = f"{self.api.rstrip('/')}/v1/chat/completions"
        self.conf.using = True
        response = self._make_request_with_retry("POST", url, json=data)
        self.conf.using = False
        if response is None:
            raise RuntimeError("Failed to get response from API")

        return response.json()

    def generate_text(self, prompt: str, **kwargs) -> str:
        """
        简化的文本生成方法

        Args:
            prompt: 输入提示
            **kwargs: 其他参数

        Returns:
            生成的文本内容
        """
        messages = [{"role": "user", "content": prompt}]
        self.conf.using = True
        response = self.chat(messages, **kwargs)
        self.conf.using = False

        # 提取生成的内容
        try:

            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            logger.error(f"Failed to extract content from response: {e}")
            return ""

    def chat_stream(self, messages: list[Dict[str, str]], **kwargs) -> Iterator[str]:
        """
        流式聊天 API 调用

        Args:
            messages: 消息列表，格式 [{"role": "user", "content": "..."}, ...]
            **kwargs: 其他参数 (如 stream=True, top_p, frequency_penalty等)

        Yields:
            流式返回的文本片段
        """
        # 构建请求数据
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": True,
            **kwargs
        }

        # 发送流式请求
        if "/v1/chat/completions" in self.api:
            url = self.api
        else:
            url = f"{self.api.rstrip('/')}/v1/chat/completions"

        # 为流式请求添加适当的headers
        stream_headers = self.headers.copy()
        stream_headers["Accept"] = "text/event-stream"
        stream_headers["Cache-Control"] = "no-cache"

        response = self._make_request_with_retry("POST", url, json=data, stream=True, headers=stream_headers)

        if response is None:
            raise RuntimeError("Failed to get response from API")

        # 处理流式响应
        buffer = ""
        thinking = False
        self.conf.using = True
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8').strip()
                if line.startswith('data: '):
                    data_str = line[6:]  # 移除 'data: ' 前缀
                    if data_str == '[DONE]':
                        break
                    try:
                        chunk = json.loads(data_str)
                        if 'choices' in chunk and len(chunk['choices']) > 0:
                            delta = chunk['choices'][0].get('delta', {})
                            # 优先使用 content 字段，如果没有则使用 reasoning_content
                            content = delta.get('content', '')
                            think = delta.get('reasoning_content', '')
                            # print(delta)
                            if content == '' and think is not None:
                                content = think
                                thinking = True
                                if buffer == "":
                                    ASCII_COLOR_GRAY = "\033[38;2;128;128;128m"
                                    content = "🤔" + ASCII_COLOR_GRAY + content
                            else:

                                if thinking:
                                    thinking = False
                                    ASCII_COLOR_END = "\033[0m"
                                    content = ASCII_COLOR_END + "🤔" + content
                            if content:
                                yield content
                                buffer += content
                    except json.JSONDecodeError:
                        continue
        self.conf.using = False
    async def chat_stream_async(self, messages: list[Dict[str, str]], **kwargs) -> AsyncIterator[str]:
        """
        异步流式聊天 API 调用

        Args:
            messages: 消息列表，格式 [{"role": "user", "content": "..."}, ...]
            **kwargs: 其他参数

        Yields:
            异步流式返回的文本片段
        """
        # 构建请求数据
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": True,
            **kwargs
        }

        # 为流式请求添加适当的headers
        stream_headers = self.headers.copy()
        stream_headers["Accept"] = "text/event-stream"
        stream_headers["Cache-Control"] = "no-cache"

        timeout = aiohttp.ClientTimeout(total=self.timeout)
        self.conf.using = True
        async with aiohttp.ClientSession(headers=stream_headers, timeout=timeout) as session:
            # 检查是否已经包含完整路径
            if "/v1/chat/completions" in self.api:
                url = self.api
            else:
                url = f"{self.api.rstrip('/')}/v1/chat/completions"

            async with session.post(url, json=data) as response:
                response.raise_for_status()

                buffer = ""
                thinking = False
                async for line in response.content:
                    line_str = line.decode('utf-8').strip()
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]  # 移除 'data: ' 前缀
                        if data_str == '[DONE]':
                            break
                        try:
                            chunk = json.loads(data_str)
                            if 'choices' in chunk and len(chunk['choices']) > 0:
                                delta = chunk['choices'][0].get('delta', {})
                                                            # 优先使用 content 字段，如果没有则使用 reasoning_content
                                content = delta.get('content', '')
                                think = delta.get('reasoning_content', '')
                                # print(delta)
                                if content == '' and think is not None:
                                    content = think
                                    thinking = True
                                    if buffer == "":
                                        ASCII_COLOR_GRAY = "\033[38;2;128;128;128m"
                                        content = "🤔" + ASCII_COLOR_GRAY + content
                                else:

                                    if thinking:
                                        thinking = False
                                        ASCII_COLOR_END = "\033[0m"
                                        content = ASCII_COLOR_END + "🤔" + content

                                if content:
                                    yield content
                                    buffer += content
                        except json.JSONDecodeError:
                            continue

        self.conf.using = False
    def generate_text_stream(self, prompt: str, **kwargs) -> Iterator[str]:
        """
        简化的流式文本生成方法

        Args:
            prompt: 输入提示
            **kwargs: 其他参数

        Yields:
            流式返回的文本片段
        """
        messages = [{"role": "user", "content": prompt}]
        yield from self.chat_stream(messages, **kwargs)

    async def generate_text_stream_async(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        """
        异步简化的流式文本生成方法

        Args:
            prompt: 输入提示
            **kwargs: 其他参数

        Yields:
            异步流式返回的文本片段
        """
        messages = [{"role": "user", "content": prompt}]
        async for chunk in self.chat_stream_async(messages, **kwargs):
            yield chunk

    def __enter__(self):
        """上下文管理器入口"""
        self.conf.using = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.conf.using = False
        self.session.close()

    def count_tokens(self, text: str) -> int:
        """
        估算文本的 token 数量
        这是一个简单的估算，实际实现需要根据具体模型调整

        Args:
            text: 输入文本

        Returns:
            估算的 token 数量
        """
        # 简单估算：英文约 4 字符/token，中文约 1.5 字符/token
        chinese_chars = len([c for c in text if '\u4e00' <= c <= '\u9fff'])
        non_chinese_chars = len(text) - chinese_chars
        return int(chinese_chars / 1.5 + non_chinese_chars / 4)

    def estimate_cost(self, messages: list[Dict[str, str]], **kwargs) -> Dict[str, float]:
        """
        估算 API 调用成本

        Args:
            messages: 消息列表
            **kwargs: 其他参数

        Returns:
            包含成本估算的字典
        """
        # 计算输入 tokens
        input_text = ""
        for msg in messages:
            input_text += f"{msg.get('role', '')}: {msg.get('content', '')}\n"

        input_tokens = self.count_tokens(input_text)

        # 获取 max_tokens 参数
        max_tokens = kwargs.get('max_tokens', self.max_tokens)

        # 默认费率 (需要根据实际 API 调整)
        input_cost_per_1k = 0.001  # $0.001 per 1k input tokens
        output_cost_per_1k = 0.002  # $0.002 per 1k output tokens

        input_cost = (input_tokens / 1000) * input_cost_per_1k
        output_cost = (max_tokens / 1000) * output_cost_per_1k

        return {
            "input_tokens": input_tokens,
            "output_tokens": max_tokens,
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": input_cost + output_cost
        }

    def close(self):
        """关闭会话"""
        if hasattr(self, 'session'):
            self.session.close()
        