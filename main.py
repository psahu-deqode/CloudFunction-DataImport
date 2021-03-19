from flask import Flask
app = Flask(__name__)

from importfunction.DataImport import *
from queryfunction.Query import *


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
