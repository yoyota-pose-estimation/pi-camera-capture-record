from flask import Flask, request
from cam import capture

app = Flask(__name__)


@app.route("/<section>")
def section(section):
    capture(section)
    return 'ok'


@app.route("/<section>/<label>")
def section_label(section, label):
    capture(section + '/' + label)
    return 'ok'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, threaded=True)
