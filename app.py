from flask import Flask, render_template, request, send_file
from datetime import datetime
import io

app = Flask(__name__)

def generate_ics(event_title, start_date, end_date, location, description):
    """
    Gera um arquivo .ics (iCalendar) como string com base nos dados do evento.
    """
    start_datetime = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    
    ics_string = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//YourCompany//NONSGML v1.0//EN
BEGIN:VEVENT
SUMMARY:{event_title}
DTSTART:{start_datetime.strftime('%Y%m%dT%H%M%S')}
DTEND:{end_datetime.strftime('%Y%m%dT%H%M%S')}
LOCATION:{location}
DESCRIPTION:{description}
STATUS:CONFIRMED
TRANSP:OPAQUE
END:VEVENT
"""
    return ics_string

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        course_type = request.form["course_type"]

        # Definir prazos de acordo com o tipo de curso
        if course_type == "mestrado":
            event_title = "Evento Mestrado"
            description = "Detalhes sobre o evento de Mestrado."
            deadlines = {
                "Escolha de Orientador": 3,
                "Envio da Proposta de Dissertação": 9,
                "Envio da Proficiência": 12,
                "Integralização de créditos para Estágio Docência": 18,
                "Indicação de Coorientador": 18,
                "Defesa da Dissertação": 24
            }
        elif course_type == "doutorado":
            event_title = "Evento Doutorado"
            description = "Detalhes sobre o evento de Doutorado."
            deadlines = {
                "Escolha de Orientador": 3,
                "Qualificação": 24,
                "Estágio Docência I": 24,
                "Proficiência em inglês": 24,
                "Proficiência em Segunda Língua": 36,
                "Estágio Docência II": 36,
                "Seminário de acompanhamento": 48,
                "Defesa da Tese": 48
            }
        else:
            event_title = "Evento Genérico"
            description = "Descrição do evento genérico."
            deadlines = {}

        # Localização fixa
        location = "Local do Evento"

        # Gerar o evento principal
        ics_content = generate_ics(event_title, start_date, end_date, location, description)

        # Incluir os prazos como eventos no .ics
        for deadline, months in deadlines.items():
            # Calcula a data do prazo a partir da data de início, somando o número de meses
            deadline_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
            deadline_date = deadline_date.replace(month=deadline_date.month + months)
            ics_content += generate_ics(deadline, deadline_date.strftime("%Y-%m-%d %H:%M:%S"), deadline_date.strftime("%Y-%m-%d %H:%M:%S"), location, "Prazo importante")

        # Criar um arquivo .ics a partir da string gerada
        ics_file = io.BytesIO()
        ics_file.write(ics_content.encode('utf-8'))
        ics_file.seek(0)

        # Enviar o arquivo .ics para download
        return send_file(ics_file, as_attachment=True, download_name="evento_com_prazos.ics", mimetype="text/calendar")
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
