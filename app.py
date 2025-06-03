import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAIクライアント初期化
client = OpenAI(api_key=OPENAI_API_KEY)

# Flask アプリケーション
app = Flask(__name__)
CORS(app)

# クリニック情報をテキストファイルから読み込む関数
def load_clinic_info():
    try:
        with open("clinic_info.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "クリニック情報が読み込めませんでした。"

# チャットエンドポイント
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    clinic_info_text = load_clinic_info()

    messages = [
        {
            "role": "system",
            "content": 
"あなたは医療事務に詳しいクリニックの受付スタッフです。患者の質問に親切・丁寧に答えてください。"
        },
        {
            "role": "user",
            "content": f"{clinic_info_text}\n\n質問: {user_message}"
        }
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.5
        )
        answer = response.choices[0].message.content
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ポート指定してアプリ起動（Renderで必要）
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print("[INFO] Flaskサーバーを起動します...")
    app.run(host="0.0.0.0", port=port)

