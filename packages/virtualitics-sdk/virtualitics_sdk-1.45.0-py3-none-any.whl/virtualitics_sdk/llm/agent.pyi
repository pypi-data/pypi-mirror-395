import redis.asyncio
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from collections import defaultdict as defaultdict
from virt_llm.inference_engine._types import LLMChatMessage
from virtualitics_sdk import Page as Page
from virtualitics_sdk.llm.types import ActionPageUpdate as ActionPageUpdate, ChatSource as ChatSource, ChatSourceCard as ChatSourceCard, RawChatContext as RawChatContext, StreamActionPageUpdate as StreamActionPageUpdate, StreamChatEnd as StreamChatEnd, StreamEvent as StreamEvent, StreamException as StreamException, StreamExecutingTool as StreamExecutingTool, StreamMessage as StreamMessage, StreamMessageState as StreamMessageState, StreamPageRefresh as StreamPageRefresh, StreamSourceInformation as StreamSourceInformation, StreamThinking as StreamThinking, StreamWaitingForInput as StreamWaitingForInput

logger: Incomplete

class DispatcherAgentInterface(ABC):
    """
    Abstract Base Class for a dispatcher agent.

    This interface defines the contract for agents that handle the lifecycle of a
    chat interaction. This includes pre-processing user prompts, streaming responses
    from a language model, and post-processing the final response.

    It provides hooks (`on_llm_request`, `on_llm_response`) that can be used to
    customize the agent's behavior.
    """
    default_prompts: Incomplete
    redis: Incomplete
    chat_stream_channel: Incomplete
    chat_context: Incomplete
    def __init__(self, *, default_prompts: list[str] | None = None, **kwargs) -> None:
        """
        Initializes the DispatcherAgentInterface.

        :param default_prompts: An optional list of default prompts to be used by the agent.
        """
    async def init(self, redis_client: redis.asyncio.Redis, chat_stream_channel: str, chat_context: RawChatContext):
        """
        Initializes the agent with a Redis client and a channel for streaming.

        This will be called by the platform prior to calling the run function

        :param redis_client: An asynchronous Redis client instance.
        :param chat_stream_channel: The name of the Redis channel to publish stream events to.
        """
    async def publish_message(self, token: str):
        """
        Publish a message token, this will be relayed to the frontend exactly as published
        """
    async def publish_sources(self, sources: list[ChatSourceCard]):
        """
        Publish source_data (clickable chips) from post-processing LLM response
        """
    async def push_response_metadata(self, meta: dict) -> None:
        '''Store data in the final response produced in the current conversation turn.
        If this method is called multiple times, the newly provided meta dict will
        be merged with the old one and already present keys will be overridden.
        
        ```python
            self.push_response_metadata({"counter": 1}) // counter: 1
            self.push_response_metadata({"counter": 5}) // counter: 5
        ```
        
        The last stored metadata can be retrieved in the next conversation turn by using 
        the `get_message_meta` method of this class.

        :param meta: Metadata dictionary to store
        :type meta: dict
        '''
    async def trigger_page_refresh(self):
        """
        Publish a request to refresh the current page
        """
    async def publish_chat_end(self):
        """
        Publish a chat end message that signals the backend to close the chat stream with the frontend
        """
    async def publish_action_page_update(self, page_update_data: ActionPageUpdate):
        """
        Publish a message that triggers a page update action (or filter update action)
        """
    async def publish_thinking(self, msg: str):
        '''Update the IRIS "Thinking" progress text while waiting for the first token.

        :param msg: New text that will replace the original text
        '''
    async def publish_executing_tool(self, tool_name: str): ...
    async def publish_waiting_for_input(self): ...
    async def publish_exception(self, message: str):
        """
        Publish an event to the stream that the frontend can handle as an exception. Not currently fully implemented
        in frontend a/o 1.34.0 but useful for debugging as you can review the exception in the browser console
        """
    @staticmethod
    async def get_message_meta(chat_context: RawChatContext, message_id: int | None = None) -> dict | None:
        """Retrieve the metadata defined in a message. There are two ways of using this method: 
        1. Do not set the `message_id` argument and retrieve the metadata associated with the latest generated
        response, so, the last message saved with the text pushed with the `publish_message` method. 
        2. Set `message_id` and retrieve the metadata associated with a specific message.
        
        In case no metadata is definied, this will return None.
        """
    @staticmethod
    async def get_page_context(chat_context: RawChatContext):
        """
        Retrieve the stored page context from when the current page was executed
        """
    @staticmethod
    async def get_page(chat_context: RawChatContext) -> Page:
        """
        A more performant way to get the page object, which can be useful for retrieving element contents and
        a page representation
        """
    @staticmethod
    def summarize_page(page_context: dict):
        """
        A rudimentary way to express the page which focuses on giving a small amount of context on the page in order to
        best minimize the size of the content
        """
    @abstractmethod
    async def run(self, chat_context: RawChatContext):
        """
        The main entry point for the agent's execution logic.

        Subclasses must implement this method to define how they process a chat request.
        """

