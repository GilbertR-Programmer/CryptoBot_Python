from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def respond():
    print(request.json)
    return Response(status=200)

@app.route('/running')
def running():
  return 'Yes The System is running'

if __name__ == '__main__':
  app.run()