import os

from dotenv import load_dotenv
from flask import Flask

from routes.auth import auth_bp
from routes.items import items_bp
from routes.pages import pages_bp

app = Flask(__name__)
app.register_blueprint(items_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(pages_bp)


load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


if __name__ == "__main__":
    app.run(debug=True)
