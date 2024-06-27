from flask import Blueprint, request, session, redirect
from flask import url_for, flash, render_template
import requests
from app import utilidades

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Send login request to FastAPI app
        login_data = {"username": username, "password": password}
        url_router = f"{utilidades.API_URL}/login"
        try:
            response = requests.post(url_router, json=login_data)
            if response.status_code == 200:
                data = response.json()
                session["username"] = username
                session["access_token"] = data["access_token"]
                session['profile_image_url'] = None                
                return redirect(url_for("dashboard.dashboard"))
            elif response.status_code == 401: 
                error_message = "401 Unauthorized for invalid credentials"                             
            else:
                error_message = "Invalid username or password"
        except requests.exceptions.MissingSchema:
            error_message = f"URL {utilidades.API_URL}/login inválida"
        except requests.exceptions.ConnectionError:
            error_message = "Erro de conexão na tentativa do login"
        except IOError: 
            error_message = "Erro de IO durante o login"
        flash(error_message, category='danger')

        return render_template("auth/login.html")

    return render_template("auth/login.html")

# Pagina de registro
@auth_bp.route("/register", methods=['GET', 'POST'])
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
                url_router = f"{utilidades.API_URL}/users"
                response = requests.post(url_router, json=user_data)
                if response.status_code == 200:
                    mensagem = f"Usuário {username} criado com sucesso!"
                    flash(mensagem, category='success')
                    return redirect(url_for("auth.login"))
                else: 
                    error_message = f"User {username} is already registered."
                
            except requests.exceptions.MissingSchema:
                error_message = f"URL {utilidades.API_URL}/users inválida"
            except requests.exceptions.ConnectionError:
                error_message = "Erro de conexão na tentativa do login"
            except IOError: 
                error_message = "Erro de IO durante o login"
        
        flash(error_message, category='danger')                
        return render_template("auth/register.html", error_message=error_message)
    return render_template("auth/register.html")

# Pagina de recuperacao de e-mail
@auth_bp.route("/forgot-password", methods=["GET"])
def forgot():
    return render_template("auth/forgot-password.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))