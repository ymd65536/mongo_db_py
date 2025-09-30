#!/bin/bash

# MongoDB起動用スクリプト
# 使用方法: ./start_mongodb.sh

echo "🗄️ MongoDBサーバーを起動しています..."

# Homebrewでインストールしたかチェック
if command -v brew &> /dev/null; then
    if brew list mongodb-community &> /dev/null; then
        echo "📦 Homebrew経由でMongoDBを起動中..."
        brew services start mongodb-community
        echo "✅ MongoDBサーバーが起動しました"
        echo "🌐 接続先: mongodb://localhost:27017"
        echo "🛑 停止するには: brew services stop mongodb-community"
        exit 0
    fi
fi

# Dockerでの起動オプション
if command -v docker &> /dev/null; then
    echo "🐳 Dockerを使用してMongoDBを起動しますか？ (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "🐳 DockerでMongoDBコンテナを起動中..."
        docker run --name mongodb-local -d -p 27017:27017 mongo:latest
        echo "✅ MongoDBコンテナが起動しました"
        echo "🌐 接続先: mongodb://localhost:27017"
        echo "🛑 停止するには: docker stop mongodb-local"
        echo "🗑️  削除するには: docker rm mongodb-local"
        exit 0
    fi
fi

echo "❌ MongoDBの起動方法が見つかりません"
echo ""
echo "📋 MongoDBをインストールする方法:"
echo "1. Homebrewの場合:"
echo "   brew tap mongodb/brew"
echo "   brew install mongodb-community"
echo ""
echo "2. Dockerの場合:"
echo "   docker pull mongo:latest"
echo ""
echo "3. 公式サイトからダウンロード:"
echo "   https://www.mongodb.com/try/download/community"