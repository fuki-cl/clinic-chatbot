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

# クリニック情報を読み込む関数
def load_clinic_info():
    try:
        with open("clinic_info.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "クリニック情報が読み込めませんでした。"

clinic_info_text = load_clinic_info()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    messages = [
        {"role": "system", "content": 
"あなたは『みどりのふきたクリニック』の受付AIです。診断は行わず、適切な受診案内を行ってください。"},
        {"role": "user", "content": f"{clinic_info_text}\n\n質問: 
{user_message}"}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = "エラーが発生しました。もう一度お試しください。"

    return jsonify({"reply": reply})

# アプリ起動設定
if __name__ == "__main__":
    print("[INFO] Flaskサーバーを起動します...")
    app.run(host="0.0.0.0", port=5001, debug=False)

