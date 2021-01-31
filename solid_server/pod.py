import re
from datetime import datetime
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, XSD
from rdflib.plugins.sparql import prepareQuery


def new_container(uri: str,
                  root: bool = False,
                  format: str = 'ttl'):

    g = Graph()

    PIM = Namespace('http://www.w3.org/ns/pim/space#')
    TERMS = Namespace('http://purl.org/dc/terms/')
    LDP = Namespace('http://www.w3.org/ns/ldp#')
    ST = Namespace('http://www.w3.org/ns/posix/stat#')

    uri = Literal(uri)

    g.add((uri, RDF.type, LDP.BasicContainer))
    g.add((uri, RDF.type, LDP.Container))

    if root:

        g.add((uri, RDF.type, PIM.Storage))

    g.add((uri, TERMS.modified,
           Literal(datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
                   datatype=XSD.dateTime)))

    g.add((uri, ST.mtime,
           Literal(datetime.timestamp(datetime.now()))))

    g.add((uri, ST.size, Literal(0)))

    return g.serialize(format=format)


def new_acl(uri: str,
            agent: str,
            scopes: list = ['read', 'write', 'control'],
            authorization: str = '#authorization1',
            default: bool = True,
            format: str = 'ttl'):

    ACL = Namespace('http://www.w3.org/ns/auth/acl#')

    auth = Literal(authorization)

    agent = Literal(agent)

    uri = Literal(uri)

    g = Graph()

    g.add((auth, RDF.type, ACL.Authorization))
    g.add((auth, ACL.agent, agent))
    g.add((auth, ACL.accessTo, uri))

    if 'read' in scopes:
        g.add((auth, ACL.mode, ACL.Read))

    if 'write' in scopes:
        g.add((auth, ACL.mode, ACL.Write))

    if 'control' in scopes:
        g.add((auth, ACL.mode, ACL.Control))

    if default:

        g.add((auth, ACL.default, uri))

    return g.serialize(format=format)


def append_acl(acl: str,
               uri: str,
               agent: str,
               scopes: list = ['read', 'write', 'control'],
               default: bool = True,
               format: str = 'ttl'):

    g = Graph()

    g.parse(data=acl, format=format)

    q = prepareQuery(
        '''
        SELECT ?s
        WHERE {
            ?s ?p ?o .
            filter (contains(str(?s), "#authorization"))
        }
        '''
    )

    authorizations = []

    for row in g.query(q):

        item = row[0].value

        search = re.compile(r'\d').search(item)

        authorizations.append(int(search[0]))

    next_auth = max(authorizations) + 1

    append_acl = new_acl(uri=uri,
                         agent=agent,
                         scopes=scopes,
                         authorization='#authorization' + str(next_auth),
                         default=default,
                         format=format)

    g2 = Graph()

    g2.parse(data=append_acl, format=format)

    g = g + g2

    return g.serialize(format=format)
