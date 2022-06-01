from csvisual import create_application
from logging import getLogger

getLogger('werkzeug').disabled = True # disable flask logging

if __name__ == "__main__":
    app = create_application()
    app.run(debug = True, port = 8080)