from flask import Flask, render_template, redirect, session 
from flask import url_for, send_from_directory
import os
from app.routes import auth
from app.routes import dashboard
from app.routes import notes
from app.routes import profile

my_app = Flask(__name__)
my_app.secret_key = "my_secret_key"  # Replace with a strong secret key for session management

STATIC_PATH = os.path.join(my_app.root_path, 'static')

#Registra os Blueprints
my_app.register_blueprint(auth.auth_bp)
my_app.register_blueprint(dashboard.dashboard_bp)
my_app.register_blueprint(notes.notes_bp)
my_app.register_blueprint(profile.profile_bp)

def mapa_rotas():
    print("Mapa de rotas da aplicação: ")
    print(my_app.url_map)

@my_app.route('/favicon.ico')
def favicon():
    return send_from_directory(STATIC_PATH, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@my_app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("dashboard.dashboard"))
    return render_template("auth/login.html")


if __name__ == "__main__":
    my_app.run(debug=True)