from fastapi import FastAPI, Request, HTTPException, status, Form, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from solid_server import token
from solid_server import agent
from authlib.jose import jwt, JsonWebKey
from solid_server import pod
import requests
from rdflib import Graph

from pymongo import MongoClient

client = MongoClient('mongodb://0.0.0.0:27017')

db = client['server']

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root(request: Request):

    return templates.TemplateResponse("home.html", {"request": request})


# new_container function to create a basic container
# new_acl function to write a new acl auxilliary resource

@app.get("/register")
async def get_register(request: Request):

    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
async def post_register(request: Request,
                        webid: str = Form(default=None),
                        pod_name: str = Form(default=None)):

    # Actual authentication flow with the IdP would happen here

    data = db.data

    acl = db.acl

    if webid is None:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No webid provided.",
        )

    if pod_name is None:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No pod name provided.",
        )

    # check that pod is not already registered

    pod_uri = 'http://127.0.0.1:8002/data/' + pod_name + '/'

    if pod_uri in data.distinct('path'):

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Pod name already exists.",
        )

    pod_doc = pod.new_container(uri=pod_uri,
                                root=True)

    acl_doc = pod.new_acl(uri=pod_uri,
                          agent=webid,
                          scopes=['read', 'write', 'control'])

    pod_doc = {
        "path": pod_uri,
        "content": pod_doc
    }

    acl_doc = {
        "path": pod_uri + '.acl',
        "content": acl_doc
    }

    data.insert_one(pod_doc)
    acl.insert_one(acl_doc)

    # redirect to new pod view

    return RedirectResponse(pod_uri, status_code=303)


@app.get("/data/{pod_name}/{rest_of_path:path}")
async def get_data(request: Request,
                   pod_name: str,
                   rest_of_path: str):

    data = db.data
    acl = db.acl

    request_path = 'http://127.0.0.1:8002/data/' + pod_name + '/' + rest_of_path

    print(request_path)

    if '.acl' in rest_of_path:

        resource = acl.find_one({'path': request_path})

    else:

        resource = data.find_one({'path': request_path})

    if not resource:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No data found.",
        )

    return Response(content=resource['content'].decode('utf-8'),
                    media_type="text/turtle")


@app.get("/protected/data.ttl")
async def get_protected(request: Request):

    try:

        access_token = request.headers['authorization']
        dpop = request.headers['dpop']

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No access credentials provided.",
        )

    access_token = access_token.replace('DPoP ', '')

    # Checks Access Token expirations
    access_token_payload = token.decode_token_section(access_token, 1)

    try:

        assert access_token_payload['exp'] >= int(datetime.timestamp(datetime.now()))

    except AssertionError:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Expired Access Token.",
        )

    dpop_token_payload = token.decode_token_section(dpop, 1)

    # Checks the DPoP token url and method

    try:

        assert 'http://127.0.0.1:8002/protected/data.ttl' == dpop_token_payload['htu']

    except AssertionError:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect request path.",
        )

    try:

        assert 'GET' == dpop_token_payload['htm']

    except AssertionError:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect request method.",
        )

    # Checks DPoP signature against Access Token

    dpop_public_key = dpop_token_payload['cnf']['jwk']

    try:

        claims = jwt.decode(dpop, dpop_public_key)

        claims.validate()

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid DPoP Signature.",
        )

    dpop_public_key = JsonWebKey.import_key(dpop_public_key, {'kty': 'EC'})
    dpop_public_key_thumbprint = dpop_public_key.thumbprint()

    try:

        assert dpop_public_key_thumbprint == access_token_payload['cnf']['jwk']

    except AssertionError:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token thumbprints do not match.",
        )

    webid_res = requests.get(access_token_payload['webid'])

    try:

        assert webid_res.status_code == 200

    except AssertionError:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unable to access WebID document.",
        )

    #  Checks issuer

    webid_iss = agent.get_webid_idp(access_token_payload['webid'])

    try:

        assert webid_iss == access_token_payload['iss']

    except AssertionError:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot confiem OIDC issuer.",
        )

    idp_config = requests.get(webid_iss + '/.well-known/openid_configuration')

    idp_config = idp_config.json()

    idp_public_keys = requests.get(idp_config['jwks_uri'])

    idp_public_keys = idp_public_keys.json()

    access_signature_verified = False

    for public_key in idp_public_keys:

        try:

            claims = jwt.decode(access_token, public_key)

            claims.validate()

            access_signature_verified = True

        except Exception:

            pass

    if not access_signature_verified:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unable to verify access token signature",
        )

    # this is where access control comes into play
    # Must check that webid in the token has been
    # granted access to the requested resource

    return {"message": "This is some protected data. Nice."}
