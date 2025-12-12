import unittest
from fluentes import QueryBuilder

class QueryBuilderTests(unittest.TestCase):
    def test_basic_match_and_term(self):
        qb = QueryBuilder()
        q = qb.match("name", "Alice", occurrence="must").term("active", True, occurrence="filter").build()
        self.assertIn("query", q)
        self.assertEqual(q["size"], 10)
        bool_part = q["query"]["bool"]
        self.assertTrue(any("match" in c for c in bool_part["must"]))
        self.assertTrue(any("term" in c for c in bool_part["filter"]))

    def test_range_and_agg(self):
        qb = QueryBuilder(size=2)
        qb.range("age", occurrence="must", gte=18, lt=30).aggregation("age_stats", "avg", field="age")
        q = qb.build()
        self.assertIn("aggs", q)
        self.assertIn("age_stats", q["aggs"])

if __name__ == "__main__":
    unittest.main()
