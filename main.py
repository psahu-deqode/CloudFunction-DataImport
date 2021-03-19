from flask import Flask,abort
from flask import make_response
import os
import json
from google.cloud import storage, datastore

PROJECT_ID = os.getenv('PROJECT_ID')
SERVICE_ACCOUNT_JSON = os.getenv('SERVICE_ACCOUNT_JSON')
BUCKET_NAME = os.getenv('BUCKET_NAME')
app = Flask(__name__)


@app.route('/main/', methods=['POST'])
def main(request):
    req = request.get_json(silent=True, force=True)
    res = makeResponse(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeResponse(req):
    # create storage client
    storage_client = storage.Client()
    # get bucket with name
    bucket = storage_client.get_bucket(BUCKET_NAME)
    # validate if a filename is provided or not
    if not req.get("filename"):
        abort(400, 'Please provide a filename')
    json_file = req.get("filename")
    # Validate the existance of the file in the bucket
    if not bucket.get_blob(json_file):
        abort(400, 'Please provide a valid filename')
    # get bucket data as blob
    blob = bucket.get_blob(json_file)
    data = json.loads(blob.download_as_string())
    for i in data['ContentsList']:
        # append details to each json in ContentsList
        i['DocumentNo'] = data['DocumentNo']
        i['LanguageCode'] = data['LanguageCode']
        i['Version'] = data['Version']
        # Converted comma separated unit names to Array so it will be easier to search
        i['UnitName'] = i['UnitName'].split(', ') if len(i['UnitName']) != 0 else i['UnitName']
        # create datastore entity
        imported_json = datastore.Entity(key=datastore.Client(PROJECT_ID).key("data"))
        # update datastore entity with the imported json
        imported_json.update(i)
        datastore.Client(PROJECT_ID).put(imported_json)
    return "Json uploaded successfully to Datastore"


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
