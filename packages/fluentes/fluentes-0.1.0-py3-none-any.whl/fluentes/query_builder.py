"""
Fluent Elasticsearch Query Builder

Usage:
    qb = QueryBuilder()
    q = (
        qb.match("title", "python", occurrence="must")
          .term("status", "active", occurrence="filter")
          .range("published", gte="2020-01-01", occurrence="must")
          .geo_distance("location", lat=52.52, lon=13.405, distance="50km", occurrence="filter")
          .aggregation("top_tags", "terms", field="tags", size=5)
          .build()
    )
"""

from copy import deepcopy
from typing import Any, Dict, List, Optional, Union


class QueryBuilder:
    def __init__(self, size: int = 10, source: Optional[List[str]] = None, min_score: Optional[float] = None):
        self._size = size
        self._source = list(source) if source else None
        self._min_score = min_score
        self._bool = {"must": [], "should": [], "filter": [], "must_not": []}
        self._aggs: Dict[str, Any] = {}
        self._highlight: Dict[str, Any] = {}
        # additional top-level options can be added here

    # --- helper to add clause ---
    def _add_clause(self, occurrence: str, clause: Dict[str, Any]):
        if occurrence not in self._bool:
            raise ValueError(f"Invalid occurrence: {occurrence}. Must be one of {list(self._bool.keys())}")
        self._bool[occurrence].append(clause)
        return self

    # --- query clauses (fluent) ---
    def match(self, field: str, query: Any, occurrence: str = "should", boost: Optional[float] = None, analyzer: Optional[str] = None):
        body = {"match": {field: {"query": query}}}
        if boost is not None:
            body["match"][field]["boost"] = boost
        if analyzer is not None:
            body["match"][field]["analyzer"] = analyzer
        return self._add_clause(occurrence, body)

    def match_phrase(self, field: str, query: Any, occurrence: str = "should", boost: Optional[float] = None, slop: Optional[int] = None):
        body = {"match_phrase": {field: {"query": query}}}
        if boost is not None:
            body["match_phrase"][field]["boost"] = boost
        if slop is not None:
            body["match_phrase"][field]["slop"] = slop
        return self._add_clause(occurrence, body)

    def term(self, field: str, value: Any, occurrence: str = "filter", boost: Optional[float] = None):
        body = {"term": {field: {"value": value}}}
        if boost is not None:
            body["term"][field]["boost"] = boost
        return self._add_clause(occurrence, body)

    def terms(self, field: str, values: List[Any], occurrence: str = "filter"):
        body = {"terms": {field: values}}
        return self._add_clause(occurrence, body)

    def range(self, field: str, occurrence: str = "must", **kwargs):
        # kwargs: gte, gt, lte, lt
        body = {"range": {field: {}}}
        for k, v in kwargs.items():
            if k not in ("gte", "gt", "lte", "lt"):
                raise ValueError("range supports only gte, gt, lte, lt")
            body["range"][field][k] = v
        return self._add_clause(occurrence, body)

    def wildcard(self, field: str, value: str, occurrence: str = "should", boost: Optional[float] = None):
        body = {"wildcard": {field: {"value": value}}}
        if boost is not None:
            body["wildcard"][field]["boost"] = boost
        return self._add_clause(occurrence, body)

    def exists(self, field: str, occurrence: str = "must"):
        body = {"exists": {"field": field}}
        return self._add_clause(occurrence, body)

    def query_string(self, query: str, default_field: Optional[str] = None, occurrence: str = "should"):
        body = {"query_string": {"query": query}}
        if default_field is not None:
            body["query_string"]["default_field"] = default_field
        return self._add_clause(occurrence, body)

    def geo_distance(self, field: str, lat: float, lon: float, distance: str, occurrence: str = "filter"):
        # distance should be like "50km" or "30mi"
        body = {"geo_distance": {"distance": distance, field: {"lat": lat, "lon": lon}}}
        return self._add_clause(occurrence, body)

    # --- aggregations ---
    def aggregation(self, name: str, agg_type: str, **kwargs):
        """
        Add an aggregation.
        Example: aggregation("top_tags", "terms", field="tags", size=10, order={"_count": "desc"})
        """
        agg_body = {agg_type: {}}
        # simple mapping for common options
        for k, v in kwargs.items():
            agg_body[agg_type][k] = v
        self._aggs[name] = agg_body
        return self

    # --- highlight configuration ---
    def highlight(self, fields: Optional[List[str]] = None, pre_tags: Optional[List[str]] = None, post_tags: Optional[List[str]] = None):
        h = {}
        if pre_tags is not None:
            h["pre_tags"] = pre_tags
        if post_tags is not None:
            h["post_tags"] = post_tags
        if fields:
            fields_map = {f: {} for f in fields}
            h["fields"] = fields_map
        self._highlight = h
        return self

    # --- setters ---
    def size(self, size: int):
        self._size = size
        return self

    def source(self, fields: List[str]):
        self._source = list(fields)
        return self

    def min_score(self, score: float):
        self._min_score = score
        return self

    # --- build final query dict ---
    def build(self) -> Dict[str, Any]:
        q: Dict[str, Any] = {}
        if self._source is not None:
            q["_source"] = deepcopy(self._source)
        q["size"] = self._size
        if self._min_score is not None:
            q["min_score"] = self._min_score

        # build bool - include only non-empty lists
        bool_body = {k: v for k, v in self._bool.items() if v}
        if bool_body:
            q["query"] = {"bool": deepcopy(bool_body)}
        else:
            q["query"] = {"match_all": {}}

        if self._aggs:
            q["aggs"] = deepcopy(self._aggs)

        if self._highlight:
            q["highlight"] = deepcopy(self._highlight)

        return q

    # convenience alias
    def to_dict(self):
        return self.build()
