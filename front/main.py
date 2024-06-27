from flask import Flask, render_template, request, redirect, session 
from flask import flash, url_for, send_from_directory, make_response
import requests
import os
from app import dto
from app.routes import auth
from app.routes import dashboard
from app.routes import notes
from app import utilidades

my_app = Flask(__name__)
my_app.secret_key = "my_secret_key"  # Replace with a strong secret key for session management

STATIC_PATH = os.path.join(my_app.root_path, 'static')

#Registra os Blueprints
my_app.register_blueprint(auth.auth_bp)
my_app.register_blueprint(dashboard.dashboard_bp)
my_app.register_blueprint(notes.notes_bp)

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

@my_app.route("/profile")
def profile():
    if "username" not in session:
        return redirect(url_for("auth.login"))

    try:
        # Recupera informacoes do backend usando o token
        access_token = session["access_token"] 
        headers = {"Authorization": f"Bearer {access_token}"}
        usuario_logado = session["username"]
        url_route = f"{utilidades.API_URL}/users/{usuario_logado}/profile"
        response = requests.get(url_route, headers=headers)

        if response.status_code == 200:
            user_data = response.json()            
            return render_template("dashboard/profile.html", user=user_data, usuario=usuario_logado, 
                profilePic=user_data["profile_image_url"], titulo="Profile", nome=usuario_logado, 
                id=str(user_data["id"]), email=user_data["email"], filename=user_data["profile_image_url"])
        else:
            # Handle error retrieving user information
            error_message = f"Failed to retrieve user information - {response.status_code}"
            return render_template("error.html", message=error_message)

    except requests.exceptions.MissingSchema:
        error_message = f"URL {url_route} inválida"
    except requests.exceptions.ConnectionError:
        error_message = "Erro de conexão"
    except IOError: 
        error_message = "Erro de IO"    
    except Exception as ex:
        error_message = f"Erro: {str(ex)}"
    flash(error_message, category='danger')

    return render_template("auth/login.html", error_message=error_message)

@my_app.route("/profile/imagem", methods=['GET', 'POST'])
def update_profile_image():    
    if "username" not in session:
        return redirect(url_for("auth.login"))

    try: 
        access_token = session["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        usuario_logado = session["username"]
        url_route = f"{utilidades.API_URL}/users/{usuario_logado}/profile"

        if request.method == "POST":
            username = request.form["username"]
            image_file = request.files["image"]
            files = {"image": (image_file.filename, image_file.read())}    
            response = requests.post(url_route, files=files, headers=headers)

            if response.status_code == 200:
                user_data = response.json()

                my_response = make_response(render_template("dashboard/profile.html", message=user_data["message"], 
                    usuario=usuario_logado, profilePic=user_data["profile_image_url"], titulo="Profile", nome=usuario_logado, 
                    id=user_data["id"], email=user_data["email"], filename=user_data["profile_image_url"]))
                my_response.headers["Authorization"] = f"Bearer {session['access_token']}"
                return my_response
            else:
                error_message = f"Error uploading image: {response.status_code}"
                return render_template("error.html", message=error_message)

        response = requests.get(url_route, headers=headers)
        if response.status_code == 200:
            user_data = response.json()

            my_return = make_response(render_template("users/imagem_profile.html", 
                usuario = usuario_logado, profilePic=user_data["profile_image_url"], 
                titulo="Update image profile", usuario_logado=usuario_logado, 
                nome=usuario_logado, filename=user_data["profile_image_url"]))
                
            my_return.headers["Authorization"] = f"Bearer {access_token}"
            return my_return

    except requests.exceptions.MissingSchema:
        error_message = f"URL {url_route} inválida"
    except requests.exceptions.ConnectionError:
        error_message = "Erro de conexão"
    except IOError: 
        error_message = "Erro de IO"    
    except Exception as ex:
        error_message = f"Erro: {str(ex)}"
    flash(error_message, category='danger')

    return render_template("auth/login.html", error_message=error_message)


if __name__ == "__main__":
    my_app.run(debug=True)