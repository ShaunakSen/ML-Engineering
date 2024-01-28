# Cypher Fundamentals

> https://graphacademy.neo4j.com/courses/cypher-fundamentals/1-reading/

---

## Domain model for this course

Here is the data model used in this course. The graph contains nodes with the labels Person and Movie. Person nodes have several types of relationships to Movie nodes. A Person node can have a FOLLOWS relationship to another Person node.

![](https://graphacademy.neo4j.com/courses/cypher-fundamentals/1-reading/images/movie-schema.svg)


## CYPHER Basics

![](https://pasteboard.co/D878ZViPgJCk.png)

```
MATCH
(p:Person{name: "Tom Hanks"}) -[:ACTED_IN]-> (m:Movie{title: "Cloud Atlas"})
RETURN p, m
```

OR 

```
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WHERE p.name = "Tom Hanks" AND m.title = "Cloud Atlas"
RETURN p, m;
```
```
╒════════════════════════════════════════╤══════════════════════════════════════════════════════════════════════╕
│p                                       │m                                                                     │
╞════════════════════════════════════════╪══════════════════════════════════════════════════════════════════════╡
│(:Person {born: 1956,name: "Tom Hanks"})│(:Movie {tagline: "Everything is connected",title: "Cloud Atlas",relea│
│                                        │sed: 2012})                                                           │
└────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────┘

```


### Cypher Pattern:

`() --> ()`: `()`: repesents nodes, `-->` represents relationships

`() --> (:Movie)`: all movie nodes that have a relationship with other nodes

`(:Person) -[:ACTED_IN]-> (:Movie)` : all movies which have a person who acted in that movie


How many people directed the movie Cloud Atlas?

```
MATCH (m:Movie) <-[:DIRECTED]- (p:Person)
WHERE m.title="Cloud Atlas"
RETURN m, p;
```

```
╒══════════════════════════════════════════════════════════════════════╤═════════════════════════════════════════════╕
│m                                                                     │p                                            │
╞══════════════════════════════════════════════════════════════════════╪═════════════════════════════════════════════╡
│(:Movie {tagline: "Everything is connected",title: "Cloud Atlas",relea│(:Person {born: 1965,name: "Tom Tykwer"})    │
│sed: 2012})                                                           │                                             │
├──────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────┤
│(:Movie {tagline: "Everything is connected",title: "Cloud Atlas",relea│(:Person {born: 1965,name: "Lana Wachowski"})│
│sed: 2012})                                                           │                                             │
├──────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────┤
│(:Movie {tagline: "Everything is connected",title: "Cloud Atlas",relea│(:Person {born: 1967,name: "Andy Wachowski"})│
│sed: 2012})                                                           │                                             │
└──────────────────────────────────────────────────────────────────────┴─────────────────────────────────────────────┘
```

Which movie has Emil Eifrem acted in?

```
MATCH (p:Person) -[:ACTED_IN]-> (m:Movie)
WHERE p.name = "Emil Eifrem"
RETURN p,m    
```

```
╒══════════════════════════════════════════╤══════════════════════════════════════════════════════════════════════╕
│p                                         │m                                                                     │
╞══════════════════════════════════════════╪══════════════════════════════════════════════════════════════════════╡
│(:Person {born: 1978,name: "Emil Eifrem"})│(:Movie {tagline: "Welcome to the Real World",title: "The Matrix",rele│
│                                          │ased: 1999})                                                          │
└──────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────┘
```

Some filtering keywords supported:

- IS NULL, IS NOT NULL
- STARTSWITH, ENDSWITH, CONTAINS
- tolower, toupper
- IN, NOT [...list...]



Find all people who wrote a movie but did not direct in same movie


- first define the 2 realtionships
- we need people who wrote a movie: `(p:Person) -[:WROTE]-> (m:Movie)`
- we need people who did not direct that movie: `(p) -[:DIRECTED]-> (m)`
- final query:

```
MATCH (p:Person) -[:WROTE]-> (m:Movie)
WHERE NOT EXISTS ( (p) -[:DIRECTED]-> (m) )
RETURN p, m
```

How many actors in the movie The Matrix were born after 1960?

```
MATCH (p:Person) -[:ACTED_IN]-> (m:Movie)
WHERE tolower(m.title) = "the matrix" AND p.born > 1960
RETURN p, m;
```
