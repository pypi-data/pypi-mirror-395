# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""
SessionManager module for managing Bokeh documents and
their associated data sources per session.
Ensures thread-safe, isolated data for each Bokeh session in Plotmon applications.
"""

from collections.abc import ItemsView
import copy
import logging

from bokeh.core.types import ID
from bokeh.document import Document
from bokeh.models import ColumnDataSource, FlexBox


class SessionManager:
    """Manages documents and their sources per session."""

    def __init__(self) -> None:
        """
        Initializes the SessionManager with empty dictionaries for documents,
        sources, base sources, and layouts.
        """
        self._docs: dict[int | ID, Document] = {}
        self._sources: dict[int | ID, dict[str, ColumnDataSource]] = {}
        self._base_sources = {}
        self._layouts = {}

    def get_doc_and_sources(
        self, doc: Document
    ) -> tuple[Document, dict[str, ColumnDataSource], None | FlexBox]:
        """Retrieve or create a unique set of data sources for the given document.
        This ensures that each document has its own copy of the data sources to prevent
        cross-document interference.

        Parameters
        ----------
        doc : Document
            The Bokeh document for which to retrieve or create data sources.

        Returns
        -------
            tuple[Document, dict[str, ColumnDataSource]]
                The document and its associated data sources.

        """
        session_id = self.get_current_session_id(doc)
        if session_id not in self._sources:
            self._sources[session_id] = {
                f"{name}": ColumnDataSource(data=copy.deepcopy(source.data))
                for name, source in self._base_sources.items()
            }
            self._docs[session_id] = doc
            self._layouts[session_id] = None  # Initialize layout for this session
        return (
            self._docs[session_id],
            self._sources[session_id],
            self._layouts[session_id],
        )

    def all_sessions(self) -> ItemsView[int | ID, Document]:
        """Get all managed sessions."""
        return self._docs.items()

    def get_sources(
        self, identifier: int | ID | None = None
    ) -> dict[str, ColumnDataSource]:
        """Get sources for a specific session identifier."""
        if identifier is None:
            logging.info("Identifier is None, cannot get sources.")
            return {}
        return self._sources.get(identifier, {})

    def delete_session(self, session_id: None | int | ID) -> None:
        """Delete the document and sources associated with the given session ID."""
        if session_id is None:
            logging.info("Session ID is None, cannot delete session.")
            return

        if session_id in self._docs:
            del self._docs[session_id]
        if session_id in self._sources:
            del self._sources[session_id]

    def add_base_source(self, name: str, source: ColumnDataSource) -> None:
        """Add a base source to be copied for new sessions."""
        self._base_sources[name] = source

    def update_sources(self, new_sources: dict[str, ColumnDataSource]) -> None:
        """
        Add new sources to base sources, then for each existing session,
        add a copy of the new sources.

        Parameters
        ----------
        new_sources : dict[str, ColumnDataSource]
            New sources to be added to the base sources and copied to existing sessions.

        """
        for name, source in new_sources.items():
            if name not in self._base_sources:
                self._base_sources[name] = source
                for _, sources in self._sources.items():
                    sources[name] = ColumnDataSource(data=copy.deepcopy(source.data))

    def set_layout(self, doc: Document, layout: FlexBox) -> None:
        """Set the layout for a specific document's session."""
        session_id = self.get_current_session_id(doc)
        self._layouts[session_id] = layout

    def get_layout(self, doc: Document) -> None | FlexBox:
        """Get the layout for a specific document's session."""
        session_id = self.get_current_session_id(doc)
        return self._layouts.get(session_id, None)

    def get_current_session_id(self, doc: Document) -> int | ID:
        """Get the session ID for the current document."""
        return doc.session_context.id if doc.session_context else id(doc)

    def get_all_session_ids(self) -> set[int | ID]:
        """Get all managed session IDs."""
        return set(self._docs.keys())

    def clear_docs(self) -> None:
        """
        Clear all managed documents.
        Keep existing sessions intact.
        Having no documents leads to regeneration of the entire page.
        """
        self._docs.clear()

    def clear(self) -> None:
        """
        Clear all managed documents and sources.
        Keep existing sessions intact.
        Having no layouts leads to regeneration of the entire page.
        """
        self._sources.clear()
        self._layouts.clear()
        self._base_sources.clear()

    def copy_base_sources_to_session(self, session_id: int | ID) -> None:
        """
        Copy base sources to a specific session.

        Parameters
        ----------
        session_id : int | ID
            The session ID to which the base sources will be copied.

        """
        if session_id not in self._sources:
            self._sources[session_id] = {}
        self._sources[session_id] = {
            ## if name already exists, skip updating it
            **{
                f"{name}": ColumnDataSource(data=copy.deepcopy(source.data))
                for name, source in self._base_sources.items()
            },
            **self._sources[session_id],
        }
