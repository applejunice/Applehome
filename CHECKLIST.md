# ✅ プロジェクトチェックリスト

## 提出前チェック

### 📋 ファイル完全性チェック

- [x] **backend/** フォルダ
  - [x] app.py - Flaskアプリケーションメインファイル
  - [x] requirements.txt - Python依存関係リスト
  - [x] .env.example - 環境変数テンプレート
  - [x] test_api.py - APIテストスクリプト

- [x] **documentation/** フォルダ
  - [x] api-docs.yml - OpenAPI仕様ファイル(YAML形式)
  - [x] api-docs.html - インタラクティブAPIドキュメントページ

- [x] **frontend/** フォルダ
  - [x] index.html - Webフロントエンドインターフェース

- [x] **ルートディレクトリ**
  - [x] README_PROJECT.md - プロジェクト説明ドキュメント
  - [x] SETUP_GUIDE.md - クイックセットアップガイド
  - [x] CHECKLIST.md - このチェックリスト

### 🔍 機能チェック

#### バックエンドAPI
- [ ] Flaskサービスが起動できる
- [ ] `/health` エンドポイントが正常に応答
- [ ] `/` エンドポイントがAPI情報を返す
- [ ] `/api/weather` が天気データを取得できる
- [ ] `/api/air-quality` が空気質データを取得できる
- [ ] `/api/walk-suitability` が散歩適性指数を取得できる

#### フロントエンドインターフェース
- [ ] ページが正常に開ける
- [ ] 都市名を入力できる
- [ ] 検索ボタンをクリックして応答がある
- [ ] 散歩適性指数が正しく表示される
- [ ] 天気詳細が表示される
- [ ] 空気質詳細が表示される
- [ ] 人気都市タグがクリックできる

#### APIドキュメント
- [ ] api-docs.html が正常に開ける
- [ ] Swagger UIが正しく読み込まれる
- [ ] すべてのAPIエンドポイントが表示される
- [ ] オンラインでAPIをテストできる(Try it out)

### 📝 コード品質チェック

- [x] 2つの異なる公開APIを使用
  - [x] OpenWeatherMap API (天気データ)
  - [x] World Air Quality Index API (空気質)

- [x] データ融合の実装
  - [x] 複数のデータソースを統合
  - [x] 加重アルゴリズムを使用して計算
  - [x] 詳細なスコア説明を提供

- [x] OpenAPIドキュメント
  - [x] YAML形式が正しい
  - [x] すべてのエンドポイントを含む
  - [x] リクエスト/レスポンス例を含む
  - [x] データモデル定義を含む

- [x] コード規範
  - [x] 適切なコメントがある
  - [x] 機能が明確
  - [x] エラー処理が完備
  - [x] CORS設定が正しい

### 🧪 テストチェック

#### 手動テスト手順

1. **バックエンドテスト**
```bash
# 1. サービスを起動
cd backend
python app.py

# 2. 新しいターミナルを開き、テストスクリプトを実行
python test_api.py

# 3. またはcurlでテスト
curl "http://localhost:5000/health"
curl "http://localhost:5000/api/walk-suitability?city=Tokyo"
```

2. **フロントエンドテスト**
```bash
# ブラウザで frontend/index.html を開く
# 以下の機能をテスト:
- "Tokyo" を入力して検索
- 人気都市タグをクリック
- スコア詳細を確認
- レスポンシブデザインを確認
```

3. **ドキュメントテスト**
```bash
# ブラウザで documentation/api-docs.html を開く
# 以下の機能をテスト:
- Swagger UIが正しく読み込まれる
- 各エンドポイントを展開できる
- "Try it out" 機能が正常
- サンプルレスポンスが正しく表示される
```

### 📦 パッケージング準備

#### レポートで説明すべき内容

1. **プロジェクトアイデア**
   - 散歩適性指数の概念
   - なぜ天気と空気質の2つのAPIを選んだか
   - ユーザーがより良い決定をするのをどう助けるか

2. **実装内容**
   - 使用した技術スタック(Flask, JavaScript, OpenAPI)
   - データ融合アルゴリズムの設計
   - スコア重みの考慮要素
   - API設計の考え方

3. **使用例スクリーンショット**
   - [ ] フロントエンドインターフェースのスクリーンショット(異なるスコアレベル)
   - [ ] APIドキュメントページのスクリーンショット
   - [ ] APIレスポンスデータのスクリーンショット
   - [ ] 異なる都市の検索結果

4. **API情報**
   - OpenWeatherMap APIの使用説明
   - WAQI APIの使用説明
   - APIキーの取得方法

#### ZIPファイルの作成

```bash
# プロジェクトルートディレクトリで実行
cd ..
zip -r walk-suitability-api.zip Applehome \
  -x "Applehome/.git/*" \
  -x "Applehome/__pycache__/*" \
  -x "Applehome/.env" \
  -x "Applehome/*/.*"
