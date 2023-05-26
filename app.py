from flask import Flask, request, Response, make_response
import base64

app = Flask(__name__)

def construct_response(msg: str, status_code: int, type_msg: str) -> Response:
    response = make_response(msg, status_code)
    response.headers['Content-Type'] = type_msg
    return response

@app.route("/")
def index():
    f = open('code3a.conf', 'r')
    conf = f.read()
    if 'Basic' in conf:
        try:
            if request.headers.get('Authorization') == None:
                return construct_response("No authenticated credentials", 401, "text/html")
            Authorization = request.headers.get('Authorization')
            basic_header, encoded_credentials = Authorization.split(' ')
            if basic_header != 'Basic':
                return construct_response('Invalid Authorization Headers', 401, 'text/html')
            try:
                credentials = base64.b64decode(encoded_credentials).decode('utf-8')
                username, password = credentials.split(':')
                if username != 'CNS' or password != 'CNS':
                    return construct_response('Invalid credentials', 401, 'text/html')
                return construct_response('Good to go!', 200, 'text/html')
            except:
                return construct_response('Invalid credentials', 401, 'text/html')
        except:
            return construct_response('Invalid request', 401, 'text/html')
    elif 'Cookie' in conf:
        pass
    elif 'JWT' in conf:
        pass
    else:
        return make_response("WTF", 401, "text/html")

