from flask import Blueprint, request, session, redirect
from flask import url_for, flash, render_template, make_response
import requests
from app import utilidades

profile_bp = Blueprint('profile', __name__)

@profile_bp.route("/profile")
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

@profile_bp.route("/profile/imagem", methods=['GET', 'POST'])
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