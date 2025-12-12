# query-collection

This should be an interface and implementation of a collection that holds SPARQL
1.1 queries.

## Usage

```python
from rdflib import Graph
from query_collection import TemplateQueryCollection

tqc = TemplateQueryCollection()
tqc.loadFromDirectory("path/to/dir/with/query/files")
example_query_template = tqc.get("example")

g = Graph()
g.query(**example_query_template.prepare())

```