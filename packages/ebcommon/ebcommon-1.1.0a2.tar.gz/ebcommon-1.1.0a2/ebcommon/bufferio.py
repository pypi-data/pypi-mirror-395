import os
import requests

from ebcommon.models_common import Message, MessageLogin, MessageData
from ebcommon.models_buffer import Buffer

def write_buffer_from_path(url: str, access_token: MessageLogin, uuid: str, path: str) -> Buffer:
    length = os.path.getsize(path)
    with open(path, "rb") as filed:
        data = filed.read()
        headers = access_token.getAuthHeader() | {
            'Content-Type': 'application/octet-stream',
            'Content-Length': '%d' % length
        }
        response = requests.put(f"{url}/eph_buffer/{uuid}/data", headers=headers, data=data)
        ebuffer = Message.castResponse(response, Buffer)
        return ebuffer


def dump_buffer_to_path(url: str, access_token: MessageLogin, uuid: str, path: str, params: dict = {}):
    response = requests.get(f"{url}/eph_buffer/{uuid}/data", headers=access_token.getAuthHeader(), params=params)
    content = MessageData.castResponse(response)
    with open(path, "wb") as f:
        f.write(content)
    return MessageData(content)
