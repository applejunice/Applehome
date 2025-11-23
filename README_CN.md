# 散歩適性指数 API

## 🎯 プロジェクト概要

これは**OpenWeatherMap**天気APIと**World Air Quality Index**空気質APIを統合し、ユーザーに科学的な散歩提案を提供するインテリジェントなWebサービスです。

### コア機能

都市名入力 → 天気データ取得 + 空気質データ取得 → 融合計算 → 散歩適性指数出力(0-100点)

## 📊 データ融合アルゴリズム

| 評価要素 | 重み | 説明 |
|---------|------|------|
| 気温 | 25% | 最適範囲: 15-25°C |
| 天気状況 | 25% | 晴天が最適、雨雪で減点 |
| 空気質 | 30% | AQI指数で評価 |
| 湿度 | 10% | 最適範囲: 40-70% |
| 風速 | 10% | 最適範囲: <5m/s |

**最終スコア = 加重平均**

## 🚀 3分クイックスタート

### 1️⃣ 無料APIキーの取得

**OpenWeatherMap:**
- アクセス: https://openweathermap.org/api
- 登録してAPI Keyを取得

**World Air Quality Index:**
- アクセス: https://aqicn.org/api/
- フォーム記入でToken取得(すぐにメールで送信されます)

### 2️⃣ APIキーの設定

`backend/app.py` の12-13行目を編集:

```python
OPENWEATHER_API_KEY = 'あなたのOpenWeatherMapキー'
WAQI_API_KEY = 'あなたのWAQIキー'
```

### 3️⃣ インストールと実行

```bash
# 依存関係をインストール
cd backend
pip install -r requirements.txt

# サービス起動
python app.py
```

### 4️⃣ インターフェースへアクセス

- **フロントエンド**: ブラウザで `frontend/index.html` を開く
- **APIドキュメント**: ブラウザで `documentation/api-docs.html` を開く

## 📱 使用例

### Webインターフェース
1. `frontend/index.html` を開く
2. 都市名を入力(例: Tokyo, Beijing, London)
3. "查询"ボタンをクリック
4. 散歩適性指数と詳細データを確認

### API呼び出し
```bash
curl "http://localhost:5000/api/walk-suitability?city=Tokyo"
```

**レスポンス例:**
```json
{
  "success": true,
  "city": "Tokyo",
  "suitability": {
    "score": 85.5,
    "level": "非常に適している",
    "recommendation": "今は散歩に最適な時間です！"
  }
}
```

## 📁 プロジェクト構造

```
.
├── backend/              # バックエンドサービス
│   ├── app.py           # Flaskアプリケーション
│   ├── requirements.txt # 依存関係リスト
│   └── test_api.py      # テストスクリプト
│
├── documentation/        # APIドキュメント
│   ├── api-docs.yml     # OpenAPI仕様
│   └── api-docs.html    # インタラクティブドキュメント
│
├── frontend/            # フロントエンドインターフェース
│   └── index.html       # Webインターフェース
│
├── report/              # レポートフォルダ
│
└── README_PROJECT.md    # 詳細説明
```

## 🎓 課題要件対照

✅ **2つ以上の公開APIを呼び出し**
- OpenWeatherMap API (天気)
- World Air Quality Index API (空気質)

✅ **データ融合**
- 加重アルゴリズムで5次元データを融合
- ユニークな散歩適性指数を生成

✅ **OpenAPIドキュメント (YAML)**
- `documentation/api-docs.yml`

✅ **インタラクティブAPIドキュメント**
- `documentation/api-docs.html`
- Swagger UIベース

✅ **Webフロントエンド**
- `frontend/index.html`
- 美しくレスポンシブなデザイン

## 🛠️ 技術スタック

- **バックエンド**: Python + Flask + Flask-CORS
- **フロントエンド**: HTML + CSS + JavaScript
- **APIドキュメント**: OpenAPI 3.0 + Swagger UI
- **サードパーティAPI**: OpenWeatherMap + WAQI

## 📖 ドキュメント説明

- `README_PROJECT.md` - 完全なプロジェクトドキュメント(英語)
- `SETUP_GUIDE.md` - 詳細なセットアップガイド
- `CHECKLIST.md` - 提出前チェックリスト
- `README_CN.md` - このファイル(日本語概要)

## 🧪 テスト

```bash
# 自動テストを実行
cd backend
python test_api.py
```

## 💡 使用のヒント

1. **都市名**: 英語を使用(Tokyo, Beijing, Londonなど)
2. **API制限**: 無料APIには呼び出し回数制限があります、頻繁にリクエストしないでください
3. **ネットワーク要件**: 国際APIサービスにアクセスできる必要があります

## 🌍 対応都市(例)

- 日本: Tokyo, Osaka
- 中国: Beijing, Shanghai, Guangzhou
- 韓国: Seoul, Busan
- ヨーロッパ: London, Paris, Berlin, Rome
- アメリカ: New York, Los Angeles, Toronto

## 📝 レポートスクリーンショット推奨

1. フロントエンドインターフェースで高スコア表示(非常に適している)
2. フロントエンドインターフェースで低スコア表示(不適)
3. APIドキュメントページ
4. APIレスポンスデータ
5. 異なる都市の比較

## ⚠️ 注意事項

- ❌ 実際のAPIキーを含むファイルを提出しないでください
- ✅ `.env.example` をテンプレートとして使用
- ✅ レポートでAPIキーの取得方法を説明
- ✅ すべての機能が正常に動作することを確認してから提出

## 🎉 完了チェック

提出前に確認:
- [ ] コードが正常に動作する
- [ ] APIキーが設定済み(テスト用)
- [ ] すべてのエンドポイントが正常に応答
- [ ] フロントエンドインターフェースが正常に表示
- [ ] APIドキュメントが開ける
- [ ] レポートが完成しスクリーンショット含む
- [ ] ZIPファイルにすべての必要なファイルが含まれる

---

課題の成功を祈ります！🎓✨
