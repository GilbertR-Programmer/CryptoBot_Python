import sys
from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/', methods=['POST'])
def welcome():
    print("\n\n Recieved webhook notification")
    sys.stdout.flush()
    if request.method == 'POST':
        print(request.json['message'])
        return '',200
    else:
        abort(400)
if __name__ == '__main__':
    app.run(debug=True)