# User Service API ドキュメント

## 基本情報

- **Base URL**: `http://localhost:5002`
- **Content-Type**: `application/json`
- **認証方式**: JWT Bearer Token

---

## JWT 認証説明

### 認証の仕組み

本システムはJWT（JSON Web Token）を使用して認証を行います。

```
┌─────────┐      1. ログイン要求        ┌─────────┐
│         │  ─────────────────────────→ │         │
│ クライアント │                            │  サーバー  │
│         │  ←───────────────────────── │         │
└─────────┘      2. JWTトークン返却      └─────────┘
     │
     │  3. トークンを保存
     ▼
┌─────────┐      4. API要求 + Token     ┌─────────┐
│         │  ─────────────────────────→ │         │
│ クライアント │   Authorization: Bearer xxx │  サーバー  │
│         │  ←───────────────────────── │         │
└─────────┘      5. レスポンス           └─────────┘
```

### JWT トークン構造

JWTトークンは3つの部分で構成されています：

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFsaWNlIiwiaXNfYWRtaW4iOmZhbHNlLCJleHAiOjE3MzM2NTY0MDB9.xxxxx
└──────────── Header ────────────┘.└────────────────────── Payload ──────────────────────┘.└ Signature ┘
```

**Payload（ペイロード）の内容：**

| フィールド | 型 | 説明 |
|-----------|------|------|
| user_id | number | ユーザーID（管理员は0） |
| username | string | ユーザー名 |
| is_admin | boolean | 管理员フラグ |
| exp | number | トークン有効期限（Unix timestamp） |

### トークンの使用方法

認証が必要なAPIでは、リクエストヘッダーに以下を追加：

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**JavaScript例：**

```javascript
fetch('/api/transfer', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ to_username: 'bob', amount: 100 })
});
```

**curl例：**

```bash
curl -X POST http://localhost:5002/api/transfer \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -d '{"to_username": "bob", "amount": 100}'
```

### トークン有効期限

- デフォルト有効期限：**24時間**
- 有効期限切れの場合、401エラーが返されます
- 再度ログインして新しいトークンを取得してください

---

## ユーザー権限

本システムには2種類のユーザーがあります：

| ロール | 説明 | 利用可能なAPI |
|--------|------|---------------|
| 管理员 | システム管理者（config.tomlで設定） | 全API + 管理员専用API |
| 普通ユーザー | 一般登録ユーザー | 自分のデータのみアクセス可能 |

### 権限別API一覧

| API | 公開 | 普通ユーザー | 管理员 |
|-----|------|--------------|--------|
| POST /api/register | ✅ | - | - |
| POST /api/login | ✅ | - | - |
| GET /api/me | - | ✅ | ✅ |
| POST /api/transfer | - | ✅ | ❌ |
| GET /api/my/balance | - | ✅ | ❌ |
| GET /api/my/transactions | - | ✅ | ❌ |
| GET /api/users/balances | - | ❌ | ✅ |
| GET /api/transactions | - | ❌ | ✅ |
| PUT /api/admin/balance | - | ❌ | ✅ |

---

## API一覧

### 1. ユーザー登録

**POST** `/api/register`

#### リクエストパラメータ

| パラメータ | 型 | 必須 | 説明 |
|------------|------|------|------|
| username | string | はい | ユーザー名 (3〜50文字) |
| password | string | はい | パスワード (6文字以上) |
| balance | number | いいえ | 初期残高 (デフォルト: 0) |

#### リクエスト例

```json
{
  "username": "alice",
  "password": "123456",
  "balance": 1000
}
```

#### レスポンス例

```json
{
  "success": true,
  "message": "登録が完了しました",
  "user": {
    "id": 1,
    "username": "alice",
    "balance": 1000.0
  }
}
```

---

### 2. ユーザーログイン（管理员/普通ユーザー共用）

**POST** `/api/login`

#### リクエストパラメータ

| パラメータ | 型 | 必須 | 説明 |
|------------|------|------|------|
| username | string | はい | ユーザー名 |
| password | string | はい | パスワード |

#### リクエスト例（普通ユーザー）

```json
{
  "username": "alice",
  "password": "123456"
}
```

#### レスポンス例（普通ユーザー）

```json
{
  "success": true,
  "message": "ログインしました",
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "username": "alice",
    "balance": 1000.0,
    "is_admin": false
  }
}
```

#### リクエスト例（管理员）

```json
{
  "username": "admin",
  "password": "admin123456"
}
```

#### レスポンス例（管理员）

```json
{
  "success": true,
  "message": "管理员ログインしました",
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 0,
    "username": "admin",
    "is_admin": true
  }
}
```

---

### 3. 現在のユーザー情報取得

**GET** `/api/me`

> 🔒 ログイン認証が必要です

#### リクエストヘッダー

| Header | 値 |
|--------|-----|
| Authorization | Bearer {token} |

#### レスポンス例（普通ユーザー）

```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "alice",
    "balance": 900.0,
    "is_admin": false,
    "created_at": "2024-01-01T12:00:00"
  }
}
```

#### レスポンス例（管理员）

```json
{
  "success": true,
  "user": {
    "id": 0,
    "username": "admin",
    "is_admin": true
  }
}
```

---

### 4. 送金（普通ユーザー専用）

**POST** `/api/transfer`

> 🔒 ログイン認証が必要です（普通ユーザーのみ）

#### リクエストヘッダー

| Header | 値 |
|--------|-----|
| Authorization | Bearer {token} |

#### リクエストパラメータ

| パラメータ | 型 | 必須 | 説明 |
|------------|------|------|------|
| to_username | string | はい | 送金先ユーザー名 |
| amount | number | はい | 送金額 (0より大きい値) |

#### リクエスト例

```json
{
  "to_username": "bob",
  "amount": 100
}
```

#### レスポンス例

```json
{
  "success": true,
  "message": "bob へ 100.0 円を送金しました",
  "from_balance": 900.0,
  "to_balance": 100.0
}
```

---

### 5. 自分の残高照会（普通ユーザー専用）

**GET** `/api/my/balance`

> 🔒 ログイン認証が必要です（普通ユーザーのみ）

#### リクエストヘッダー

| Header | 値 |
|--------|-----|
| Authorization | Bearer {token} |

#### レスポンス例

```json
{
  "success": true,
  "balance": 900.0
}
```

---

### 6. 自分の転送記録照会（普通ユーザー専用）

**GET** `/api/my/transactions`

> 🔒 ログイン認証が必要です（普通ユーザーのみ）

#### リクエストヘッダー

| Header | 値 |
|--------|-----|
| Authorization | Bearer {token} |

#### レスポンス例

```json
{
  "success": true,
  "count": 2,
  "transactions": [
    {
      "id": 2,
      "from_user": "alice",
      "to_user": "bob",
      "amount": 50.0,
      "type": "transfer",
      "direction": "sent",
      "created_at": "2024-01-02T10:00:00"
    },
    {
      "id": 1,
      "from_user": "charlie",
      "to_user": "alice",
      "amount": 100.0,
      "type": "transfer",
      "direction": "received",
      "created_at": "2024-01-01T12:00:00"
    }
  ]
}
```

---

### 7. 全ユーザー残高照会（管理员専用）

**GET** `/api/users/balances`

> 🔒 管理员認証が必要です

#### リクエストヘッダー

| Header | 値 |
|--------|-----|
| Authorization | Bearer {admin_token} |

#### レスポンス例

```json
{
  "success": true,
  "count": 2,
  "users": [
    {
      "id": 1,
      "username": "alice",
      "balance": 900.0
    },
    {
      "id": 2,
      "username": "bob",
      "balance": 100.0
    }
  ]
}
```

---

### 8. 全転送記録照会（管理员専用）

**GET** `/api/transactions`

> 🔒 管理员認証が必要です

#### リクエストヘッダー

| Header | 値 |
|--------|-----|
| Authorization | Bearer {admin_token} |

#### レスポンス例

```json
{
  "success": true,
  "count": 2,
  "transactions": [
    {
      "id": 2,
      "from_user": "alice",
      "to_user": "bob",
      "amount": 50.0,
      "type": "transfer",
      "created_at": "2024-01-02T10:00:00"
    },
    {
      "id": 1,
      "from_user": "charlie",
      "to_user": "alice",
      "amount": 100.0,
      "type": "transfer",
      "created_at": "2024-01-01T12:00:00"
    }
  ]
}
```

---

### 9. ユーザー残高修正（管理员専用）

**PUT** `/api/admin/balance`

> 🔒 管理员認証が必要です

#### リクエストヘッダー

| Header | 値 |
|--------|-----|
| Authorization | Bearer {admin_token} |

#### リクエストパラメータ

| パラメータ | 型 | 必須 | 説明 |
|------------|------|------|------|
| username | string | はい | 対象ユーザー名 |
| balance | number | はい | 新しい残高 (0以上) |

#### リクエスト例

```json
{
  "username": "alice",
  "balance": 5000
}
```

#### レスポンス例

```json
{
  "success": true,
  "message": "alice の残高を更新しました",
  "user": {
    "id": 1,
    "username": "alice",
    "old_balance": 900.0,
    "new_balance": 5000.0
  }
}
```

---

## エラーレスポンス

すべてのエラーレスポンスは以下の形式です：

```json
{
  "success": false,
  "error": "エラーメッセージ"
}
```

### HTTPステータスコード一覧

| HTTPステータスコード | 説明 |
|---------------------|------|
| 400 | リクエストパラメータエラー |
| 401 | 未認証または認証失敗（トークンなし/期限切れ/無効） |
| 403 | 権限不足（管理员専用APIに普通ユーザーがアクセス） |
| 404 | リソースが存在しません |
| 500 | サーバー内部エラー |

### 認証関連のエラーメッセージ

| エラーメッセージ | 原因 |
|-----------------|------|
| 認証トークンがありません | Authorizationヘッダーがない |
| トークンの有効期限が切れています | JWTトークンが期限切れ |
| 無効なトークンです | JWTトークンが不正 |
| 管理员権限が必要です | 管理员専用APIに普通ユーザーがアクセス |

---

## 設定ファイル

### config.toml

```toml
[server]
host = "0.0.0.0"
port = 5002
debug = true

[database]
host = "localhost"
port = 5432
name = "userdb"
user = "dbuser"
password = "dbpassword"

[jwt]
secret_key = "your-secret-key-here"
expires_hours = 24

[admin]
username = "admin"
password = "admin123456"
```

| セクション | キー | 説明 |
|-----------|------|------|
| jwt.secret_key | JWTトークン署名用の秘密鍵 |
| jwt.expires_hours | トークン有効期限（時間） |
| admin.username | 管理员ユーザー名 |
| admin.password | 管理员パスワード（平文） |
