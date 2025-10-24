## View the graph in your platform of choice

To make the Knowledge Graph more accessible to users working with their graph
data platform of choice, we exported the nodes and relationships to CSV format.
The CSV files are available in the [./cdl_db](./cdl_db) directory of this repository.

### Property graph schema

The data was initially created using the [Kuzu](https://kuzudb.com/) graph database, so
a property graph schema is used. The schema is as follows:

```
(:Talk) -[:IS_DESCRIBED_BY]-> (:Tag)
(:Speaker) -[:GIVES_TALK]-> (:Talk)
(:Talk) -[:IS_PART_OF]-> (:Event)
(:Talk) -[:IS_CATEGORIZED_AS]-> (:Category)

Node properties:
  - Tag
    - keyword: string
  - Talk
    - title: string
    - category: string
    - url: string
    - description: string
    - type: string
  - Speaker
    - name: string
  - Event
    - name: string
    - description: string
  - Category
    - name: string

Edge properties:
- GIVES_TALK
    - date: date
```

### Node files

The following node files are available:

- `Category.csv`: Categories of talks
- `Event.csv`: Event name and information
- `Speaker.csv`: Names and metadata of speakers
- `Tag.csv`: Tags (keywords) associated with the talk content
- `Talk.csv`: Talks and their metadata

### Relationship files

The following relationship files are available (the first column is the source node's property
value, and the second column is the target node's property value):

- `GIVES_TALK.csv`: Relationships between speakers and talks
- `IS_CATEGORIZED_AS.csv`: Relationships between talks and categories
- `IS_DESCRIBED_BY.csv`: Relationships between talks and tags
- `IS_PART_OF.csv`: Relationships between talks and events

Using the relationship directions from the schema as shown above, you can import these CSV files into your graph database of choice.
