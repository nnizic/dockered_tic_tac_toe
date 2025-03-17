"""frontend za dockerirani križić kružić"""

import requests

from flask import Flask, Response, render_template


app = Flask(__name__)

SERVIS_1_URL = "http://servis_igra:8001/start"


@app.route("/")
def index():
    return render_template("index.html")


def stream_data():
    """strimanje podataka iz servis1, prosljeđivanje frontendu"""
    with requests.post(SERVIS_1_URL, stream=True) as r:
        for line in r.iter_lines():
            if line:
                yield f"data: {line.decode()}\n\n"


@app.route("/stream")
def stream():
    return Response(stream_data(), content_type="text/event-stream")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8004, debug=True)
