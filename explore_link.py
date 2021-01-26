from rdflib import Graph, Literal, RDF, URIRef, BNode

from rdflib.namespace import FOAF, RDF

from rdflib import Namespace

# example personal page (PRIVATE)
SOLID = Namespace('.')

g = Graph()
g.bind("solid", SOLID)

id = URIRef("#id")

g.add((id, SOLID.oidcRegistration, Literal('''{
    "client_id" : "https://app.example/webid#id",
    "redirect_uris" : ["https://app.example/callback"],
    "client_name" : "Solid Application Name",
    "client_uri" : "https://app.example/",
    "logo_uri" : "https://app.example/logo.png",
    "tos_uri" : "https://app.example/tos.html",
    "scope" : "openid profile offline_access",
    "grant_types" : ["refresh_token","authorization_code"],
    "response_types" : ["code"],
    "default_max_age" : 60000,
    "require_auth_time" : true
    }''')))



g.serialize('data/johndoe/profile.ttl', format="turtle")

with open('data/johndoe/profile.ttl', 'w') as f:

    f.write(profile)


g = Graph()
g.parse(source='/Users/hamishgibbs/Documents/Personal/solid_server/data/johndoe/profile.ttl', format='turtle').serialize(format='turtle')



for a, b, c in g:

    print((a, b, c))

# next: how to save Graph
# integrate API with personal profile (check password)
# grant certain access with tokens
# write app to access resources with token after user OKs it (writes it to trusted app section of personal profile)

# how to save graph


"""
Private profile contents

username
password hash

trusted applications
    |_ https://urlofdogsocialnetwork.co.uk

        |_ semantic type foaf:Person ( & foaf:Friend)
        |_ permission [read, write, append]

        |_ semantic type foaf:Dog ( & foaf:Pet)
        |_ permission [read, write, append]

    |_ https://urlofrecipesite.com

        |_ semantic type any:Recipe
        |_ permission [read, write, append]


Try to remove any use of SQL DB and store password hash in private .rdf profile

"""
