from flask import Response
import json


def custom_response(message, status_code):
  return Response(
    mimetype="application/json",
    response=json.dumps(message),
    status=status_code
  )
