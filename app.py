# app.py
import requests
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# Estado para alternar curiosidades
curiosity_index = 0

CURIOSIDADES = [
    "💡 Sabia que a FURIA foi o primeiro time BR a jogar de forma agressiva e estratégica no CS internacional?",
    "🔥 A FURIA foi fundada em 2017 e rapidamente se tornou uma das principais organizações de eSports do Brasil.",
    "🎯 O estilo tático da FURIA chamou atenção mundial por sua ousadia, especialmente em mapas como Mirage e Vertigo.",
    "🎮 A FURIA não atua apenas em CS:GO! Ela também possui times em League of Legends, Valorant, PUBG, Apex Legends e Rocket League.",
    "🏆 A FURIA já conquistou diversos campeonatos, incluindo o ESL Pro League Season 12 e o DreamHack Masters Spring 2021."
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang=\"pt-BR\">
<head>
  <meta charset=\"UTF-8\">
  <title>Chat FURIA</title>
  <style>
    body { font-family: sans-serif; background: #000; color: white; display: flex; flex-direction: column; align-items: center; }
    #chatbox { width: 100%; max-width: 500px; margin-top: 2rem; background: #111; padding: 1rem; border-radius: 8px; }
    .msg { margin: 0.5rem 0; padding: 0.5rem; border-radius: 6px; }
    .user { background: #6b21a8; text-align: right; }
    .bot { background: #1f2937; text-align: left; }
    input, button { padding: 0.5rem; font-size: 1rem; margin-top: 1rem; }
    img.logo { max-width: 150px; margin-top: 1rem; }
  </style>
</head>
<body>
  <h1>🔥 Chat com a FURIA</h1>
  <img class=\"logo\" src=\"https://upload.wikimedia.org/wikipedia/pt/9/99/Furia_Esports_logo.png\" alt=\"Logo FURIA\">
  <div id=\"chatbox\"></div>
  <input id=\"userInput\" type=\"text\" placeholder=\"Pergunte algo...\">
  <button onclick=\"sendMessage()\">Enviar</button>
  <script>
    function sendMessage() {
      const input = document.getElementById('userInput');
      const text = input.value.trim();
      if (!text) return;
      appendMessage('user', text);
      input.value = '';
      fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      })
      .then(res => res.json())
      .then(data => appendMessage('bot', data.reply));
    }
    function appendMessage(sender, text) {
      const div = document.createElement('div');
      div.className = `msg ${sender}`;
      div.textContent = text;
      document.getElementById('chatbox').appendChild(div);
    }
  </script>
</body>
</html>
"""

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
                    return f"\U0001F4C5 Próximo jogo: {event} — contra {opponent_str} em {date_str}"
            return "❌ Não encontrei partidas futuras da FURIA no momento."
        else:
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
            else:
                return "Nenhum jogador encontrado."
        else:
            return "⚠️ Erro ao buscar informações, tente novamente mais tarde."
    except Exception as e:
        return f"⚠️ Erro inesperado: {str(e)}"

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    global curiosity_index
    data = request.json
    user_input = data.get('message', '').lower()

    if any(p in user_input for p in ['jogo', 'agenda', 'partida']):
        reply = get_next_furia_match()
    elif any(p in user_input for p in ['destaque', 'jogador', 'jogadores']):
        reply = get_furia_players()
    elif 'curiosidade' in user_input:
        reply = CURIOSIDADES[curiosity_index]
        curiosity_index = (curiosity_index + 1) % len(CURIOSIDADES)
    else:
        reply = '⚡️ Ainda estou aprendendo! Tente perguntar sobre jogos, jogadores ou curiosidades.'

    return jsonify({ 'reply': reply })

if __name__ == '__main__':
    app.run(debug=True)
