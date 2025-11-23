# 🎓 使用開始 - Walk Suitability API

## 📌 発生したエラー

```
❌ エラー: 天気データ取得失敗: 401 Client Error: Unauthorized
```

**原因:** APIキーがまだ設定されていません

**解決方法:** 以下の3つのステップに従ってください 👇

---

## ⚡ 3ステップクイックスタート

### ステップ1️⃣: 無料APIキーの取得

#### OpenWeatherMap API (天気データ)

1. ブラウザで開く: https://home.openweathermap.org/users/sign_up
2. アカウント登録(ユーザー名、メール、パスワードを入力)
3. メール認証(受信箱を確認し、認証リンクをクリック)
4. ログイン後アクセス: https://home.openweathermap.org/api_keys
5. API Keyをコピー(例: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)
6. ⚠️ **重要: 新しいキーは使用できるまで10分-2時間待つ必要があります**

#### World Air Quality Index API (空気質データ)

1. ブラウザで開く: https://aqicn.org/data-platform/token/
2. フォームに記入:
   - Your name: あなたの名前
   - Email address: あなたのメール
   - Category: "Education and Research"を選択
3. Submitをクリック、すぐにTokenを取得(メールでも送信されます)
4. Tokenをコピー(例: `1234567890abcdef1234567890abcdef12345678`)

---

### ステップ2️⃣: APIキーの設定

1. テキストエディタ(メモ帳、VS Codeなど)でファイルを開く:
   ```
   backend/app.py
   ```

2. 12-13行目を見つける、次のようになっています:
   ```python
   OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'your_openweather_api_key_here')
   WAQI_API_KEY = os.getenv('WAQI_API_KEY', 'your_waqi_api_key_here')
   ```

3. 実際のキーに変更(**行全体を削除し、以下の内容に置き換え**):
   ```python
   OPENWEATHER_API_KEY = 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6'  # あなたのOpenWeatherMapキーを貼り付け
   WAQI_API_KEY = '1234567890abcdef1234567890abcdef12345678'  # あなたのWAQI Tokenを貼り付け
   ```

4. **ファイルを保存** (Ctrl+S または Cmd+S)

---

### ステップ3️⃣: プロジェクトの実行

ターミナル(コマンドライン)を開き、以下のコマンドを実行:

```bash
# 1. backendディレクトリに移動
cd backend

# 2. 依存関係をインストール(一度だけ実行)
pip install -r requirements.txt

# 3. サービスを起動
python app.py
```

以下のような出力が表示されれば成功:
```
 * Running on http://127.0.0.1:5000
```

---

## 🎯 プロジェクトのテスト

### 方法1: フロントエンドインターフェースを使用
1. バックエンドサービスを実行したまま
2. ブラウザでファイルを開く: `frontend/index.html`
3. 都市名を入力(例: Tokyo)
4. "查询"ボタンをクリック

### 方法2: ブラウザで直接APIにアクセス
ブラウザで開く:
```
http://localhost:5000/api/walk-suitability?city=Tokyo
```

### 方法3: APIドキュメントを表示
ブラウザでファイルを開く: `documentation/api-docs.html`

---

## ❓ よくある質問

### Q1: まだ401エラーが表示される？
**考えられる原因:**
- APIキーのコピーエラー(余分なスペースがないか確認)
- OpenWeatherMapキーがまだ有効化されていない(10分-2時間待つ必要あり)

**解決方法:**
- キーを再コピーし、スペースがないことを確認
- しばらく待ってから再試行
- `backend/app.py` ファイルが保存されているか確認

### Q2: キーが正しいか確認する方法は？
ブラウザでこれら2つのURLをテスト(自分のキーに置き換え):

**天気APIをテスト:**
```
http://api.openweathermap.org/data/2.5/weather?q=Tokyo&appid=あなたのOpenWeatherMapキー&units=metric
```

**空気質APIをテスト:**
```
http://api.waqi.info/feed/Tokyo/?token=あなたのWAQI_Token
```

両方ともデータを表示できれば、キーは正しいです。

### Q3: ModuleNotFoundError エラー？
```bash
pip install -r requirements.txt
```

---

## 📚 詳細ヘルプ

- **詳細なAPIキー取得ガイド**: `GET_API_KEYS.md` を参照
- **完全なセットアップ説明**: `SETUP_GUIDE.md` を参照
- **プロジェクト詳細ドキュメント**: `README_PROJECT.md` を参照
- **日本語概要**: `README_CN.md` を参照

---

## ✅ チェックリスト

完了後に確認:

- [ ] OpenWeatherMap API Keyを取得済み
- [ ] WAQI Tokenを取得済み
- [ ] `backend/app.py` ファイルを修正済み
- [ ] 修正を保存済み
- [ ] 依存関係をインストール済み (`pip install -r requirements.txt`)
- [ ] バックエンドサービスが起動できる
- [ ] フロントエンドインターフェースがデータを表示できる

---

## 🎉 次のステップ

設定成功後:
1. 異なる都市をテスト(Tokyo, Beijing, London, Parisなど)
2. 結果のスクリーンショットを保存(レポート用)
3. APIドキュメントインターフェースを確認
4. 課題レポートを完成させる

課題の成功を祈ります！
