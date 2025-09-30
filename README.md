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

## 🔍 mongoshでのデータ取得方法

### 基本的なクエリ

#### 1. MongoDB Shellに接続
```bash
# ローカルMongoDBに接続
mongosh

# プロジェクトのデータベースに直接接続
mongosh mongodb://localhost:27017/user_data_db
```

#### 2. 基本的なデータ表示
```javascript
// プロジェクトデータベースに切り替え
use user_data_db

// 全データを表示
db.users.find()

// 見やすく整形して表示
db.users.find().pretty()

// 最初の1件のみ表示
db.users.findOne()

// 総件数を確認
db.users.countDocuments()
```

### 条件検索

#### 3. 基本的な検索クエリ
```javascript
// 特定のIDで検索
db.users.findOne({id: 1})

// 特定の商品を検索
db.users.find({product: "Laptop"}).pretty()

// ソースファイル別にデータを表示
db.users.find({source_file: "user_1.json"}).pretty()

// 価格範囲での検索
db.users.find({price: {$gte: 500, $lte: 2000}}).pretty()

// 複数の条件で検索
db.users.find({product: "Laptop", price: {$gt: 1000}}).pretty()
```

#### 4. 高度な検索
```javascript
// 正規表現を使用した検索
db.users.find({product: /^Lap/}).pretty()

// OR条件での検索
db.users.find({
  $or: [
    {price: {$lt: 600}},
    {product: "Smartphone"}
  ]
}).pretty()

// 存在チェック
db.users.find({uploaded_at: {$exists: true}}).pretty()

// 日付範囲での検索
db.users.find({
  uploaded_at: {
    $gte: new Date("2025-09-30"),
    $lt: new Date("2025-10-01")
  }
}).pretty()
```

### ソートと制限

#### 5. データの並び替えと制限
```javascript
// 価格の昇順でソート
db.users.find().sort({price: 1}).pretty()

// 価格の降順でソート
db.users.find().sort({price: -1}).pretty()

// 最新5件を表示
db.users.find().limit(5).pretty()

// 特定のフィールドのみ表示
db.users.find({}, {product: 1, price: 1, _id: 0}).pretty()

// ページング（2件スキップして3件表示）
db.users.find().skip(2).limit(3).pretty()
```

### 統計と集計

#### 6. 統計情報の取得
```javascript
// ユニークな商品名を取得
db.users.distinct("product")

// ソースファイル別の件数
db.users.aggregate([
  {$group: {
    _id: "$source_file",
    count: {$sum: 1}
  }}
])

// 価格統計（平均、最大、最小）
db.users.aggregate([
  {$group: {
    _id: null,
    avgPrice: {$avg: "$price"},
    maxPrice: {$max: "$price"},
    minPrice: {$min: "$price"},
    totalCount: {$sum: 1}
  }}
])

// 商品別の価格統計
db.users.aggregate([
  {$group: {
    _id: "$product",
    avgPrice: {$avg: "$price"},
    count: {$sum: 1}
  }},
  {$sort: {avgPrice: -1}}
])
```

### 便利な関数

#### 7. カスタム関数の定義（mongosh内で実行）
```javascript
// 統計情報を表示する関数
function showStats() {
    print("📈 統計情報:");
    const total = db.users.countDocuments();
    print(`総件数: ${total}`);
    
    const bySource = db.users.aggregate([
        {$group: {_id: "$source_file", count: {$sum: 1}}}
    ]).toArray();
    
    print("ソースファイル別:");
    bySource.forEach(item => print(`  ${item._id}: ${item.count}件`));
    
    const priceStats = db.users.aggregate([
        {$group: {
            _id: null,
            avg: {$avg: "$price"},
            max: {$max: "$price"},
            min: {$min: "$price"}
        }}
    ]).toArray()[0];
    
    if (priceStats) {
        print(`価格統計:`);
        print(`  平均: ￥${priceStats.avg?.toFixed(2) || 'N/A'}`);
        print(`  最高: ￥${priceStats.max || 'N/A'}`);
        print(`  最低: ￥${priceStats.min || 'N/A'}`);
    }
}

// 価格範囲で検索する関数
function findByPrice(min, max) {
    print(`💰 価格範囲 ￥${min} - ￥${max} の商品:`);
    db.users.find({
        price: {$gte: min, $lte: max}
    }).forEach(doc => {
        print(`${doc.product}: ￥${doc.price} (${doc.source_file})`);
    });
}

// 使用例
showStats()
findByPrice(500, 1500)
```

### データエクスポート

#### 8. コマンドラインからのエクスポート
```bash
# JSON形式でエクスポート
mongoexport --db=user_data_db --collection=users --out=export.json --pretty

# CSV形式でエクスポート
mongoexport --db=user_data_db --collection=users --type=csv --fields=id,product,price,source_file --out=export.csv

# 特定の条件でエクスポート
mongoexport --db=user_data_db --collection=users --query='{"price":{"$gt":1000}}' --out=expensive_items.json --pretty
```

### クイック接続スクリプト

#### 9. 便利な接続スクリプト
プロジェクト用の接続スクリプト `connect_mongodb.sh` を作成：

```bash
#!/bin/bash
echo "🔌 MongoDBに接続中..."
echo "📊 プロジェクト用データベース: user_data_db"
echo "📁 メインコレクション: users"
echo ""
echo "よく使うコマンド:"
echo "  show dbs                    - データベース一覧"
echo "  use user_data_db            - プロジェクトDBに切り替え"
echo "  show collections            - コレクション一覧"
echo "  db.users.find().pretty()    - データ表示"
echo "  db.users.countDocuments()   - 件数確認"
echo "  exit                        - 終了"
echo ""

# user_data_dbに直接接続
mongosh mongodb://localhost:27017/user_data_db
```

使用方法：
```bash
chmod +x connect_mongodb.sh
./connect_mongodb.sh
```
