from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# Ambil API Key dari environment variable supaya aman
openai.api_key = os.getenv("OPENAI_API_KEY")

# Simpan history chat di memory (sederhana)
chat_history = [{"role": "system", "content": "Kamu adalah chatbot ramah dan membantu."}]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"reply": "Tolong ketik sesuatu!"})

    # tambahkan pesan user ke history
    chat_history.append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
            max_tokens=150,
            temperature=0.7
        )
        bot_reply = response.choices[0].message.content.strip()
        # simpan jawaban bot ke history
        chat_history.append({"role": "assistant", "content": bot_reply})
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": f"Terjadi error: {e}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
