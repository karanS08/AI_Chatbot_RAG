from asgiref.wsgi import WsgiToAsgi

# Import the Flask WSGI app
from app import app as flask_app

# Wrap the WSGI app with an ASGI adapter
app = WsgiToAsgi(flask_app)
