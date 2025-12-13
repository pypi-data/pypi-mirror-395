from dataclasses import dataclass
from typing import List, Literal, Optional


@dataclass
class Message:
    role: Literal["user", "assistant", "system"]
    content: str


@dataclass
class ChatRequest:
    messages: List[Message]
    model: str = "Nous-20B"
    temperature: float = 0.7
    max_tokens: int = 512


@dataclass
class Usage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class ChatChoice:
    index: int
    message: Message
    finish_reason: str


@dataclass
class ChatResponse:
    id: str
    object: str
    model: str
    choices: List[ChatChoice]
    usage: Usage
