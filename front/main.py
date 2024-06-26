from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory, make_response
import requests
import os
from app import dto

my_app = Flask(__name__)
my_app.secret_key = "my_secret_key"  # Replace with a strong secret key for session management

STATIC_PATH = os.path.join(my_app.root_path, 'static')
# Define API base URL (replace with your actual FastAPI URL)
API_PORT = "8000"
API_URL = f"http://localhost:{API_PORT}"  # Replace with your FastAPI app's URL and port

@my_app.route('/favicon.ico')
def favicon():
    return send_from_directory(STATIC_PATH, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@my_app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return render_template("auth/login.html")

@my_app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Send login request to FastAPI app
        login_data = {"username": username, "password": password}
        try:
            response = requests.post(f"{API_URL}/login", json=login_data)
            if response.status_code == 200:
                data = response.json()
                session["username"] = username
                session["access_token"] = data["access_token"]
                return redirect(url_for("dashboard"))
            elif response.status_code == 401: 
                error_message = "401 Unauthorized for invalid credentials"                             
            else:
                error_message = "Invalid username or password"
        except requests.exceptions.MissingSchema:
            error_message = f"URL {API_URL}/login inválida"
        except requests.exceptions.ConnectionError:
            error_message = "Erro de conexão na tentativa do login"
        except IOError: 
            error_message = "Erro de IO durante o login"
        flash(error_message)

        return render_template("auth/login.html", error_message=error_message)

    return render_template("auth/login.html")

# Pagina de registro
@my_app.route("/register", methods=['GET', 'POST'])
def register():
    """
    Register a new user.
    Validates that the username is not already taken. Hashes the password for security.
    """
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        repassword = request.form["repassword"]
        
        error_message = None

        if not username:
            error_message = "Username is required."
        elif not email: 
            error_message = "E-mail is required."
        elif not password:
            error_message = "Password is required."
        elif password != repassword: 
            error_message = "Password is not correct."

        if error_message is None:
            try: 
                # Send user data to FastAPI app
                user_data = {"id": 0, "username": username, "email":email, "password": password}
                response = requests.post(f"{API_URL}/users", json=user_data)
                if response.status_code == 200:
                    mensagem = f"Usuário {username} criado com sucesso!"
                    flash(mensagem)
                    return redirect(url_for("login"))
                else: 
                    error_message = f"User {username} is already registered."
                
            except requests.exceptions.MissingSchema:
                error_message = f"URL {API_URL}/users inválida"
            except requests.exceptions.ConnectionError:
                error_message = "Erro de conexão na tentativa do login"
            except IOError: 
                error_message = "Erro de IO durante o login"
        
        flash(error_message)                
        return render_template("auth/register.html", error_message=error_message)
    return render_template("auth/register.html")

# Pagina de recuperacao de e-mail
@my_app.route("/forgot-password", methods=["GET"])
def forgot():
    return render_template("auth/forgot-password.html")

@my_app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@my_app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    try:
        # Retrieve user information from FastAPI app using token
        access_token = session["access_token"] 
        headers = {"Authorization": f"Bearer {access_token}"}
        usuario_logado = session['username']
        url_router = f"{API_URL}/users/{usuario_logado}"
        response = requests.get(url_router, headers=headers)
    
        if response.status_code == 200:
            dadosDashboardDTO = dto.DadosDashboardDTO(lista_usuarios=[], lista_imagens=[], lista_analises=[], lista_notas=[])
            user_data = response.json()            
            url_route_profile = f"{API_URL}/users/{usuario_logado}/profile"
            response_profile = requests.get(url_route_profile, headers=headers)

            if response_profile.status_code == 200:
                user_data_profile = response_profile.json()     

                return render_template("dashboard/starter.html", user=user_data, usuario = usuario_logado, 
                    profilePic=user_data_profile["profile_image_url"], titulo="Dashboard",dadosDashboardDTO=dadosDashboardDTO)
        else:
            # Handle error retrieving user information
            error_message = f"Failed to retrieve user information - {response.status_code}"
            return render_template("error.html", message=error_message)

    except requests.exceptions.MissingSchema:
        error_message = f"URL {url_router} inválida"
    except requests.exceptions.ConnectionError:
        error_message = "Erro de conexão"
    except IOError: 
        error_message = "Erro de IO"    
    except Exception as ex:
        error_message = f"Erro: {str(ex)}"
    flash(error_message)

    return render_template("auth/login.html", error_message=error_message)

@my_app.route("/profile")
def profile():
    if "username" not in session:
        return redirect(url_for("login"))

    try:
        # Recupera informacoes do backend usando o token
        access_token = session["access_token"] 
        headers = {"Authorization": f"Bearer {access_token}"}
        usuario_logado = session["username"]
        url_route = f"{API_URL}/users/{usuario_logado}/profile"
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
    flash(error_message)

    return render_template("auth/login.html", error_message=error_message)

@my_app.route("/profile/imagem", methods=['GET', 'POST'])
def update_profile_image():    
    if "username" not in session:
        return redirect(url_for("login"))

    try: 
        access_token = session["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        usuario_logado = session["username"]
        url_route = f"{API_URL}/users/{usuario_logado}/profile"

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
    flash(error_message)

    return render_template("auth/login.html", error_message=error_message)

@my_app.route("/notas", methods=['GET'])
def listar_notas():
    if "username" not in session:
        return redirect(url_for("login"))

    try:
        # Recupera informacoes do backend usando o token
        access_token = session["access_token"] 
        headers = {"Authorization": f"Bearer {access_token}"}
        usuario_logado = session["username"]
        url_route = f"{API_URL}/users/{usuario_logado}/profile"
        response = requests.get(url_route, headers=headers)

        if response.status_code == 200:
            user_data = response.json()            
            return render_template("notas/listar_notas.html", usuario = usuario_logado, titulo="Notas", profilePic=user_data["profile_image_url"])
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
    flash(error_message)

    return render_template("notas/listar_notas.html", error_message=error_message)

@my_app.route("/nota", methods=['GET', 'POST'])
def nova_nota():
    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == 'POST':
     print('Not implemented!')
     return 

    try:
        # Recupera informacoes do backend usando o token
        access_token = session["access_token"] 
        headers = {"Authorization": f"Bearer {access_token}"}
        usuario_logado = session["username"]
        url_route = f"{API_URL}/users/{usuario_logado}/profile"
        response = requests.get(url_route, headers=headers)

        if response.status_code == 200:
            user_data = response.json()            
            return render_template("notas/nova_nota.html", usuario = usuario_logado, titulo="Nova Nota", profilePic=user_data["profile_image_url"])
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
    flash(error_message)

    return render_template("notas/listar_notas.html", error_message=error_message)


if __name__ == "__main__":
    my_app.run(debug=True)