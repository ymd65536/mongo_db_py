#!/bin/bash

echo "🛠️  User Data Management システムのセットアップを開始します..."

# Python 仮想環境の作成・アクティベート
if [ ! -d ".venv" ]; then
    echo "📦 Python仮想環境を作成中..."
    python3 -m venv .venv
fi

echo "🔧 依存関係をインストール中..."
.venv/bin/pip install --upgrade pip
.venv/bin/pip install fastapi uvicorn pymongo python-multipart

echo ""
echo "✅ セットアップが完了しました！"
echo ""
echo "🚀 使用方法:"
echo "   1. MongoDBを起動: ./start_mongodb.sh"
echo "   2. サンプルデータを作成: .venv/bin/python main.py"
echo "   3. APIサーバーを起動: ./start_api.sh"
echo "   4. ブラウザで http://localhost:8000 にアクセス"
echo ""
echo "📚 APIドキュメント: http://localhost:8000/docs"
echo ""