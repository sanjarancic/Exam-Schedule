from flask import Response
import json


def custom_response(message, status_code = 200):
    return Response(
        mimetype="application/json",
        response=json.dumps(message),
        status=status_code
    )


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


