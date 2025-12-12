import time
import uuid
from typing import List, Optional, Dict, Union, Literal,Annotated
from pydantic import BaseModel, Field, model_validator


class ImageUrl(BaseModel):
    """定义了 image_url 字段的内部结构"""
    url: str

class TextPart(BaseModel):
    """代表类型为 'text' 的内容部分"""
    type: Literal['text']
    text: str

class ImagePart(BaseModel):
    """代表类型为 'image_url' 的内容部分"""
    type: Literal['image_url']
    image_url: ImageUrl

# 使用 "Tagged Union" 来让 Pydantic 根据 'type' 字段自动选择正确的模型
ContentPart = Annotated[
    Union[TextPart, ImagePart],
    Field(discriminator='type')
]

# --- 你的 ChatMessage 和 ChatCompletionRequest 模型 (修改 `content` 字段) ---

class ChatMessage(BaseModel):
    """
    更新后的 ChatMessage，其 content 字段可以接受 str 或 List[ContentPart]，
    并在内部统一为 List[ContentPart]。
    """
    role: Literal["system", "user", "assistant", "tool"]
    # content 字段现在可以接受 str 或 List[ContentPart]
    content: Optional[Union[str, List[ContentPart]]] = None
    # tool_calls: Optional[...] # Add if you support tool/function calling
    # tool_call_id: Optional[...] # Add if you support tool/function calling

    @model_validator(mode='after')
    def normalize_content(self) -> 'ChatMessage':
        """
        验证后标准化 content 字段：
        - 将 str 类型的 content 转换为 [TextPart]。
        - 合并连续的 TextPart。
        """
        if self.content is None:
            return self

        new_content: List[ContentPart] = []
        if isinstance(self.content, str):
            if self.content: # 避免创建空的 text part
                new_content.append(TextPart(type='text', text=self.content))
        else: # self.content is List[ContentPart]
            temp_text_buffer = ""
            for part in self.content:
                if isinstance(part, TextPart):
                    temp_text_buffer += part.text
                else:
                    if temp_text_buffer:
                        new_content.append(TextPart(type='text', text=temp_text_buffer))
                        temp_text_buffer = ""
                    new_content.append(part)
            if temp_text_buffer:
                new_content.append(TextPart(type='text', text=temp_text_buffer))
        
        # 赋值回 self.content，确保它总是 List[ContentPart]
        # Pydantic v2允许在after验证器中修改self
        self.content = new_content
        return self


class ChatCompletionRequest(BaseModel):
    """ x """
    model: str  # The model name you want your service to expose
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1.0
    n: Optional[int] = 1 # How many chat completion choices to generate for each input message.
    stream: Optional[bool] = False
    stop: Optional[Union[str, List[str]]] = None
    max_tokens: Optional[int] = 2048 # Adjusted default for flexibility
    presence_penalty: Optional[float] = 0.0
    frequency_penalty: Optional[float] = 0.0
    logit_bias: Optional[Dict[str, float]] = None
    user: Optional[str] = None
    # Add other parameters if your model supports them (e.g., seed, tool_choice)

# --- Response Models (Non-Streaming) ---

class ChatCompletionMessage(BaseModel):
    """ x """
    role: Literal["assistant", "tool"] # Usually assistant
    content: Optional[str] = None
    # tool_calls: Optional[...]

class Choice(BaseModel):
    """ x """
    index: int
    message: ChatCompletionMessage
    finish_reason: Optional[Literal["stop", "length", "tool_calls",
                                    "content_filter", "function_call"]] = "stop"
    # logprobs: Optional[...]

class UsageInfo(BaseModel):
    """ x """
    prompt_tokens: int = 0 # You might need to implement token counting
    completion_tokens: int = 0
    total_tokens: int = 0

class ChatCompletionResponse(BaseModel):
    """ x """
    id: str = Field(default_factory=lambda: f"chatcmpl-{uuid.uuid4().hex}")
    object: Literal["chat.completion"] = "chat.completion"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str # Echo back the model requested or the one used
    choices: List[Choice]
    usage: UsageInfo = Field(default_factory=UsageInfo)
    # system_fingerprint: Optional[str] = None

# --- Response Models (Streaming) ---

class DeltaMessage(BaseModel):
    """ x """
    role: Optional[Literal["system", "user", "assistant", "tool"]] = None
    content: Optional[str] = None
    # tool_calls: Optional[...]

class ChunkChoice(BaseModel):
    """ x """
    index: int
    delta: DeltaMessage
    finish_reason: Optional[Literal["stop", "length", "tool_calls",
                                    "content_filter", "function_call"]] = None
    # logprobs: Optional[...]

class ChatCompletionChunkResponse(BaseModel):
    """ x """
    id: str = Field(default_factory=lambda: f"chatcmpl-{uuid.uuid4().hex}")
    object: Literal["chat.completion.chunk"] = "chat.completion.chunk"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[ChunkChoice]
    # system_fingerprint: Optional[str] = None
    # usage: Optional[UsageInfo] = None

# --- (Optional) Add other OpenAI-like endpoints if needed ---
# For example, /v1/models to list available models
class ModelCard(BaseModel):
    """ x """
    id: str
    object: Literal["model"] = "model"
    created: int = Field(default_factory=lambda: int(time.time()))
    owned_by: str = "zhaoxuefeng" # Customize as needed

class ModelList(BaseModel):
    """ x """
    object: Literal["list"] = "list"
    data: List[ModelCard] = []