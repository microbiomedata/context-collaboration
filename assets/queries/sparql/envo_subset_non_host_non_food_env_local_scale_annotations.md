The provided SPARQL query is designed to retrieve information about classes from an ontology, specifically focusing on
classes that are subclasses of certain top-level classes. The query filters out classes related to biomes, environmental
materials, food, and soil.

The results are intended to be considered as potential answers to the MIxS question [env_broad_scale](https://genomicsstandardsconsortium.github.io/mixs/0000012/)

Here's a breakdown of the main components of the query:

1. Prefix declarations: The query starts by declaring the necessary prefixes for the ontology namespaces (obo, oboInOwl,
   and rdfs) to simplify the URIs used in the query.

2. SELECT clause: The query selects various pieces of information about each class, including the class ID, alternative
   terms, comments, definitions, editor notes, synonyms (broad, exact, narrow, and related), subsets, labels, and
   superclasses.

3. WHERE clause: The main part of the query specifies the conditions for selecting the desired classes.
    - It uses the VALUES clause to define a set of top-level classes (specified by their URIs) that the desired classes
      should be subclasses of. These top-level classes include astronomical body parts, constructions, fiat objects,
      layers, manufactured products, and systems.
    - The MINUS clauses are used to exclude classes that are subclasses of specific classes related to biomes,
      environmental materials, food, and soil.

4. BIND and OPTIONAL clauses: The query uses BIND to extract the class ID from the full URI and assigns it to the ?class
   variable. OPTIONAL clauses are used to retrieve additional information about each class, such as superclasses,
   definitions, editor notes, alternative terms, synonyms, subsets, comments, and labels.

5. GROUP BY and ORDER BY clauses: The query groups the results by the ?class variable and orders the results
   alphabetically based on the class ID.

The query aims to retrieve comprehensive information about classes that are subclasses of the specified top-level
classes while excluding classes related to biomes, environmental materials, food, and soil. The retrieved information
includes various annotations and metadata associated with each class, such as alternative terms, comments, definitions,
synonyms, and labels. The results are grouped by class and ordered alphabetically for better organization and
readability.

All allowed classes are subclasses
of [BFO:000004, material entity](https://www.ebi.ac.uk/ols4/ontologies/envo/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FBFO_0000040?lang=en)

## Included first

* obo:ENVO_01000813 # astronomical body part, for example: beach sand, ecoregion, agricultural field, airport, village
* obo:ENVO_01001813 # construction, for example:beaver dam
* obo:BFO_0000024 # fiat object, for example:area of barren land
* obo:ENVO_01000281 # layer, for example:mineral horizon
* obo:ENVO_00003074 # manufactured product, for example:chair
* `<http://purl.obolibrary.org/obo/RO_0002577>` # system, for example:public transit system

## Explicitly does not include

* CHEBI:24431 # chemical entity
* CHEBI:36342 # subatomic particle
* NCBITaxon:1 # root
* OBI:0100026 # organism
* PCO:0000031 # organismal entity
* PO:0025131 # plant anatomical entity
* _and more_

## Then excluded from there

_To be included in separate queries_

* obo:ENVO_00000428 # biome
* obo:ENVO_00010483 # environmental material
* obo:FOODON_00002403 # food material
* obo:ENVO_00001998 # soil

