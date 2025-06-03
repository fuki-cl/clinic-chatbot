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

# クリニック情報の読み込み
def load_clin_

