from flask import Flask, render_template, request, redirect, session, flash, url_for
import requests

app = Flask(__name__)
app.secret_key = "my_secret_key"  # Replace with a strong secret key for session management

# Define API base URL (replace with your actual FastAPI URL)
API_URL = "http://localhost:8000"  # Replace with your FastAPI app's URL and port

@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return render_template("auth/login.html")

@app.route("/login", methods=["GET", "POST"])
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
            error_message = "URL inválida"
        except requests.exceptions.ConnectionError:
            error_message = "Erro de conexão"
        except IOError: 
            error_message = "Erro de IO"
        flash(error_message)
        return render_template("auth/login.html", error_message=error_message)

    return render_template("auth/login.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    try:
        # Retrieve user information from FastAPI app using token
        headers = {"Authorization": f"Bearer {session['access_token']}"}
        response = requests.get(f"{API_URL}/users/{session['username']}", headers=headers)
    
        if response.status_code == 200:
            user_data = response.json()
            usuarios = []
            quantidade_usuarios = len(usuarios)
            imagens = []
            quantidade_imagens = len(imagens)
            usuario = session['username']
            return render_template("dashboard/starter.html", user=user_data, usuario = usuario, 
                profilePic="", titulo="Dashboard", usuarios = usuarios, 
                imagens = imagens, quantidade_usuarios=quantidade_usuarios, quantidade_imagens=quantidade_imagens)
        else:
            # Handle error retrieving user information
            error_message = f"Failed to retrieve user information - {response.status_code}"
            return render_template("error.html", message=error_message)
    except requests.exceptions.MissingSchema:
        error_message = "URL inválida"
    except requests.exceptions.ConnectionError:
        error_message = "Erro de conexão"
    except IOError: 
        error_message = "Erro de IO"    
    except Exception as ex:
        print(f"Erro: {str(ex)}")
        error_message = f"Erro: {str(ex)}"
    flash(error_message)
    return render_template("auth/login.html", error_message=error_message)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# Pagina de registro
@app.route("/register", methods=['GET', 'POST'])
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
        error = None

        if not username:
            error = "Username is required."
        elif not email: 
            error = "E-mail is required."
        elif not password:
            error = "Password is required."
        elif password != repassword: 
            error = "Password is not correct."

        if error is None:
            # Send user data to FastAPI app
            user_data = {"id": 0, "username": username, "email":email, "password": password}
            response = requests.post(f"{API_URL}/users", json=user_data)
            if response.status_code == 200:
                mensagem = f"Usuário {username} criado com sucesso!"
                flash(mensagem)
                return redirect(url_for("login"))
            else: 
                error = f"User {username} is already registered."
        
        flash(error)                
        return render_template("auth/register.html", error_message=error)
    return render_template("auth/register.html")

# Pagina de recuperacao de e-mail
@app.route("/forgot-password", methods=["GET"])
def forgot():
    return render_template("auth/forgot-password.html")


if __name__ == "__main__":
    app.run(debug=True)