import os
import json
from mongodb_uploader import MongoDBUploader

data_records = [
    {"id": 1, "product": "Laptop", "price": 1200.0},
    {"id": 2, "product": "Mouse", "price": 25.5},
    {"id": 3, "product": "Monitor", "price": 350.99},
    {"id": 4, "product": "Keyboard", "price": 75.0}
]

output_dir = "user_data_files"
os.makedirs(output_dir, exist_ok=True) # ディレクトリがない場合は作成

# JSONファイルを作成
for record in data_records:
    file_name = f"{output_dir}/user_{record['id']}.json"
    
    with open(file_name, 'w', encoding='utf-8') as f:
        json_line = json.dumps(record, ensure_ascii=False) + '\n'
        f.write(json_line)

print(f"✅ 個別のJSONファイルが '{output_dir}/' ディレクトリに作成されました。")

# MongoDBにアップロード
print("\n🚀 MongoDBへのアップロードを開始...")
uploader = MongoDBUploader()

try:
    if uploader.connect():
        success = uploader.upload_json_files(output_dir)
        if success:
            print("🎉 MongoDBへのアップロードが完了しました！")
            uploader.show_collection_data()
        else:
            print("⚠️ アップロード中にエラーが発生しました")
    else:
        print("❌ MongoDB接続に失敗しました。MongoDBサーバーが起動していることを確認してください。")
finally:
    uploader.disconnect()
