from __future__ import annotations
from typing import Any, Dict, List, Optional

try:
    from openmemory import Memory as _OMMemory
except ImportError as e:
    _OMMemory = None
    _IMPORT_ERROR = e
else:
    _IMPORT_ERROR = None


class OpenMemoryClient:
    def __init__(self, base_url: Optional[str] = None, mode: str = "local") -> None:
        if _OMMemory is None:
            raise ImportError(
                "openmemory python package is not installed. "
                "install it with `pip install openmemory`."
            ) from _IMPORT_ERROR
        self._client = _OMMemory(base_url=base_url, mode=mode)

    def store_message(
        self,
        user_id: Optional[str],
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        m = metadata or {}
        m.setdefault("kind", "chat_message")
        m.setdefault("role", role)
        self._client.store(user_id=user_id, content=content, metadata=m)

    def store_fact(
        self,
        user_id: Optional[str],
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        m = metadata or {}
        m.setdefault("kind", "fact")
        self._client.store(user_id=user_id, content=content, metadata=m)

    def clear_chat(self, user_id: Optional[str]) -> None:
        try:
            self._client.clear(user_id=user_id, filter={"kind": "chat_message"})
        except AttributeError:
            pass

    def list_chat_messages(
        self,
        user_id: Optional[str],
        limit: int = 200,
    ) -> List[Dict[str, Any]]:
        res = self._client.query(
            user_id=user_id,
            query="*",
            k=limit,
            filter={"kind": "chat_message"},
            order_by="created_at",
        )
        return getattr(res, "items", res)

    def query(
        self,
        user_id: Optional[str],
        query: str,
        k: int = 8,
        time: Optional[str] = None,
        sectors: Optional[list[str]] = None,
    ) -> List[Dict[str, Any]]:
        payload: Dict[str, Any] = {
            "user_id": user_id,
            "query": query,
            "k": k,
        }
        if time is not None:
            payload["time"] = time
        if sectors:
            payload["sectors"] = sectors
        res = self._client.query(**payload)
        return getattr(res, "items", res)
