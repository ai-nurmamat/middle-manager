"""
Core Data Structures for the Chronos-MCP Engine.

This module defines the foundational models for the Universal 4D Hypergraph.
Every piece of information is treated as a 4D Tuple: (Subject, Predicate, Object, Time).
"""

import uuid
import datetime
from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field


class SourceEvidence(BaseModel):
    """
    Evidence to trace back the origin of a data point, eliminating AI hallucinations.
    """

    source_id: str = Field(
        ..., description="Unique identifier of the source document/report."
    )
    text_snippet: str = Field(
        ..., description="The original text snippet from which the data was extracted."
    )
    timestamp: datetime.datetime = Field(
        ..., description="The publication or occurrence time of the source."
    )


class FourDTuple(BaseModel):
    """
    The Universal 4D Tuple: S-P-O-T
    (Subject, Predicate, Object, Time)

    This disruptive model breaks the boundaries between traditional property graphs
    and time-series databases by representing everything as a temporal edge.
    """

    id: str = Field(default_factory=lambda: f"tup_{uuid.uuid4().hex[:8]}")
    subject: str = Field(..., description="The subject entity, e.g., 'CATL', 'Apple'.")
    predicate: str = Field(
        ..., description="The relation or property, e.g., 'gross margin', 'invests_in'."
    )
    object: str = Field(
        ...,
        description="The object entity or value, e.g., '28.5', 'Solid State Battery'.",
    )
    time: datetime.datetime = Field(
        ..., description="The exact time when this fact is valid or occurred."
    )

    # Metadata
    unit: Optional[str] = Field(
        None, description="The unit if the object is a numeric value, e.g., '%', 'USD'."
    )
    evidence: Optional[SourceEvidence] = Field(
        None, description="Source evidence to guarantee traceability."
    )


class UniversalHypergraph:
    """
    Universal 4D Hypergraph Memory Engine.

    A pure in-memory O(1) indexing engine that natively supports Temporal Knowledge Graphs.
    It indexes tuples by Subject, Predicate, and Object to allow instant multidimensional queries.
    """

    def __init__(self) -> None:
        self.tuples: Dict[str, FourDTuple] = {}

        # O(1) Inverted Indexes
        self._s_index: Dict[str, List[str]] = {}
        self._p_index: Dict[str, List[str]] = {}
        self._o_index: Dict[str, List[str]] = {}

    def insert(self, tup: FourDTuple) -> str:
        """
        Insert a FourDTuple into the hypergraph and update indexes.

        Args:
            tup (FourDTuple): The tuple to insert.

        Returns:
            str: The unique ID of the inserted tuple.
        """
        self.tuples[tup.id] = tup

        if tup.subject not in self._s_index:
            self._s_index[tup.subject] = []
        self._s_index[tup.subject].append(tup.id)

        if tup.predicate not in self._p_index:
            self._p_index[tup.predicate] = []
        self._p_index[tup.predicate].append(tup.id)

        if tup.object not in self._o_index:
            self._o_index[tup.object] = []
        self._o_index[tup.object].append(tup.id)

        return tup.id

    def query(
        self,
        subject: Optional[str] = None,
        predicate: Optional[str] = None,
        object: Optional[str] = None,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
    ) -> List[FourDTuple]:
        """
        Query the Universal Hypergraph across any combination of dimensions.

        Args:
            subject (Optional[str]): Filter by subject entity.
            predicate (Optional[str]): Filter by predicate/relation.
            object (Optional[str]): Filter by object entity or value.
            start_time (Optional[datetime.datetime]): Filter tuples occurring on or after this time.
            end_time (Optional[datetime.datetime]): Filter tuples occurring on or before this time.

        Returns:
            List[FourDTuple]: A chronologically sorted list of matching tuples.
        """
        candidates: Optional[Set[str]] = None

        if subject:
            s_set = set(self._s_index.get(subject, []))
            candidates = s_set if candidates is None else candidates.intersection(s_set)
        if predicate:
            p_set = set(self._p_index.get(predicate, []))
            candidates = p_set if candidates is None else candidates.intersection(p_set)
        if object:
            o_set = set(self._o_index.get(object, []))
            candidates = o_set if candidates is None else candidates.intersection(o_set)

        if candidates is None:
            candidates = set(self.tuples.keys())

        results = []
        for cid in candidates:
            t = self.tuples[cid]
            if start_time and t.time < start_time:
                continue
            if end_time and t.time > end_time:
                continue
            results.append(t)

        # Always return chronologically sorted data
        results.sort(key=lambda x: x.time)
        return results
