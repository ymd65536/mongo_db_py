# JSON to MongoDB アップローダー

このプロジェクトは、JSONファイルをMongoDBに格納するためのPythonスクリプトです。

## 📋 必要な要件

- Python 3.7+
- MongoDB サーバー
- pymongo パッケージ

## 🚀 セットアップ

### 1. Pythonパッケージのインストール
```bash
pip install pymongo
```

### 2. MongoDBサーバーの起動

#### Homebrewを使用している場合：
```bash
# MongoDBをインストール（初回のみ）
brew tap mongodb/brew
brew install mongodb-community

# MongoDBサーバーを起動
brew services start mongodb-community

# または提供されているスクリプトを使用
./start_mongodb.sh
```

#### Dockerを使用する場合：
```bash
# MongoDBコンテナを起動
docker run --name mongodb-local -d -p 27017:27017 mongo:latest
```

## 📁 ファイル構成

```
ld_json/
├── main.py                 # メインスクリプト（JSONファイル作成 + MongoDB投入）
├── mongodb_uploader.py     # MongoDB専用アップローダークラス
├── start_mongodb.sh        # MongoDB起動スクリプト
├── user_data_files/        # JSONファイル格納ディレクトリ
│   ├── user_1.json
│   ├── user_2.json
│   ├── user_3.json
│   └── user_4.json
└── README.md
```

## 🔧 使用方法

### 基本的な使用方法

1. **JSONファイル作成とMongoDB投入の一括実行：**
```bash
python main.py
```

2. **既存のJSONファイルのみをMongoDBに投入：**
```bash
python mongodb_uploader.py
```

### カスタム設定での使用

```python
from mongodb_uploader import MongoDBUploader

# カスタム接続設定
uploader = MongoDBUploader(
    connection_string="mongodb://localhost:27017/",
    database_name="my_custom_db"
)

if uploader.connect():
    # 特定のディレクトリとコレクション名を指定
    uploader.upload_json_files(
        data_dir="custom_data_dir",
        collection_name="custom_collection"
    )
    
    # データの確認
    uploader.show_collection_data("custom_collection")
    
uploader.disconnect()
```

## 🗄️ MongoDB設定

### デフォルト設定
- **接続先:** `mongodb://localhost:27017/`
- **データベース名:** `user_data_db`
- **コレクション名:** `users`

### データ構造
各JSONファイルは以下の追加情報と共にMongoDBに保存されます：

```json
{
  "id": 1,
  "product": "Laptop",
  "price": 1200.0,
  "source_file": "user_1.json",  // 追加：ソースファイル名
  "uploaded_at": null,           // 追加：アップロード日時（カスタマイズ可能）
  "_id": ObjectId("...")         // MongoDB自動生成ID
}
```

## 🛠️ トラブルシューティング

### MongoDB接続エラー
- MongoDBサーバーが起動していることを確認
- 接続文字列が正しいことを確認
- ファイアウォール設定を確認

### JSONファイルエラー
- JSONファイルの形式が正しいことを確認
- ファイルのエンコーディングがUTF-8であることを確認

### パーミッションエラー
- スクリプトに実行権限があることを確認
- ファイルディレクトリへの読み書き権限を確認

## 📊 機能

- ✅ 複数のJSONファイルの一括アップロード
- ✅ エラーハンドリングとログ出力
- ✅ アップロード結果の詳細レポート
- ✅ MongoDB接続状態の確認
- ✅ アップロードされたデータの表示
- ✅ カスタム設定対応
- ✅ 自動的なソースファイル名記録

## 🔄 MongoDB操作

### データベースとコレクションの確認
```bash
# MongoDBシェルに接続
mongosh

# データベース一覧
show dbs

# user_data_dbに切り替え
use user_data_db

# コレクション一覧
show collections

# usersコレクションのデータ表示
db.users.find().pretty()

# データ件数確認
db.users.countDocuments()
```

### データの削除
```bash
# 全データ削除
db.users.deleteMany({})

# 特定の条件でデータ削除
db.users.deleteMany({"source_file": "user_1.json"})
```