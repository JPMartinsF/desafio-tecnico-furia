# README.md

# 🔥 Chatbot FURIA — Desafio Conversacional

Este repositório contém a entrega do **Challenge #1 - Experiência Conversacional**, desenvolvido para os fãs do time de CS:GO da **FURIA Esports**. Trata-se de um chatbot interativo, com interface web, que permite aos torcedores acompanhar novidades e interagir de forma prática e divertida.

## ✅ Funcionalidades Implementadas

- 💬 **Chat em tempo real** com respostas automáticas.
- 🎲 **Curiosidades aleatórias** sobre a história e estilo da FURIA.
- 🗓️ **Próximos jogos da FURIA**, com integração à HLTV.
- 👥 **Destaques dos jogadores da FURIA**, com estatísticas básicas (rating, KD, nickname).
- 📞 **Canal oficial de contato via WhatsApp**, com link direto para o beta fechado.

## 🚀 Como Executar Localmente

1. **Clone o repositório:**
```bash
git clone https://github.com/JPMartinsF/desafio-tecnico-furia.git
cd desafio-tecnico-furia
```

2. **Crie o ambiente virtual e instale as dependências:**
```bash
python -m venv venv
source venv/bin/activate
pip install -r chat_furia/requirements.txt
```

3. **Execute a aplicação:**
```bash
python chat_furia/app.py
```

4. Acesse via navegador:
```
http://localhost:5000
```

## 📹 Demonstração em Vídeo
Veja como o fã pode interagir com o bot:
[🔗 Link para o vídeo de demonstração no YouTube](https://youtu.be/9lTmcwobp4k)

## 🗂️ Estrutura do Projeto
```
desafio-tecnico-furia/
├── README.md                     # Documentação do projeto
├── chat_furia/                   # Módulo principal do chatbot
│   ├── requirements.txt          # Dependências do projeto
│   ├── app.py                    # Código principal do Flask
│   └── templates/                # Templates HTML do Flask
```

## 📌 Observações
- A aplicação utiliza a API pública da HLTV (não oficial) para obter dados dos jogos.
- A API pública da HLTV (não oficial) não é mais mantida portanto suas informações estão desatualizadas.

## 🛡️ Licença
Este projeto é apenas para fins demonstrativos no contexto do desafio proposto.

---