from fluentes import QueryBuilder
import json

def main():
    qb = QueryBuilder(size=5, source=["title", "tags", "published"])
    q = (
        qb.match("title", "python programming", occurrence="must")
          .term("status", "published", occurrence="filter")
          .range("published", occurrence="must", gte="2020-01-01")
          .geo_distance("location", lat=52.52, lon=13.405, distance="50km", occurrence="filter")
          .aggregation("top_tags", "terms", field="tags", size=5)
          .highlight(["title"], pre_tags=["<em>"], post_tags=["</em>"])
          .build()
    )

    print(json.dumps(q, indent=2))

if __name__ == "__main__":
    main()
