import datetime
from flask import Flask, request, jsonify
import status_codes as StatusCodes

app = Flask(__name__)

@app.route('/time', methods=['GET'])
def get_time():
    current_time = datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")
    res = {
        'current_time': current_time,
    }
    return jsonify(res), StatusCodes.OK

if __name__ == '__main__':
    app.run(debug=True, port=5001)