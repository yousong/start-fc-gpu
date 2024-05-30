import os
import subprocess
import sys
import traceback
from flask import Flask, request


app = Flask(__name__)


@app.route('/initialize', methods=['POST'])
def initialize():
    # See FC docs for all the HTTP headers: https://help.aliyun.com/document_detail/179368.html#section-fk2-z5x-am6
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Initialize Start RequestId: " + request_id)

    # do your things
    # Use the following code to get temporary credentials
    # access_key_id = request.headers['x-fc-access-key-id']
    # access_key_secret = request.headers['x-fc-access-key-secret']
    # access_security_token = request.headers['x-fc-security-token']

    print("FC Initialize End RequestId: " + request_id)
    return "Function is initialized, request_id: " + request_id + "\n"


@app.route('/invoke', methods=['POST'])
def invoke():
    # See FC docs for all the HTTP headers: https://help.aliyun.com/document_detail/179368.html#section-fk2-z5x-am6
    request_id = request.headers.get("x-fc-request-id", "")
    print("FC Invoke Start RequestId: " + request_id)

    # Use the following code to get temporary STS credentials to access Alibaba Cloud services
    # access_key_id = request.headers['x-fc-access-key-id']
    # access_key_secret = request.headers['x-fc-access-key-secret']
    # access_security_token = request.headers['x-fc-security-token']

    # Get function input from arguments
    sample = request.args.get("sample")

    try:
        # list available samples
        if not sample or sample == 'help':
            samples = os.listdir('./samples')
            return {
                'code': 0,
                'samples': samples,
            }, 200, [("Content-Type", "application/json")]

        args = [f"samples/{sample}"] + request.args.getlist('args')
        p = subprocess.run(args,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
        return {
            'code': p.returncode,
            'stdout': p.stdout.decode('utf8'),
            'stderr': p.stderr.decode('utf8'),
        }, 200, [("Content-Type", "application/json")]
    except Exception as e:
        exc_info = sys.exc_info()
        trace = traceback.format_tb(exc_info[2])
        errRet = {
            "code": 1,
            "message": str(e),
            "stack": trace
        }
        print(errRet)
        print("FC Invoke End RequestId: " + request_id)
        return errRet, 404, [("x-fc-status", "404")]

    print("FC Invoke End RequestId: " + request_id)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=9000)
