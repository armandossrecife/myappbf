from flask import Blueprint, request, session, redirect
from flask import url_for, flash, render_template
import requests
from app import utilidades

notes_bp = Blueprint('notes', __name__)

@notes_bp.route("/notas", methods=['GET'])
def listar_notas():
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
            url_route_all_notes = f"{utilidades.API_URL}/users/{usuario_logado}/notes"
            response_all_notes = requests.get(url_route_all_notes, headers=headers)
            if response_all_notes.status_code == 200:
                notes_data = response_all_notes.json()
                return render_template("notas/listar_notas.html", usuario = usuario_logado, titulo="Notas", 
                profilePic=user_data["profile_image_url"], notas = notes_data)
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

    return render_template("notas/listar_notas.html", profilePic=session['profile_image_url'], error_message=error_message)

@notes_bp.route("/nota", methods=['GET', 'POST'])
def nova_nota():
    if "username" not in session:
        return redirect(url_for("auth.login"))

    # Recupera informacoes do backend usando o token
    access_token = session["access_token"] 
    headers = {"Authorization": f"Bearer {access_token}"}
    usuario_logado = session["username"]
    error_message = None

    if request.method == "POST":
        descricao = request.form["descricaonota"]
        if not descricao:
            error_message = "A descrição é um campo obrigatório!"

        if error_message is None:
            try: 
                # Send user data to FastAPI app
                descricao_data = {'id': 0, "description": descricao}
                response = requests.post(f"{utilidades.API_URL}/users/{usuario_logado}/notes", json=descricao_data, headers=headers)

                if response.status_code == 200:
                    mensagem = f"Nota criada com sucesso!"
                    flash(mensagem, category='success')
                    return redirect(url_for("notes.listar_notas"))
                else: 
                    error_message = f"Erro {response.status_code} ao cadastrar a nota!: {response.content}"
                
            except requests.exceptions.MissingSchema:
                error_message = f"URL {utilidades.API_URL}/notes inválida!"
            except requests.exceptions.ConnectionError:
                error_message = "Erro de conexão na tentativa de cadastro de nota."
            except IOError: 
                error_message = "Erro de IO durante o cadastro da nota."
        
        flash(error_message, category='danger')                
        return render_template("notas/nova_nota.html", titulo="Nova nota", usuario=usuario_logado, profilePic=session['profile_image_url'], error_message=error_message)

    return render_template("notas/nova_nota.html", titulo="Nova nota", usuario=usuario_logado, profilePic=session['profile_image_url'], error_message=error_message)


