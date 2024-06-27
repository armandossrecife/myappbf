from flask import Blueprint, request, session, redirect
from flask import url_for, flash, render_template
import requests
from app import utilidades
from app import dto

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("auth.login"))

    try:
        # Retrieve user information from FastAPI app using token
        access_token = session["access_token"] 
        headers = {"Authorization": f"Bearer {access_token}"}
        usuario_logado = session['username']
        url_router = f"{utilidades.API_URL}/users/{usuario_logado}"
        response = requests.get(url_router, headers=headers)
    
        if response.status_code == 200:
            user_data = response.json()            
            url_route_profile = f"{utilidades.API_URL}/users/{usuario_logado}/profile"
            response_profile = requests.get(url_route_profile, headers=headers)

            if response_profile.status_code == 200:
                user_data_profile = response_profile.json()
                url_route_all_notes = f"{utilidades.API_URL}/users/{usuario_logado}/notes"
                session['profile_image_url'] = user_data_profile['profile_image_url']
                response_all_notes = requests.get(url_route_all_notes, headers=headers)
                
                if response_all_notes.status_code == 200:
                    notes_data = response_all_notes.json()
                    dadosDashboardDTO = dto.DadosDashboardDTO(lista_usuarios=[], lista_imagens=[], lista_analises=[], lista_notas=notes_data)

                return render_template("dashboard/starter.html", user=user_data, usuario = usuario_logado, 
                    profilePic=session['profile_image_url'], titulo="Dashboard",dadosDashboardDTO=dadosDashboardDTO)
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
    flash(error_message, category='danger')

    return render_template("auth/login.html", error_message=error_message)
