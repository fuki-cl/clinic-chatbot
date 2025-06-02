import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

# .env ファイルからAPIキーを読み込み
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAIクライアントの初期化
client = OpenAI(api_key=OPENAI_API_KEY)

# Flaskアプリの設定
app = Flask(__name__)
CORS(app)

# clinic_info.txt からFAQ読み込み
def load_clinic_info():
    try:
        with open("clinic_info.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "クリニックの情報が見つかりませんでした。"

clinic_info = load_clinic_info()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"error": "メッセージが空です。"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": 
f"あなたは医療事務スタッフとして、患者さんの質問に対して「{clinic_info}」の情報に基づいて、やさしく丁寧に答えてください。分からない場合は無理に答えず、診療時間内の受診を案内してください。"},
                {"role": "user", "content": user_message}
            ],
            temperature=0.5,
            max_tokens=500
        )
        bot_reply = response.choices[0].message.content.strip()
        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# エントリーポイント
if __name__ == "__main__":
    print("[INFO] Flaskサーバーを起動します...")
    app.run(host="0.0.0.0", port=5001, debug=False)

