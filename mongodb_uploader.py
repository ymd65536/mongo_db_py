import os
import json
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from datetime import datetime

class MongoDBUploader:
    def __init__(self, connection_string="mongodb://localhost:27017/", database_name="user_data_db"):
        self.connection_string = connection_string
        self.database_name = database_name
        self.client = None
        self.database = None
        
    def connect(self):
        """MongoDBに接続"""
        try:
            print(f"📡 MongoDB接続中... ({self.connection_string})")
            
            # クライアント作成（タイムアウト設定を追加）
            self.client = MongoClient(
                self.connection_string,
                serverSelectionTimeoutMS=5000,  # 5秒でタイムアウト
                connectTimeoutMS=10000,         # 10秒で接続タイムアウト
                socketTimeoutMS=10000           # 10秒でソケットタイムアウト
            )
            
            # 接続テスト
            self.client.admin.command('ping')
            
            # データベース取得
            self.database = self.client[self.database_name]
            
            print(f"✅ MongoDB接続成功！")
            print(f"📊 データベース: {self.database_name}")
            return True
            
        except ConnectionFailure as e:
            print(f"❌ MongoDB接続失敗: {e}")
            return False
        except ServerSelectionTimeoutError as e:
            print(f"❌ MongoDB接続タイムアウト: {e}")
            print("💡 MongoDBサーバーが起動していることを確認してください")
            return False
        except Exception as e:
            print(f"❌ 予期しないエラー: {e}")
            return False
    
    def disconnect(self):
        """MongoDB接続を切断"""
        if self.client:
            self.client.close()
            print("🔌 MongoDB接続を切断しました")
    
    def upload_json_files(self, data_dir="user_data_files", collection_name="users"):
        """JSONファイルをMongoDBにアップロード"""
        if self.database is None:
            print("❌ データベース接続が確立されていません。先にconnect()を実行してください。")
            return False
            
        if not os.path.exists(data_dir):
            print(f"❌ ディレクトリが見つかりません: {data_dir}")
            return False
        
        collection = self.database[collection_name]
        success_count = 0
        error_count = 0
        
        print(f"📁 ディレクトリをスキャン中: {data_dir}")
        
        json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
        
        if not json_files:
            print(f"⚠️  JSONファイルが見つかりません: {data_dir}")
            return False
        
        print(f"📄 {len(json_files)}個のJSONファイルを発見")
        
        for filename in json_files:
            file_path = os.path.join(data_dir, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                
                # メタデータを追加
                if isinstance(data, dict):
                    data['source_file'] = filename
                    data['uploaded_at'] = datetime.now()
                    collection.insert_one(data)
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            item['source_file'] = filename
                            item['uploaded_at'] = datetime.now()
                    collection.insert_many(data)
                else:
                    # プリミティブ型の場合はオブジェクトでラップ
                    wrapped_data = {
                        'data': data,
                        'source_file': filename,
                        'uploaded_at': datetime.now()
                    }
                    collection.insert_one(wrapped_data)
                
                print(f"✅ アップロード成功: {filename}")
                success_count += 1
                
            except json.JSONDecodeError as e:
                print(f"❌ JSONエラー in {filename}: {e}")
                error_count += 1
            except Exception as e:
                print(f"❌ アップロードエラー in {filename}: {e}")
                error_count += 1
        
        print(f"\n📊 アップロード結果:")
        print(f"   ✅ 成功: {success_count}件")
        print(f"   ❌ 失敗: {error_count}件")
        
        return success_count > 0
    
    def show_collection_data(self, collection_name="users", limit=10):
        """コレクションのデータを表示"""
        if self.database is None:
            print("❌ データベース接続が確立されていません")
            return
        
        collection = self.database[collection_name]
        
        try:
            count = collection.count_documents({})
            print(f"\n📊 コレクション '{collection_name}' の情報:")
            print(f"   📄 総データ数: {count}件")
            
            if count > 0:
                print(f"   📝 最新{min(limit, count)}件のデータ:")
                for i, doc in enumerate(collection.find().limit(limit), 1):
                    print(f"   [{i}] {doc}")
            else:
                print("   ℹ️  データが存在しません")
                
        except Exception as e:
            print(f"❌ データ取得エラー: {e}")

def main():
    """メイン実行関数"""
    print("🚀 MongoDB Uploader を開始...")
    
    uploader = MongoDBUploader()
    
    # 接続確認
    if not uploader.connect():
        print("❌ MongoDB接続に失敗しました。以下を確認してください:")
        print("   1. MongoDBサーバーが起動しているか")
        print("   2. 接続文字列が正しいか")
        print("   3. ファイアウォール設定")
        print("\n💡 MongoDB起動方法:")
        print("   brew services start mongodb-community")
        print("   または ./start_mongodb.sh")
        return
    
    try:
        # JSONファイルをアップロード
        if uploader.upload_json_files():
            print("\n🎉 アップロード完了！")
            
            # アップロードしたデータを表示
            uploader.show_collection_data()
        else:
            print("❌ アップロードに失敗しました")
    
    finally:
        uploader.disconnect()

if __name__ == "__main__":
    main()