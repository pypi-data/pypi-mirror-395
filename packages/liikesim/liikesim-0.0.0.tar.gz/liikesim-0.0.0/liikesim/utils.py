import json


def formatMessage(clientRequestFunction: str, clientRequestParameter: dict):
    data = {
        "clientRequestFunction": clientRequestFunction,
        "clientRequestParameter": clientRequestParameter
    }
    message = json.dumps(data) + "\n"
    return message