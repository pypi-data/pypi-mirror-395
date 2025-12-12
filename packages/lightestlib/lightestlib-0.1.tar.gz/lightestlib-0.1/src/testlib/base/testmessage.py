from enum import Enum
from typing import Any, Dict, Optional
from datetime import datetime
import json


class TestMessageType(Enum):
    """
    Enum for test message types.

    This enumeration defines the different types of messages that can be used
    in the testlib framework for categorizing test output.

    测试消息类型枚举

    该枚举定义了在testlib框架中用于分类测试输出的不同消息类型。
    """

    MESSAGE = "TEST"
    INFO = "INFO"
    WARNING = "WARNING"
    DEBUG = "DEBUG"

    def __str__(self) -> str:
        """
        Get string representation of the message type.

        Returns:
            str: String representation of the message type.

        获取消息类型的字符串表示。

        返回:
            str: 消息类型的字符串表示。
        """
        return self.value


class TestMessage:
    """
    Test message class for encapsulating test information.

    This class is used to encapsulate various information generated during
    the testing process, including the message type, content, timestamp,
    and additional details.

    测试消息类，用于封装测试过程中的各种信息

    该类用于封装测试过程中生成的各种信息，包括消息类型、内容、时间戳
    和其他详细信息。
    """

    def __init__(
        self,
        message_type: TestMessageType,
        content: str,
        timestamp: Optional[datetime] = None,
        details: Optional[Dict[str, Any]] = None,
        *args,
        **kwargs,
    ):
        """
        Initialize a TestMessage instance.

        Args:
            message_type (TestMessageType): The type of the message.
            content (str): The main content of the message.
            timestamp (datetime, optional): The timestamp of the message. Defaults to current time.
            details (Dict[str, Any], optional): Additional details of the message.
            *args: Additional positional arguments that will be added to details.
            **kwargs: Additional keyword arguments that will be added to details.

        初始化TestMessage实例。

        参数:
            message_type (TestMessageType): 消息的类型。
            content (str): 消息的主要内容。
            timestamp (datetime, optional): 消息的时间戳。默认为当前时间。
            details (Dict[str, Any], optional): 消息的附加详细信息。
            *args: 将被添加到details中的附加位置参数。
            **kwargs: 将被添加到details中的附加关键字参数。
        """
        self.type = message_type
        self.content = content
        self.timestamp = timestamp or datetime.now()
        self.details = details or {}

        # 将位置参数添加到details中
        if args:
            self.details["args"] = args

        # 将关键字参数添加到details中（如果details中没有同名键）
        for key, value in kwargs.items():
            if key not in self.details:
                self.details[key] = value
        if "name" in self.details and self.details["name"] is None:
            self.name = self.details["name"]
        if "status" in self.details and self.details["status"] is None:
            self.status = self.details["status"]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the message to dictionary format.

        Returns:
            Dict[str, Any]: Dictionary representation of the message.

        将消息转换为字典格式。

        返回:
            Dict[str, Any]: 消息的字典表示。
        """
        return {
            "type": self.type.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "details": self.details,
        }

    def to_json(self) -> str:
        """
        Convert the message to JSON format.

        Returns:
            str: JSON representation of the message.

        将消息转换为JSON格式。

        返回:
            str: 消息的JSON表示。
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def __str__(self) -> str:
        """
        Get string representation of the message.

        Returns:
            str: String representation of the message.

        获取消息的字符串表示。

        返回:
            str: 消息的字符串表示。
        """
        base_info = f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {self.type.value.upper()}: {self.content}"
        return base_info
