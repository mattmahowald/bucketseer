import logging
from flask import Flask, request

app = Flask(__name__)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

@app.route("/bucketseer/bucket-webhook")
def bucket_webhook():
    app.logger.debug(request.data)
    return 'helloworld'

@app.route('/healthz', methods=['GET'])
def run_health_check():
    """GET /healthz exposes a readiness check that Kubernetes can use to determine
    if bucketseer is ready to accept traffic.
    """

    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
