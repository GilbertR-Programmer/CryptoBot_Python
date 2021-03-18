from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def respond():
    print(request.json)
    return Response(status=200)

@app.route('/running')
def running():
  return 'Yes The System is running'

app.run(host='0.0.0.0', port=80)