class DefaultDispatcherAgent(DispatcherAgentInterface):
    """
    A default, concrete implementation of the `DispatcherAgentInterface`.

    This agent provides a standard workflow for handling chat interactions:
    1.  Pre-processes the user prompt using `on_prompt_received`.
    2.  Streams the response from the language model.
    3.  Post-processes the final response to generate sources.

    It is designed to be used out-of-the-box for simple chat use cases but can be
    customized by overriding the `on_prompt_received` hook during initialization. It is also useful as an
    example implementation of extending the DispatcherAgentInterface
    """
    chat_sources: list[ChatSourceCard]
    def __init__(self, default_prompts: list[str] | None = None) -> None: ...
    async def on_prompt_received(self, chat_context: RawChatContext) -> list[LLMChatMessage]:
        """Prepares the chat messages for the language model.

        This method orchestrates the pre-processing of a user's query by:
        1.  Fetching the full context of the current dashboard page.
        2.  Attempting to identify specific dashboard elements relevant to the user's
            prompt using an LLM-based extraction method.
        3.  If relevant elements are found, the context is filtered to include only
            the data for those elements.
        4.  If no specific elements are identified, a summary of the entire page
            context is generated instead.
        5.  Constructs a final prompt that includes system instructions, the
            processed page context (either filtered data or a summary), and the
            original user question.

        :param chat_context: The raw context of the chat, including the user's prompt.

        :return: A list containing a single `LLMChatMessage` ready to be sent to the LLM
        """
    async def extract_relevant_elements(self, chat_context: RawChatContext, simplified_context: dict):
        '''Identifies dashboard elements relevant to the user\'s question using an LLM.

        This method constructs a specialized prompt that asks the language model to act as a "matching engine." It
        provides the user\'s question and a simplified view of the available dashboard elements (plots, tables, etc.).
        The LLM is instructed to return a JSON array containing the unique IDs of the elements it deems relevant to
        the user\'s query.

        The resulting string from the LLM is then parsed to extract a clean list  of element IDs.

        :param chat_context: The context of the chat, including the user\'s prompt and the LLM client.
        :param simplified_context: A dictionary representing a summarized view of the dashboard elements.

        :return: A list of strings, where each string is the ID of a relevant dashboard element. Returns an empty list
                 if no elements are matched or if an error occurs during processing.
        '''
    def extract_list_from_json(self, json_string: str, retry_count: int = 0) -> list[str]: ...
    async def run(self, chat_context: RawChatContext) -> tuple[list[str], list[dict]]:
        """
        Executes the default chat processing pipeline.

        This method orchestrates the agent's workflow by first preparing the
        messages for the LLM via `on_prompt_received` and then passing them
        to `_stream_chat` to handle the streaming and finally to
        on_final_response for post-processing.

        :param chat_context: The context for the current chat interaction.
        :return: The final, post-processed response from the LLM as a dictionary.
        """

class TestDispatcherAgent(DispatcherAgentInterface):
    """
    Test Interface that streams prompt exactly as given, useful for testing formatting and verifying interactivity
    """
    async def run(self, chat_context: RawChatContext) -> dict: ...
