"""
FluentES - Elasticsearch Fluent Query Builder
----------------------------------

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

# expose the builder at package level
from .query_builder import QueryBuilder

__all__ = ["QueryBuilder"]
