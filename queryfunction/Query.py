from flask import abort
from flask import make_response
import os
import json
from google.cloud import datastore
from main import app

PROJECT_ID = os.getenv('PROJECT_ID')
SERVICE_ACCOUNT_JSON = os.getenv('SERVICE_ACCOUNT_JSON')
BUCKET_NAME = os.getenv('BUCKET_NAME')


@app.route('/query/', methods=['POST'])
def query_entity(request):
    req = request.get_json(silent=True, force=True)
    res = makeResponse(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeResponse(req):
    if req is None or req.get('key') is None:
        abort(400, 'Please provide a valid key to search ')
    key = req.get("key")
    entities = datastore.Client(PROJECT_ID).query(kind="data")
    entities.add_filter("UnitName", "=", key)
    entities_list = list(entities.fetch())
    if not entities_list:
        return "No result is returned"
    else:
        for i in entities_list:
            return i
