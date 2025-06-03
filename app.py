import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAIクライアントの初期化
client = OpenAI(api_key=OPENAI_API_KEY)

# Flaskアプリの作成
app = Flask(__name__)
CORS(app)

# クリニック情報を読み込む関数
def load_clinic_info():
    try:
        with open("clinic_info.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "クリニック情報が見つかりませんでした。"

clinic_info_text = load_clinic_info()

# チャット用のエンドポイント
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()
    if not user_message:
        return jsonify({"reply": "メッセージが空です。"})

    try:
        # OpenAI API へ問い合わせ
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": 
"あなたはクリニックの受付担当AIです。必要に応じて受診を勧めてください。"},
                {"role": "user", "content": f"{clinic_info_text}\n\n質問: 
{user_message}"}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"エラーが発生しました: {str(e)}"})

# アプリ起動設定
if __name__ == "__main__":
    print("[INFO] Flaskサーバーを起動します...")
    app.run(host="0.0.0.0", port=5001, debug=False)