```

または手動でパッケージング:
1. 以下のフォルダを選択: backend, documentation, frontend, report
2. 以下のファイルを選択: README_PROJECT.md, SETUP_GUIDE.md
3. 右クリック → 圧縮

### 📊 レポートチェック

レポートに含めるべき内容:

- [ ] **表紙**
  - プロジェクト名
  - 学生情報
  - 日付

- [ ] **プロジェクト概要**
  - プロジェクトアイデアの説明
  - 解決する問題
  - ターゲットユーザー

- [ ] **技術実装**
  - 使用したAPIの説明(公式サイトリンクを含む)
  - データ融合方法の詳細
  - システムアーキテクチャ図
  - 技術スタックの説明

- [ ] **機能展示**
  - 主要機能リスト
  - 使用フロー説明
  - スクリーンショット(少なくとも3-5枚)

- [ ] **APIドキュメント**
  - エンドポイントリスト
  - リクエスト/レスポンス例
  - OpenAPI仕様の説明

- [ ] **使用説明**
  - APIキーの取得方法
  - プロジェクトの実行方法
  - よくある質問への回答

- [ ] **まとめと展望**
  - プロジェクトの特徴
  - 遭遇した課題
  - 今後の改善方向

### 🎯 評価ポイントチェック

課題要件に基づく:

- [x] ✅ 少なくとも2つの異なる公開APIを呼び出し
  - OpenWeatherMap API
  - World Air Quality Index API

- [x] ✅ APIデータを融合
  - 加重アルゴリズムで天気と空気質データを融合
  - 独自の「散歩適性指数」を生成

- [x] ✅ OpenAPIドキュメント(YAML形式)
  - documentation/api-docs.yml

- [x] ✅ インタラクティブAPIドキュメント(api-docs.html)
  - Swagger UIを使用
  - ブラウザでエンドポイントをテスト可能

- [x] ✅ Webフロントエンドインターフェース
  - frontend/index.html
  - 美しく使いやすい

- [x] ✅ 完全なコードとドキュメント
  - コードコメントが充実
  - README説明が詳細
  - セットアップガイドを提供

### 🚀 最終提出

提出内容に含めるべき:

```
walk-suitability-api.zip
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── .env.example
│   └── test_api.py
├── documentation/
│   ├── api-docs.html
│   └── api-docs.yml
├── frontend/
│   └── index.html
├── report/
│   └── [あなたの学籍番号].pdf
├── README_PROJECT.md
└── SETUP_GUIDE.md
```

### ⚠️ 注意事項

- [ ] `.env` ファイルを提出に**含めない**(実際のAPIキーを含むため)
- [ ] `.env.example` のみをテンプレートとして提出
- [ ] レポートに実際のAPIキーを**含めない**
- [ ] コード内のAPIキーは環境変数を使用
- [ ] すべての機能が正常に動作することをテスト
- [ ] ドキュメント説明が明確で完全
- [ ] スクリーンショットが鮮明に見える
- [ ] ZIPファイルが正常に解凍できる

---

## ✨ 完了チェック

上記のすべての項目が完了していれば、おめでとうございます！プロジェクトは提出準備が整いました！

良い成績を祈ります！🎓
