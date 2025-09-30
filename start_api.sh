#!/bin/bash

# User Data Management API Server
# MongoDB + FastAPI + フロントエンド

echo "🚀 User Data Management API Server を起動します..."

# Python仮想環境のアクティベート確認
if [ ! -d ".venv" ]; then
    echo "❌ 仮想環境が見つかりません。先にsetup.shを実行してください。"
    exit 1
fi

# MongoDBの起動確認
echo "📡 MongoDB接続を確認中..."
if ! python test_mongodb_connection.py > /dev/null 2>&1; then
    echo "⚠️  MongoDB接続に失敗しました。MongoDBを起動してください:"
    echo "   brew services start mongodb-community"
    echo "   または ./start_mongodb.sh を実行"
    echo ""
    echo "🔄 MongoDBなしでもAPIサーバーは起動しますが、一部機能が制限されます。"
    read -p "続行しますか？ (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "🌐 API サーバーを起動中..."
echo "   URL: http://localhost:8000"
echo "   API ドキュメント: http://localhost:8000/docs"
echo "   管理画面: http://localhost:8000"
echo ""
echo "⏹️  停止するには Ctrl+C を押してください"
echo ""

# FastAPI アプリケーションを起動
.venv/bin/python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload