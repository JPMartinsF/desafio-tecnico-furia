# app.py
import requests
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

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
                    return f"📅 Próximo jogo: {event} — contra {opponent_str} em {date_str}"
            return "❌ Não encontrei partidas futuras da FURIA no momento."
        else:
            return "⚠️ Erro ao buscar informações, tente novamente mais tarde."
    except Exception as e:
        return f"⚠️ Erro inesperado: {str(e)}"

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '').lower()

    if any(palavra in user_input for palavra in ['jogo', 'agenda', 'partida']):
        reply = get_next_furia_match()
    elif 'destaque' in user_input or 'jogador' in user_input:
        reply = '🐍 KSCERATO tem sido o destaque nas últimas partidas!'
    elif 'curiosidade' in user_input:
        reply = '💡 Sabia que a FURIA foi o primeiro time BR a jogar de forma agressiva e estratégica no CS internacional?'
    elif 'quiz' in user_input:
        reply = '🎮 Em breve teremos um quiz interativo para testar seu nível de fã!'
    else:
        reply = '⚡️ Ainda estou aprendendo! Tente perguntar sobre jogos, jogadores ou curiosidades.'

    return jsonify({ 'reply': reply })

if __name__ == '__main__':
    app.run(debug=True)
