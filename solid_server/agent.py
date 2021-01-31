from fastapi import HTTPException, status
from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery


def get_webid_idp(webid: str):

    try:

        g = Graph()

        g.parse(webid, format='turtle')

        q = prepareQuery(
            '''
            SELECT ?o
            WHERE {
                ?s <http://www.w3.org/ns/solid/terms#oidcIssuer> ?o
            }
            '''
        )

        oidc_registration = []

        for row in g.query(q):
            oidc_registration.append(row)

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unable to confirm Identity Provider.",
        )

    return oidc_registration[0][0].value
