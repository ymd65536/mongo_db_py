from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

def test_mongodb_connection():
    """MongoDB接続をテスト"""
    print("🔍 MongoDB接続テスト開始...")
    
    try:
        # クライアント作成
        client = MongoClient(
            "mongodb://localhost:27017/",
            serverSelectionTimeoutMS=3000
        )
        
        # 接続テスト
        client.admin.command('ping')
        
        print("✅ MongoDB接続成功！")
        
        # サーバー情報表示
        server_info = client.server_info()
        print(f"📊 MongoDBバージョン: {server_info.get('version')}")
        
        # データベース一覧
        db_list = client.list_database_names()
        print(f"📁 利用可能なデータベース: {db_list}")
        
        # テストデータベースへの書き込みテスト
        test_db = client['test_connection_db']
        test_collection = test_db['test_collection']
        
        test_doc = {'test': 'connection', 'timestamp': '2025-09-30'}
        result = test_collection.insert_one(test_doc)
        
        print(f"✅ テストデータ挿入成功: {result.inserted_id}")
        
        # テストデータを削除
        test_collection.delete_one({'_id': result.inserted_id})
        print("🧹 テストデータを削除しました")
        
        client.close()
        return True
        
    except ConnectionFailure:
        print("❌ MongoDB接続失敗: サーバーに接続できません")
        return False
    except ServerSelectionTimeoutError:
        print("❌ MongoDB接続タイムアウト: サーバーが応答しません")
        return False
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        return False

if __name__ == "__main__":
    success = test_mongodb_connection()
    
    if not success:
        print("\n💡 トラブルシューティング:")
        print("1. MongoDBサーバーを起動してください:")
        print("   brew services start mongodb-community")
        print("   または ./start_mongodb.sh")
        print("2. ポート27017が使用可能か確認:")
        print("   lsof -i :27017")
        print("3. MongoDB プロセスが実行中か確認:")
        print("   ps aux | grep mongod")