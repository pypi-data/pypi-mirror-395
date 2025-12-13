import json
import random

import hashlib

import string
from pathlib import Path
from typing import Literal, List
from datetime import datetime
class GeneralToolkit:
    def __init__(self) -> None:
        # 限制最大 JSON 长度为 1MB，防止过大的恶意输入
        self.MAX_JSON_LENGTH = 1024 * 1024

        # 定义不同类型UA对应的文件路径
        self.file_paths = {
            'computer': 'computer_ua.txt',
            'mobile': 'mobile_ua.txt'
        }
        # 获取UA文件所在的目录
        self.ua_dir = Path(__file__).parent / "ua"

        # 初始化时就加载所有UA并缓存
        self.computer_uas = self._read_ua_file('computer')
        self.mobile_uas = self._read_ua_file('mobile')

        # 验证加载结果
        if not self.computer_uas:
            raise ValueError(f"电脑UA文件中没有有效的User-Agent: {self.file_paths['computer']}")
        if not self.mobile_uas:
            raise ValueError(f"手机UA文件中没有有效的User-Agent: {self.file_paths['mobile']}")

    def _read_ua_file(self, device_type: str) -> List[str]:
        """读取指定类型的UA文件并返回非空UA列表"""
        try:
            # 查找对应的文件
            file_path = list(self.ua_dir.glob(self.file_paths[device_type]))[0]

            with open(file_path, 'r', encoding='utf-8') as f:
                # 读取并过滤空行
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            raise FileNotFoundError(f"UA文件不存在: {self.file_paths[device_type]}，请确保文件已创建并包含内容")
        except IndexError:
            raise FileNotFoundError(f"在目录 {self.ua_dir} 中未找到 {self.file_paths[device_type]} 文件")

    def check_common_substrings(self, input_string, substr_list):
        """
        检查字符串是否包含列表中的任何完整子字符串

        参数:
        input_string (str): 需要检查的字符串
        substr_list (list): 用于比较的子字符串列表

        返回:
        bool: 如果存在匹配的子字符串返回 True，否则返回 False
        """
        for substr in substr_list:
            if substr in input_string:
                return True
        return False

    def filter_sensitive_words(self, sensitive_words: list[str], text: str, replacement: str = '*') -> str:
        """
        将文本中的敏感词替换为指定字符串，每个敏感词仅替换一次

        参数:
            sensitive_words: 敏感词列表
            text: 需要过滤的文本
            replacement: 用于替换敏感词的字符串，默认为星号(*)

        返回:
            过滤后的文本
        """
        # 按长度降序排列敏感词，确保长词优先被替换
        sensitive_words = sorted(sensitive_words, key=len, reverse=True)

        filtered_text = text
        for word in sensitive_words:
            filtered_text = filtered_text.replace(word, replacement, 1)  # 仅替换一次

        return filtered_text

    def is_safe_json_structure(self, obj) -> bool:
        """
        验证 JSON 对象结构是否安全（只允许 object 或 array 作为根节点）

        参数:
            obj: 解析后的 JSON 对象

        返回:
            bool: 结构安全返回 True，否则返回 False
        """
        return isinstance(obj, (dict, list))

    def json_format(self, content: str, is_json: bool = True, should_dump: bool = True) -> str | dict | list:
        """
        格式化 JSON 字符串，增加安全性处理

        参数:
            content: 待格式化的字符串
            is_json: 是否强制作为 JSON 处理
            should_dump: 是否对解析后的对象执行 json.dumps，默认为 True

        返回:
            格式化后的 JSON 字符串或解析后的 Python 对象（dict/list）或原始内容

        异常:
            ValueError: 输入不符合 JSON 格式或结构不安全
            TypeError: 输入类型错误
        """
        # 检查输入类型
        if not isinstance(content, str):
            raise TypeError(f"Expected string, got {type(content).__name__}")

        # 检查输入长度
        if len(content) > self.MAX_JSON_LENGTH:
            raise ValueError(f"Input exceeds maximum length of {self.MAX_JSON_LENGTH} characters")

        # 如果明确不是 JSON 且不需要强制处理，直接返回
        if not is_json:
            return content

        try:
            # 解析 JSON
            parsed = json.loads(content)

            # 验证 JSON 结构安全性
            if not self.is_safe_json_structure(parsed):
                raise ValueError("Unsafe JSON structure: root must be object or array")

            # 根据 should_dump 参数决定是否执行 json.dumps
            if should_dump:
                return json.dumps(parsed, indent=4, ensure_ascii=False)
            else:
                return parsed

        except json.JSONDecodeError as e:
            # 处理 JSON 解析错误
            if is_json:
                # 如果强制要求是 JSON，抛出错误
                raise ValueError(f"Invalid JSON format: {str(e)}") from e
            else:
                # 否则返回原始内容
                return content
        except ValueError as e:
            # 重新抛出安全验证错误
            raise ValueError(f"Unsafe JSON structure: {str(e)}") from e
        except Exception as e:
            # 处理其他异常
            raise ValueError(f"Unexpected error processing JSON: {str(e)}") from e

    def get_ua(self, device_type: Literal['computer', 'mobile', 'random'] = 'random') -> str:
        """
        返回指定类型设备的User-Agent（使用预加载的缓存数据）

        参数:
            device_type: 设备类型，可选值为 'computer'(电脑), 'mobile'(手机) 或 'random'(随机)

        返回:
            随机选择的User-Agent字符串
        """
        if device_type == 'computer':
            return random.choice(self.computer_uas)
        elif device_type == 'mobile':
            return random.choice(self.mobile_uas)
        elif device_type == 'random':
            # 随机选择设备类型及其再随机选择UA
            return random.choice(
                self.computer_uas + self.mobile_uas
            )
        else:
            raise ValueError("device_type must be one of 'computer', 'mobile', 'random'")
    def get_headers(self, ua_device_type = 'random') -> dict:
        """返回一个包含随机 User-Agent 的 HTTP 头字典"""
        user_agent = self.get_ua(ua_device_type)
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': user_agent
        }
        return headers

    def get_formatted_time(self) -> str:
        """返回格式为 'YYYY-MM-DD HH:MM:SS' 的当前时间字符串"""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def generate_device_id(self, length: int = 22, segments: int = 3, separator: str = '_') -> str:
        """
        生成随机设备ID，格式类似 "WiRsasjclDTQ2eVSz6_SY"

        Args:
            length: 每个段的字符长度（默认22）
            segments: 段的数量（默认3）
            separator: 段之间的分隔符（默认下划线）

        Returns:
            生成的随机设备ID字符串
        """
        # 允许的字符集合（大小写字母和数字）
        allowed_chars = string.ascii_letters + string.digits

        # 生成每个段的随机字符串
        parts = [
            ''.join(random.choice(allowed_chars) for _ in range(length))
            for _ in range(segments)
        ]

        # 使用分隔符连接各段
        return separator.join(parts)



    def md5_encrypt(self, data: str) -> str:
        md5_obj = hashlib.md5()
        if isinstance(data, str):
            data = data.encode('utf-8')
        md5_obj.update(data)

        return md5_obj.hexdigest()


if __name__ == "__main__":
    common_utils = GeneralToolkit()
    print(common_utils.md5_encrypt(common_utils.md5_encrypt("128524") + "USR2025092602816"))
    