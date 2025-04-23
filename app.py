from flask import Flask
from flask import jsonify
from flask import render_template_string
from flask import request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
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
  <img class="logo" src="https://upload.wikimedia.org/wikipedia/pt/f/f9/Furia_Esports_logo.png" alt="Logo FURIA">
  <div id="chatbox"></div>
  <input id="userInput" type="text" placeholder="Pergunte algo...">
  <button onclick="sendMessage()">Enviar</button>
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


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").lower()

    reply = user_input
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
