from datetime import datetime

import requests
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

app = Flask(__name__)
curiosity_index = 0

CURIOSIDADES = [
    "💡 Sabia que a FURIA foi o primeiro time BR a jogar de forma agressiva e estratégica no CS internacional?",
    "🔥 A FURIA foi fundada em 2017 e rapidamente se tornou uma das principais organizações de eSports do Brasil.",
    "🎯 O estilo tático da FURIA chamou atenção mundial por sua ousadia, especialmente em mapas como Mirage e Vertigo.",
    "🎮 A FURIA também tem times em outros jogos como Valorant, League of Legends, Rocket League, Apex Legends, e PUBG Mobile.",
]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    global curiosity_index
    data = request.json
    user_input = data.get("message", "").lower()

    if any(p in user_input for p in ["jogo", "agenda", "partida"]):
        reply = get_next_furia_match()
    elif any(p in user_input for p in ["destaque", "jogador", "jogadores"]):
        reply = get_furia_players()
    elif "curiosidade" in user_input:
        reply = CURIOSIDADES[curiosity_index]
        curiosity_index = (curiosity_index + 1) % len(CURIOSIDADES)
    elif "contato" in user_input:
        reply = '📞 Para falar com a FURIA, acesse: <a href="https://wa.me/5511993404466" target="_blank">WhatsApp Oficial</a>'
    else:
        reply = "⚡️ Olá! Tente perguntar sobre jogos, jogadores, curiosidades ou contato para falar conosco!"

    return jsonify({"reply": reply})


def get_next_furia_match():
    try:
        response = requests.get("https://hltv-api.vercel.app/api/matches.json")
        if response.status_code == 200:
            matches = response.json()
            for match in matches:
                teams = [team["name"] for team in match.get("teams", [])]
                if "FURIA" in teams or "FURIA Academy" in teams:
                    event = match.get("event", {}).get("name", "Evento desconhecido")
                    dt = datetime.strptime(match["time"], "%Y-%m-%dT%H:%M:%S.%fZ")
                    date_str = dt.strftime("%d/%m/%Y %H:%M")
                    opponent = [team for team in teams if "FURIA" not in team]
                    opponent_str = opponent[0] if opponent else "Adversário indefinido"
                    return f"\U0001f4c5 Próximo jogo: {event} — contra {opponent_str} em {date_str}"
            return "❌ Não encontrei partidas futuras da FURIA no momento."
        return "⚠️ Erro ao buscar informações, tente novamente mais tarde."
    except Exception as e:
        return f"⚠️ Erro inesperado: {str(e)}"


def get_furia_players():
    try:
        response = requests.get("https://hltv-api.vercel.app/api/match.json")
        if response.status_code == 200:
            players = response.json()
            jogadores = []
            for player in players:
                if "FURIA" in player["team"] or "FURIA Academy" in player["team"]:
                    nickname = player.get("nickname", "FURIA")
                    kd = player.get("kd", "N/A")
                    rating = player.get("rating", "N/A")
                    jogadores.append(f"Nickname: {nickname}\nKD: {kd}\nRating: {rating}")
            if jogadores:
                return "👥 Jogadores em destaque da FURIA:\n\n" + "\n\n".join(jogadores)
            return "Nenhum jogador encontrado."
        return "⚠️ Erro ao buscar informações, tente novamente mais tarde."
    except Exception as e:
        return f"⚠️ Erro inesperado: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)
