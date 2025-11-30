# User Service API ドキュメント

## 基本情報

- **Base URL**: `http://localhost:5002`
- **Content-Type**: `application/json`
- **認証方式**: JWT Bearer Token

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

### 2. ユーザーログイン

**POST** `/api/login`

#### リクエストパラメータ

| パラメータ | 型 | 必須 | 説明 |
|------------|------|------|------|
| username | string | はい | ユーザー名 |
| password | string | はい | パスワード |

#### リクエスト例

```json
{
  "username": "alice",
  "password": "123456"
}
```

#### レスポンス例

```json
{
  "success": true,
  "message": "ログインしました",
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "username": "alice",
    "balance": 1000.0
  }
}
```

---

### 3. 全ユーザー残高照会

**GET** `/api/users/balances`

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

### 4. 送金

**POST** `/api/transfer`

> ログイン認証が必要です

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

### 5. 現在のユーザー情報取得

**GET** `/api/me`

> ログイン認証が必要です

#### リクエストヘッダー

| Header | 値 |
|--------|-----|
| Authorization | Bearer {token} |

#### レスポンス例

```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "alice",
    "balance": 900.0,
    "created_at": "2024-01-01T12:00:00"
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

### 一般的なHTTPステータスコード

| HTTPステータスコード | 説明 |
|---------------------|------|
| 400 | リクエストパラメータエラー |
| 401 | 未認証または認証失敗 |
| 404 | リソースが存在しません |
| 500 | サーバー内部エラー |
