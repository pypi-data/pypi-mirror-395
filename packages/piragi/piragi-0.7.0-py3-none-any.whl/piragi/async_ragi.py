"""Async wrapper for Ragi - non-blocking API for web frameworks."""

import asyncio
from typing import Any, Dict, List, Optional, Union

from .core import Ragi
from .stores import VectorStoreProtocol
from .types import Answer


class AsyncRagi:
    """
    Async wrapper around Ragi for use with async web frameworks.

    Provides non-blocking versions of all Ragi methods by running them
    in a thread executor. Use this with FastAPI, Starlette, aiohttp, etc.

    Examples:
        >>> from piragi import AsyncRagi
        >>>
        >>> kb = AsyncRagi("./docs")
        >>> answer = await kb.ask("How do I deploy?")
        >>>
        >>> # With FastAPI
        >>> @app.post("/ingest")
        >>> async def ingest(files: list[str]):
        >>>     await kb.add(files)
        >>>     return {"status": "done"}
    """

    def __init__(
        self,
        sources: Union[str, List[str], None] = None,
        persist_dir: str = ".piragi",
        config: Optional[Dict[str, Any]] = None,
        store: Union[str, Dict[str, Any], VectorStoreProtocol, None] = None,
        graph: bool = False,
    ) -> None:
        """
        Initialize AsyncRagi with optional document sources.

        Args:
            sources: File paths, URLs, or glob patterns to load
            persist_dir: Directory to persist vector database
            config: Configuration dict (see Ragi for options)
            store: Vector store backend
            graph: Enable knowledge graph
        """
        self._sync = Ragi(
            sources=sources,
            persist_dir=persist_dir,
            config=config,
            store=store,
            graph=graph,
        )

    async def add(self, sources: Union[str, List[str]]) -> "AsyncRagi":
        """
        Add documents to the knowledge base (non-blocking).

        Args:
            sources: File paths, URLs, or glob patterns

        Returns:
            Self for chaining
        """
        await asyncio.to_thread(self._sync.add, sources)
        return self

    async def ask(
        self,
        query: str,
        top_k: int = 5,
        system_prompt: Optional[str] = None,
    ) -> Answer:
        """
        Ask a question and get an answer with citations (non-blocking).

        Args:
            query: Question to ask
            top_k: Number of relevant chunks to retrieve
            system_prompt: Optional custom system prompt

        Returns:
            Answer with citations
        """
        return await asyncio.to_thread(
            self._sync.ask, query, top_k, system_prompt
        )

    async def retrieve(self, query: str, top_k: int = 5) -> List:
        """
        Retrieve relevant chunks without LLM generation (non-blocking).

        Args:
            query: Search query
            top_k: Number of chunks to retrieve

        Returns:
            List of Citation objects
        """
        return await asyncio.to_thread(self._sync.retrieve, query, top_k)

    async def refresh(self, sources: Union[str, List[str]]) -> "AsyncRagi":
        """
        Refresh specific sources (non-blocking).

        Args:
            sources: File paths, URLs, or glob patterns to refresh

        Returns:
            Self for chaining
        """
        await asyncio.to_thread(self._sync.refresh, sources)
        return self

    def filter(self, **kwargs: Any) -> "AsyncRagi":
        """
        Filter documents by metadata for the next query.

        Args:
            **kwargs: Metadata key-value pairs to filter by

        Returns:
            Self for chaining
        """
        self._sync.filter(**kwargs)
        return self

    async def count(self) -> int:
        """Return the number of chunks in the knowledge base."""
        return await asyncio.to_thread(self._sync.count)

    async def clear(self) -> None:
        """Clear all data from the knowledge base."""
        await asyncio.to_thread(self._sync.clear)

    @property
    def graph(self):
        """Access the knowledge graph for direct queries."""
        return self._sync.graph

    async def __call__(self, query: str, top_k: int = 5) -> Answer:
        """Callable shorthand for ask()."""
        return await self.ask(query, top_k=top_k)
