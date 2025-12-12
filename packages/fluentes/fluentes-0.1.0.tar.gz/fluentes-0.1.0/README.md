# FluentES -  Elasticsearch Fluent Query Builder

A small Python library for building Elasticsearch queries using a fluent API.

Example:
```python
from fluentes import QueryBuilder

q = (
    QueryBuilder()
    .match("title", "python")
    .term("status", "active")
    .build()
)

print(q)
```

## License [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

Released under the MIT License.  
You are free to use, modify, and distribute this software, as long as the original license is included with any copies.


