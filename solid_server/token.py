import base64
import json


def decode_token_section(token: str,
                         index: int):

    token = base64.b64decode(token.split('.')[index] + '=' * 5)
    token = json.loads(token.decode('utf-8'))

    return token
