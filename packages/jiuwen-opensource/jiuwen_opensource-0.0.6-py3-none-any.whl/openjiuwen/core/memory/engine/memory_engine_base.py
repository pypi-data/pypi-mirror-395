from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Tuple
from sqlalchemy import Engine
from openjiuwen.core.memory.config.config import Config, MemoryConfig
from openjiuwen.core.memory.store.base_kv_store import BaseKVStore
from openjiuwen.core.memory.store.base_semantic_store import BaseSemanticStore
from openjiuwen.core.utils.llm.base import BaseModelClient
from openjiuwen.core.utils.llm.messages import BaseMessage


class MemoryEngineBase(ABC):
    """
    Abstract base class defining a unified interface for a memory engine that manages:
    - Conversation history (messages)
    - Semantic/user memories
    - User-defined variables
    - User profiles (topic-based summaries)

    Implementations must support both synchronous and asynchronous message ingestion,
    configurable per-application behavior, and multi-store persistence (SQL, KV, vector).
    """

    def __init__(self, config: Config, llm_base: BaseModelClient = None):
        """
        Initialize the memory engine with global configuration and an optional default LLM client.

        Args:
            config (Config): Global system-wide memory configuration.
            llm_base (BaseModelClient, optional): Default LLM used for memory generation if not overridden per request.
        """
        pass

    @abstractmethod
    def init_mem_store(
        self,
        vector_db_instance: BaseSemanticStore,
        db_engine_instance: Engine,
        kv_db_instance: BaseKVStore
    ):
        """
        Initialize internal managers using provided storage backends.

        This method must be called before any memory operation. It sets up:
        - Message storage (via SQL engine)
        - Semantic/vector search (via vector store)
        - Fast key-value access (for variables, IDs, etc.)

        Args:
            vector_db_instance (BaseSemanticStore): Backend for embedding-based semantic memory.
            db_engine_instance (Engine): SQLAlchemy engine for relational message storage.
            kv_db_instance (BaseKVStore): Key-value store for variables, counters, and metadata.
        """
        pass

    @abstractmethod
    def set_app_config(self, app_id: str, config: MemoryConfig) -> bool:
        """
        Register or update memory-specific configuration for an application.

        Args:
            app_id (str): Unique application identifier.
            config (MemoryConfig): Application-level memory settings (e.g., window size, profile topics).

        Returns:
            bool: True if successfully registered; False if inputs are invalid.
        """
        pass

    @abstractmethod
    def add_conversation_messages(
        self,
        user_id: str,
        app_id: str,
        messages: list[BaseMessage],
        timestamp: datetime | None = None,
        request_config: dict[str, Any] | None = None,
        session_id: str | None = None,
        llm: BaseModelClient | None = None
    ) -> str:
        """
        Synchronously ingest one or more conversation messages and trigger memory generation.

        The engine will:
        1. Store raw messages in message history.
        2. Extract/update user variables, profile, and semantic memories based on configuration.
        3. Return the memory ID of the last stored message.

        Args:
            user_id (str): Unique user identifier.
            app_id (str): Unique application identifier.
            messages (list[BaseMessage]): Non-empty list of messages to process.
            timestamp (datetime, optional): Timestamp for all messages; defaults to current time if omitted.
            request_config (dict, optional): Runtime overrides for memory generation (e.g., custom topics).
            session_id (str, optional): Session grouping key; if omitted, messages are session-agnostic.
            llm (BaseModelClient, optional): LLM to use for memory inference; falls back to engine default.

        Returns:
            str: Memory ID of the last added message. Returns "-1" on failure (e.g., empty messages).

        Raises:
            ValueError: If required managers are not initialized or inputs are malformed.
        """
        pass

    @abstractmethod
    async def aadd_conversation_messages(
        self,
        user_id: str,
        app_id: str,
        messages: list[BaseMessage],
        timestamp: datetime | None = None,
        request_config: dict[str, Any] | None = None,
        session_id: str | None = None,
        llm: BaseModelClient | None = None
    ) -> str:
        """
        Asynchronously ingest conversation messages (see `add_conversation_messages` for semantics).

        This method should behave identically to its synchronous counterpart but executed in an async context.

        Args and Returns: Same as `add_conversation_messages`.
        """
        pass

    @abstractmethod
    def get_recent_message(self, user_id: str, app_id: str, session_id: str | None = None) -> list[Tuple[BaseMessage, datetime]]:
        """
        Retrieve recent conversation messages for a user in an app, optionally scoped to a session.

        Results are typically ordered from newest to oldest, limited by internal retention policy.

        Args:
            user_id (str): User identifier.
            app_id (str): Application identifier.
            session_id (str, optional): If provided, only returns messages from this session.

        Returns:
            list[Tuple[BaseMessage, datetime]]: List of (message, timestamp) pairs.
        """
        pass

    @abstractmethod
    def get_message_by_id(self, msg_id: str) -> Tuple[BaseMessage, datetime]:
        """
        Fetch a specific message by its unique memory ID.

        Args:
            msg_id (str): Unique message identifier assigned during ingestion.

        Returns:
            Tuple[BaseMessage, datetime]: The message object and its associated timestamp.

        Raises:
            KeyError or ValueError: If the message does not exist.
        """
        pass

    @abstractmethod
    def delete_mem_by_id(self, mem_id: str) -> bool:
        """
        Delete a memory entry (message, variable, or profile fragment) by its ID.

        Args:
            mem_id (str): Unique memory identifier.

        Returns:
            bool: True if deletion was attempted/successful (implementation may vary on existence check).
        """
        pass

    @abstractmethod
    def delete_mem_by_user_id(self, user_id: str, app_id: str) -> bool:
        """
        Delete all memory entries (messages, variables, profiles) associated with a user in an app.

        Args:
            user_id (str): User identifier.
            app_id (str): Application identifier.

        Returns:
            bool: True if operation was initiated successfully.
        """
        pass

    @abstractmethod
    def delete_user_profile_by_user_id(self, user_id: str, app_id: str) -> bool:
        """
        Remove only the inferred user profile (not messages or variables) for a given user-app pair.

        Args:
            user_id (str): User identifier.
            app_id (str): Application identifier.

        Returns:
            bool: True if profile deletion was successful.
        """
        pass

    @abstractmethod
    def update_mem_by_id(self, mem_id: str, memory: str) -> bool:
        """
        Update the content of an existing memory entry (e.g., corrected user variable or profile snippet).

        Args:
            mem_id (str): Memory identifier.
            memory (str): New string content to store.

        Returns:
            bool: True if update succeeded.
        """
        pass

    @abstractmethod
    def get_user_variable(self, user_id: str, app_id: str, name: str) -> str:
        """
        Retrieve the value of a named user-defined variable.

        Args:
            user_id (str): User identifier.
            app_id (str): Application identifier.
            name (str): Variable name.

        Returns:
            str: Current value of the variable.

        Raises:
            KeyError: If the variable is not defined.
        """
        pass

    @abstractmethod
    def list_user_variables(self, user_id: str, app_id: str) -> dict[str, str]:
        """
        List all user-defined variables for a user in an application.

        Args:
            user_id (str): User identifier.
            app_id (str): Application identifier.

        Returns:
            dict[str, str]: Mapping from variable names to their string values.
        """
        pass

    @abstractmethod
    def search_user_mem(self, user_id: str, app_id: str, query: str, num: int, threshold: float = 0.3) \
            -> list[dict[str, Any]]:
        """
        Perform semantic similarity search over the user's memory using a natural language query.

        Args:
            user_id (str): User identifier.
            app_id (str): Application identifier.
            query (str): Search query in natural language.
            num (int): Maximum number of results to return.
            threshold (float, optional): Minimum similarity score (e.g., cosine) to include a result.

        Returns:
            list[dict[str, Any]]: List of memory records, each containing metadata (e.g., type, ID, content, score).
        """
        pass

    @abstractmethod
    def list_user_mem(self, user_id: str, app_id: str, num: int, page: int) -> list[dict[str, Any]]:
        """
        Paginated listing of a user’s memory entries (non-semantic, typically chronological).

        Args:
            user_id (str): User identifier.
            app_id (str): Application identifier.
            num (int): Number of entries per page (must be > 0).
            page (int): Page number (typically starting at 1).

        Returns:
            list[dict[str, Any]]: Memory entries for the requested page.
        """
        pass

    @abstractmethod
    def get_user_profile_by_topics(self, user_id: str, app_id: str, topics: list[str]) -> dict[str, str]:
        """
        Retrieve user profile content grouped by specified topics.

        Each topic’s value is a concatenated string of all stored profile snippets under that topic.

        Args:
            user_id (str): User identifier.
            app_id (str): Application identifier.
            topics (list[str]): List of profile topics to retrieve (e.g., ["preferences", "personality"]).

        Returns:
            dict[str, str]: Mapping from topic name to aggregated profile text.
        """
        pass

    @abstractmethod
    def update_user_variable(self, user_id: str, app_id: str, name: str, value: str):
        """
        Create or update a user-defined variable.

        Args:
            user_id (str): User identifier.
            app_id (str): Application identifier.
            name (str): Variable name.
            value (str): Variable value (stored as string).
        """
        pass

    @abstractmethod
    def delete_user_variable(self, user_id: str, app_id: str, name: str):
        """
        Remove a user-defined variable by name.

        Args:
            user_id (str): User identifier.
            app_id (str): Application identifier.
            name (str): Name of the variable to delete.

        Raises:
            KeyError: If the variable does not exist (optional, depending on implementation).
        """
        pass