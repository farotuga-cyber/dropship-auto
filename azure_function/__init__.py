import json, os
from ..fulfill_order import handler  # reuse the existing logic

def main(req):
    # Azure Functions passes the request body in req.get_body().decode()
    try:
        body = req.get_body().decode()
    except Exception:
        return {
            "status": 400,
            "body": json.dumps({"error": "Invalid request"})
        }
    event = {"body": body}
    response = handler(event)
    return {
        "status": 200,
        "body": json.dumps({"result": "ok"})
    }
