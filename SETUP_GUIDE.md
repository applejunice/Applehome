# 🚀 クイックセットアップガイド

## ⚡ クイックスタート(3つのステップ)

### 第一ステップ: APIキーの取得(10分)

> **詳細な手順は `GET_API_KEYS.md` を参照してください**

**OpenWeatherMap API:**
1. 登録: https://home.openweathermap.org/users/sign_up
2. メール認証
3. API Keyを取得: https://home.openweathermap.org/api_keys
4. ⚠️ **新しいキーは有効化まで10分-2時間待つ必要があります**

**WAQI API:**
1. 申請: https://aqicn.org/data-platform/token/
2. 名前とメールを記入
3. すぐにTokenを取得(メールでも送信されます)

### 第二ステップ: APIキーの設定(1分)

**推奨方法: コードを直接修正**

1. テキストエディタで `backend/app.py` を開く
2. 12-13行目を見つけて、実際のキーに置き換える:

```python
# 修正前:
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'your_openweather_api_key_here')
WAQI_API_KEY = os.getenv('WAQI_API_KEY', 'your_waqi_api_key_here')

# 修正後(例):
OPENWEATHER_API_KEY = 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6'  # あなたのキーに置き換え
WAQI_API_KEY = '1234567890abcdef1234567890abcdef12345678'  # あなたのTokenに置き換え
```

3. ファイルを保存

## 第三ステップ: 依存関係のインストール

```bash
# backendディレクトリにいることを確認
cd backend

# Python依存関係をインストール
pip install -r requirements.txt

# またはpip3を使用
pip3 install -r requirements.txt
```

## 第四ステップ: サービスの起動

```bash
# バックエンドサービスを起動
python app.py

# またはpython3を使用
python3 app.py
```

以下のような出力が表示されるはずです:
```
 * Running on http://0.0.0.0:5000
 * Running on http://127.0.0.1:5000
```

## 第五ステップ: APIのテスト

### ブラウザでテスト

ブラウザで開く:
```
http://localhost:5000/api/walk-suitability?city=Tokyo
```

### curlでテスト

```bash
curl "http://localhost:5000/api/walk-suitability?city=Tokyo"
```

### フロントエンドインターフェースを使用

1. バックエンドサービスを実行したまま
2. ブラウザで `frontend/index.html` を開く
3. 都市名を入力して"查询"をクリック

### APIドキュメントを表示

ブラウザで `documentation/api-docs.html` を開き、完全なインタラクティブAPIドキュメントを確認。

## よくある質問

### Q: "ModuleNotFoundError: No module named 'flask'" が出る

**A:** 依存関係をインストールする必要があります:
```bash
pip install -r requirements.txt
```

### Q: APIが "天気データ取得失敗" エラーを返す

**A:** 以下の点を確認してください:
1. APIキーが正しく設定されているか確認
2. ネットワーク接続が正常か確認
3. 都市名は英語を使用(例: Tokyo, Beijing)

### Q: フロントエンドがバックエンドに接続できない

**A:** 以下を確認:
1. バックエンドサービスが実行中か(http://localhost:5000)
2. ブラウザがCORSクロスドメインリクエストを許可しているか
3. ブラウザコンソールにエラーメッセージがないか確認

### Q: 都市の検索を変更するには？

**A:**
- フロントエンドインターフェースで直接都市名を入力(英語)
- またはAPIリクエストでcityパラメータを変更
- 対応都市例: Tokyo, Beijing, Shanghai, London, Paris, New York, Seoul

## 対応都市リスト(一部)

### アジア
- Tokyo, Osaka (日本)
- Beijing, Shanghai, Guangzhou, Shenzhen (中国)
- Seoul, Busan (韓国)
- Singapore (シンガポール)
- Bangkok (タイ)
- Hanoi, Ho Chi Minh City (ベトナム)

### ヨーロッパ
- London (イギリス)
- Paris (フランス)
- Berlin (ドイツ)
- Rome (イタリア)
- Madrid (スペイン)

### アメリカ
- New York, Los Angeles, Chicago (米国)
- Toronto (カナダ)

### オセアニア
- Sydney, Melbourne (オーストラリア)

## 次のステップ

- `README_PROJECT.md` でプロジェクト詳細を確認
- `documentation/api-docs.html` で完全なAPIドキュメントを確認
- 異なる都市のクエリを試す
- 必要に応じて評価アルゴリズムをカスタマイズ
