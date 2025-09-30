from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import json
from datetime import datetime
from mongodb_uploader import MongoDBUploader

app = FastAPI(title="User Data API", description="MongoDB User Data Management API")

# CORS設定（フロントエンドからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静的ファイル（フロントエンド）を配信
app.mount("/static", StaticFiles(directory="static"), name="static")

# データモデル
class UserData(BaseModel):
    id: int
    product: str
    price: float

class UserDataCreate(BaseModel):
    product: str
    price: float

# MongoDB接続を管理するグローバル変数
uploader = MongoDBUploader()

@app.on_event("startup")
async def startup_event():
    """アプリケーション起動時にMongoDBに接続"""
    if not uploader.connect():
        print("⚠️ MongoDB接続に失敗しました。一部の機能が制限される可能性があります。")

@app.on_event("shutdown")
async def shutdown_event():
    """アプリケーション終了時にMongoDB接続を切断"""
    uploader.disconnect()

@app.get("/")
async def root():
    """ルートエンドポイント - フロントエンド画面を返す"""
    with open("static/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/api/users", response_model=List[dict])
async def get_users():
    """全ユーザーデータを取得"""
    try:
        if uploader.database is None:
            raise HTTPException(status_code=500, detail="MongoDB接続エラー")
        
        collection = uploader.database["users"]
        users = list(collection.find({}, {"_id": 0}))  # _idフィールドを除外
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"データ取得エラー: {str(e)}")

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    """特定のユーザーデータを取得"""
    try:
        if uploader.database is None:
            raise HTTPException(status_code=500, detail="MongoDB接続エラー")
        
        collection = uploader.database["users"]
        user = collection.find_one({"id": user_id}, {"_id": 0})
        
        if user is None:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
        
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"データ取得エラー: {str(e)}")

@app.post("/api/users", response_model=dict)
async def create_user(user_data: UserDataCreate):
    """新しいユーザーデータを作成"""
    try:
        if uploader.database is None:
            raise HTTPException(status_code=500, detail="MongoDB接続エラー")
        
        collection = uploader.database["users"]
        
        # 新しいIDを生成（既存の最大ID + 1）
        max_id_doc = collection.find().sort("id", -1).limit(1)
        max_id = 0
        for doc in max_id_doc:
            max_id = doc.get("id", 0)
        
        new_user = {
            "id": max_id + 1,
            "product": user_data.product,
            "price": user_data.price,
            "source_file": "api_created",
            "uploaded_at": datetime.now()
        }
        
        result = collection.insert_one(new_user)
        
        if result.inserted_id:
            # 作成したユーザーを返す（_idフィールドを除外）
            created_user = collection.find_one({"_id": result.inserted_id}, {"_id": 0})
            return created_user
        else:
            raise HTTPException(status_code=500, detail="ユーザー作成に失敗")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ユーザー作成エラー: {str(e)}")

@app.put("/api/users/{user_id}")
async def update_user(user_id: int, user_data: UserDataCreate):
    """ユーザーデータを更新"""
    try:
        if uploader.database is None:
            raise HTTPException(status_code=500, detail="MongoDB接続エラー")
        
        collection = uploader.database["users"]
        
        update_data = {
            "product": user_data.product,
            "price": user_data.price,
        }
        
        result = collection.update_one({"id": user_id}, {"$set": update_data})
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
        
        # 更新されたユーザーを返す
        updated_user = collection.find_one({"id": user_id}, {"_id": 0})
        return updated_user
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ユーザー更新エラー: {str(e)}")

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int):
    """ユーザーデータを削除"""
    try:
        if uploader.database is None:
            raise HTTPException(status_code=500, detail="MongoDB接続エラー")
        
        collection = uploader.database["users"]
        result = collection.delete_one({"id": user_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
        
        return {"message": f"ユーザーID {user_id} を削除しました"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ユーザー削除エラー: {str(e)}")

@app.get("/api/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    mongodb_status = "connected" if uploader.database is not None else "disconnected"
    return {
        "status": "ok",
        "mongodb": mongodb_status,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)