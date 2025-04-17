from flask import Flask, request, send_file
from flask_cors import CORS
from datetime import datetime, timedelta
from ics import Calendar, Event
import io

app = Flask(__name__)
CORS(app)

def gerar_eventos(data_ingresso, curso):
    eventos = []
    base = datetime.strptime(data_ingresso, "%Y-%m-%d")

    if curso == "mestrado":
        prazos = [
            ("Escolha do orientador", 3),
            ("Envio da proposta de dissertação", 9),
            ("Envio da proficiência", 12),
            ("Estágio docência", 18),
            ("Indicação de coorientador", 18),
            ("Defesa da dissertação", 24)
        ]
    else:  # doutorado
        prazos = [
            ("Escolha do orientador", 3),
            ("Qualificação", 24),
            ("Proficiência na segunda língua", 36),
            ("Defesa da tese", 48)
        ]

    for titulo, meses in prazos:
        data_evento = base + timedelta(days=30 * meses)
        evento = Event()
        evento.name = f"{titulo} ({curso})"
        evento.begin = data_evento.strftime("%Y-%m-%d")
        eventos.append(evento)

    return eventos

@app.route("/gerar-ics", methods=["POST"])
def gerar_ics():
    dados = request.get_json()
    data_ingresso = dados.get("data_ingresso")
    curso = dados.get("curso")

    calendario = Calendar()
    eventos = gerar_eventos(data_ingresso, curso)
    for evento in eventos:
        calendario.events.add(evento)

    buffer = io.StringIO(str(calendario))
    bytes_io = io.BytesIO(buffer.getvalue().encode("utf-8"))
    return send_file(bytes_io, mimetype="text/calendar", as_attachment=True, download_name="lembretes.ics")

if __name__ == "__main__":
    app.run()
