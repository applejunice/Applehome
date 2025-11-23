# 🔑 APIキー取得ガイド

## 第一ステップ: OpenWeatherMap APIキーの取得

### 1. 登録ページにアクセス
ブラウザで開く: https://home.openweathermap.org/users/sign_up

### 2. 登録情報を記入
- **Username**: あなたのユーザー名
- **Email**: あなたのメール
- **Password**: パスワードを設定
- サービス規約に同意
- "Create Account"をクリック

### 3. メール認証
- メール受信箱を確認
- 認証リンクをクリック

### 4. APIキーを取得
- ログイン後アクセス: https://home.openweathermap.org/api_keys
- またはナビゲーションバーの "API keys" をクリック
- デフォルトのAPI keyが表示されます
- このキーをコピー(例: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)

### 5. 有効化を待つ
⚠️ **重要**: 新しく作成したAPIキーは使用できるまで **10分から2時間** 待つ必要があります

---

## 第二ステップ: World Air Quality Index API Tokenの取得

### 1. 申請ページにアクセス
ブラウザで開く: https://aqicn.org/data-platform/token/

### 2. 申請フォームに記入
以下の情報を記入:
- **Your name**: あなたの名前
- **Email address**: あなたのメール
- **Category**: "Education and Research" または "Personal" を選択

### 3. 申請を提出
- "Submit" ボタンをクリック
- システムがすぐにTokenを表示
- Token形式は例: `1234567890abcdef1234567890abcdef12345678`

### 4. Tokenを保存
- 表示されたTokenをコピー
- Tokenはメールでも送信されます

---

## 第三ステップ: プロジェクトへのAPIキー設定

### 方法1: コードを直接修正(最も簡単)

1. テキストエディタでファイルを開く:
   ```
   backend/app.py
   ```

2. 12-13行目を見つける:
   ```python
   OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'your_openweather_api_key_here')
   WAQI_API_KEY = os.getenv('WAQI_API_KEY', 'your_waqi_api_key_here')
   ```

3. 実際のキーに変更(あなたの実際のキーに置き換え):
   ```python
   OPENWEATHER_API_KEY = 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6'  # あなたのOpenWeatherMapキー
   WAQI_API_KEY = '1234567890abcdef1234567890abcdef12345678'  # あなたのWAQI Token
   ```

4. ファイルを保存

### 方法2: 環境変数を使用(本番環境推奨)

1. `backend/` ディレクトリに `.env` ファイルを作成:
   ```bash
   cd backend
   cp .env.example .env
   ```

2. `.env` ファイルを編集:
   ```bash
   OPENWEATHER_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
   WAQI_API_KEY=1234567890abcdef1234567890abcdef12345678
   ```

3. python-dotenvをインストール(まだインストールしていない場合):
   ```bash
   pip install python-dotenv
   ```

---

## 第四ステップ: APIキーのテスト

### 1. サービスを起動
```bash
cd backend
python app.py
```

### 2. APIをテスト

#### テスト方法A: ブラウザを使用
ブラウザで開く:
```
http://localhost:5000/api/walk-suitability?city=Tokyo
```

成功すれば、天気と空気質情報を含むJSONデータが表示されます。

#### テスト方法B: テストスクリプトを使用
```bash
cd backend
python test_api.py
```

#### テスト方法C: curlを使用
```bash
curl "http://localhost:5000/api/walk-suitability?city=Tokyo"
```

---

## よくある質問

### ❌ 401 Unauthorized エラー

**原因:**
- APIキーが未設定または誤っている
- OpenWeatherMapキーがまだ有効化されていない(新しいキーは待つ必要あり)

**解決方法:**
1. キーが正しくコピーされているか確認
2. OpenWeatherMapキーの有効化まで10分から2時間待つ
3. 余分なスペースがないことを確認

### ❌ 404 エラー

**原因:**
- 都市名が正しくない

**解決方法:**
- 英語の都市名を使用(Tokyo, Beijing, London)
- スペルが正しいか確認

### ❌ WAQI APIが "Invalid key" を返す

**原因:**
- Tokenが正しくコピーされていない
- Token形式が誤っている

**解決方法:**
1. メールまたはWebサイトからTokenを再コピー
2. Tokenが完全であることを確認(通常40文字)

---

## 確認チェックリスト

設定完了後、以下を確認:

- [ ] OpenWeatherMapアカウントを登録しメール認証済み
- [ ] OpenWeatherMap APIキーを取得済み
- [ ] WAQI Tokenを取得済み
- [ ] 両方のキーを `backend/app.py` に設定済み
- [ ] OpenWeatherMapキーの有効化を待った(新しいキーの場合)
- [ ] サービスが正常に起動できる(`python app.py`)
- [ ] APIテストが正しいデータを返す

---

## クイックテスト例

キー取得後、これらのURLで直接テストできます:

### OpenWeatherMap APIをテスト
ブラウザで開く(あなたのキーに置き換え):
```
http://api.openweathermap.org/data/2.5/weather?q=Tokyo&appid=あなたのキー&units=metric
```

### WAQI APIをテスト
ブラウザで開く(あなたのTokenに置き換え):
```
http://api.waqi.info/feed/Tokyo/?token=あなたのToken
```

両方のURLがデータを返せば、キー設定は正しいです！

---

## まとめ

1. **OpenWeatherMapを登録** → API Keyを取得
2. **WAQI Tokenを申請** → すぐにTokenを取得
3. **プロジェクトに設定** → `backend/app.py` を修正
4. **有効化を待つ** → OpenWeatherMapは時間が必要
5. **起動してテスト** → `python app.py` + フロントエンドにアクセス

これらのステップを完了すれば、プロジェクトが正常に動作します！
