import typing
from .base_client import PinnacleBase, AsyncPinnacleBase

if typing.TYPE_CHECKING:
    from .wrapper.messages.client import EnhancedMessages, AsyncEnhancedMessages
    from .wrapper.tools.client import EnhancedTools, AsyncEnhancedTools


class Pinnacle(PinnacleBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enhanced_messages: typing.Optional["EnhancedMessages"] = None
        self._enhanced_tools: typing.Optional["EnhancedTools"] = None

    @property
    def messages(self) -> "EnhancedMessages":
        if self._enhanced_messages is None:
            from .wrapper.messages.client import EnhancedMessages  # noqa: E402

            self._enhanced_messages = EnhancedMessages(client_wrapper=self._client_wrapper)
        return self._enhanced_messages

    @property
    def tools(self) -> "EnhancedTools":
        if self._enhanced_tools is None:
            from .wrapper.tools.client import EnhancedTools  # noqa: E402

            self._enhanced_tools = EnhancedTools(client_wrapper=self._client_wrapper)
        return self._enhanced_tools


class AsyncPinnacle(AsyncPinnacleBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enhanced_messages: typing.Optional["AsyncEnhancedMessages"] = None
        self._enhanced_tools: typing.Optional["AsyncEnhancedTools"] = None

    @property
    def messages(self) -> "AsyncEnhancedMessages":
        if self._enhanced_messages is None:
            from .wrapper.messages.client import AsyncEnhancedMessages  # noqa: E402

            self._enhanced_messages = AsyncEnhancedMessages(client_wrapper=self._client_wrapper)
        return self._enhanced_messages

    @property
    def tools(self) -> "AsyncEnhancedTools":
        if self._enhanced_tools is None:
            from .wrapper.tools.client import AsyncEnhancedTools  # noqa: E402

            self._enhanced_tools = AsyncEnhancedTools(client_wrapper=self._client_wrapper)
        return self._enhanced_tools
