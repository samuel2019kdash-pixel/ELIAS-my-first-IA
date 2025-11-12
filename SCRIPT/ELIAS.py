from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
import markdown

load_dotenv()  # só para desenvolvimento local

app = Flask(__name__)

# Cliente OpenAI (usa a variável de ambiente OPENAI_API_KEY em produção)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/elias')
def elias():
    return render_template('elias.html')

@app.route('/elias_api', methods=['POST'])
def elias_api():
    data = request.get_json()
    user_message = data.get('message', '')
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é o assistente ELIAS, amigável e didático."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content
        # converte Markdown -> HTML para o front renderizar
        formatted = markdown.markdown(reply)
        return jsonify({"response": formatted})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"response": "⚠️ Ocorreu um erro ao conectar com a IA."})

if __name__ == '__main__':
    # pega a porta do ambiente (Render define PORT)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
