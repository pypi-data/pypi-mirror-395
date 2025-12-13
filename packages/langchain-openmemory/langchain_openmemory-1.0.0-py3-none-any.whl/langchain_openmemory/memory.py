from __future__ import annotations
from typing import Any, Dict, List, Optional, Union, Sequence

from langchain_core.documents import Document
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_core.retrievers import BaseRetriever
from langchain_core.chat_history import BaseChatMessageHistory

from .client import OpenMemoryClient


class Memory(Runnable):
    """
    one-line openmemory integration for langchain.

    example:

        from langchain_openmemory import Memory
        m = Memory()  # no user id required!
        m = Memory("user1")  # optional user id
    """

    def __init__(
        self,
        user: Optional[str] = None,
        *,
        base_url: Optional[str] = None,
        mode: str = "local",
        k: int = 5,
        sectors: Optional[Sequence[str]] = None,
        time: Optional[str] = None,
    ) -> None:
        self.user = user  # none is valid; openmemory handles it
        self.client = OpenMemoryClient(base_url=base_url, mode=mode)
        self.k = k
        self.sectors = list(sectors) if sectors else None
        self.time = time

        self.retriever = _Retriever(self)
        self.history = _ChatHistory(self)

    def invoke(
        self,
        input: Union[str, Dict[str, Any]],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any,
    ) -> str:
        if isinstance(input, dict):
            q = input.get("question") or input.get("input") or ""
        else:
            q = input

        docs = self.retriever.get_relevant_documents(str(q))
        return "\n".join([d.page_content for d in docs])

    def store(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        self.client.store_fact(self.user, content=text, metadata=metadata)

    def __call__(self, query: str) -> List[str]:
        items = self.client.query(
            user_id=self.user,
            query=query,
            k=self.k,
            time=self.time,
            sectors=self.sectors,
        )
        return [i.get("content", "") for i in items]


class _Retriever(BaseRetriever):
    def __init__(self, mem: Memory) -> None:
        self.mem = mem

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: Optional[Any] = None,
    ) -> List[Document]:
        items = self.mem.client.query(
            user_id=self.mem.user,
            query=query,
            k=self.mem.k,
            time=self.mem.time,
            sectors=self.mem.sectors,
        )
        docs: List[Document] = []
        for it in items:
            content = it.get("content") or ""
            meta = it.get("metadata") or {}
            docs.append(Document(page_content=content, metadata=meta))
        return docs


class _ChatHistory(BaseChatMessageHistory):
    def __init__(self, mem: Memory) -> None:
        self.mem = mem

    @property
    def messages(self) -> List[BaseMessage]:
        raw = self.mem.client.list_chat_messages(user_id=self.mem.user)
        out: List[BaseMessage] = []
        for r in raw:
            meta = r.get("metadata") or {}
            role = meta.get("role") or "user"
            content = r.get("content") or ""
            if role == "user":
                out.append(HumanMessage(content=content))
            elif role == "assistant":
                out.append(AIMessage(content=content))
            else:
                out.append(SystemMessage(content=content))
        return out

    def add_message(self, message: BaseMessage) -> None:
        if isinstance(message, HumanMessage):
            role = "user"
        elif isinstance(message, AIMessage):
            role = "assistant"
        elif isinstance(message, SystemMessage):
            role = "system"
        else:
            role = "user"
        self.mem.client.store_message(
            user_id=self.mem.user,
            role=role,
            content=str(message.content),
        )

    def clear(self) -> None:
        self.mem.client.clear_chat(user_id=self.mem.user)
