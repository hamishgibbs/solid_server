from rdflib import Graph, URIRef, Literal

from rdflib.namespace import FOAF, XSD

g = Graph()
g.parse('profile.rdf')

g.add((
    URIRef("http://example.com/person/nick"),
    FOAF.givenName,
    Literal("Nick", datatype=XSD.string)
))

g.add((
    URIRef("http://example.com/person/jack"),
    FOAF.givenName,
    Literal("Jack", datatype=XSD.string)
))

g.add((
    URIRef("http://example.com/person/herbert"),
    FOAF.givenName,
    Literal("Herbert", datatype=XSD.string)
))

print(len(g)) # prints 2

for s, p, o in g:
    print(s, p, o)

content = g.serialize(format="n3")


with open('test.rdf', 'wb') as f:

    f.write(content)

# to do - make a working profile document
# define permissions to read / write / append data
# access resources from other locations
