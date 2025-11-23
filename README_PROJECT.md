# Walk Suitability API - 散歩適性指数サービス

## 📖 プロジェクト概要

本プロジェクトは、**2つのオープンソースサードパーティAPI**を統合することで、ユーザーに科学的で包括的な散歩提案を提供する革新的なWebサービスです。システムはリアルタイムの天気と空気質データに基づいて、独自の「散歩適性指数」(0-100点)を計算します。

## 🌟 プロジェクトの特徴

### 使用するオープンソースサードパーティAPI

1. **OpenWeatherMap API** (https://openweathermap.org/api)
   - リアルタイム天気データを提供
   - 気温、湿度、風速、天気状況などの情報を含む
   - 無料API、毎分60回の呼び出し制限

2. **World Air Quality Index API** (https://aqicn.org/api/)
   - 世界の都市の空気質指数(AQI)を提供
   - PM2.5、PM10、O3、NO2などの汚染物質データを含む
   - 無料API、毎分1000回の呼び出し制限

### データ融合方法

本サービスは革新的な加重アルゴリズムで2つのAPIのデータを融合します:

- **気温の重み: 25%** - 気温が屋外活動に適しているかを評価(最適範囲15-25°C)
- **天気状況の重み: 25%** - 天気タイプを判定(晴天、雨天、雪天など)
- **空気質の重み: 30%** - AQI指数に基づいて空気汚染度を評価
- **湿度の重み: 10%** - 人体の快適度を考慮(最適範囲40-70%)
- **風速の重み: 10%** - 風の影響を評価(最適範囲<5m/s)

最終的に総合的な散歩適性指数を出力し、具体的な提案を提供します。

## 📁 プロジェクト構造

```
.
├── backend/
│   ├── app.py              # Flaskバックエンドアプリケーション
│   ├── requirements.txt    # Python依存関係
│   └── .env.example        # 環境変数サンプル
├── documentation/
│   ├── api-docs.html       # インタラクティブAPIドキュメント
│   └── api-docs.yml        # OpenAPI仕様
├── frontend/
│   └── index.html          # Webフロントエンドインターフェース
└── README_PROJECT.md       # プロジェクト説明ドキュメント
```

## 🚀 クイックスタート

### 前提条件

- Python 3.8+
- pip (Pythonパッケージマネージャー)

### 1. APIキーの取得

#### OpenWeatherMap API
1. https://openweathermap.org/api にアクセス
2. 無料アカウントを登録
3. "API keys"ページでAPIキーを取得

#### World Air Quality Index API
1. https://aqicn.org/api/ にアクセス
2. 申請フォームに記入して無料APIトークンを取得
3. 通常、すぐにメールでトークンが送信されます

### 2. 依存関係のインストール

```bash
cd backend
pip install -r requirements.txt
```

### 3. 環境変数の設定

```bash
# 環境変数サンプルファイルをコピー
cp .env.example .env

# .envファイルを編集し、APIキーを入力
# OPENWEATHER_API_KEY=あなたのOpenWeatherMapキー
# WAQI_API_KEY=あなたのWAQIキー
```

または、app.pyで直接APIキーを変更(本番環境には推奨されません):

```python
OPENWEATHER_API_KEY = 'your_actual_api_key_here'
WAQI_API_KEY = 'your_actual_token_here'
```

### 4. バックエンドサービスの起動

```bash
cd backend
python app.py
```

サービスは http://localhost:5000 で起動します

### 5. フロントエンドインターフェースへアクセス

ブラウザで開く:
```
frontend/index.html
```

またはシンプルなHTTPサーバーを使用:
```bash
cd frontend
python -m http.server 8080
# その後 http://localhost:8080 にアクセス
```

### 6. APIドキュメントの表示

ブラウザで開く:
```
documentation/api-docs.html
```

## 📡 APIエンドポイント

### 1. 散歩適性指数の取得
```
GET /api/walk-suitability?city={city_name}
```

**例:**
```bash
curl "http://localhost:5000/api/walk-suitability?city=Tokyo"
```

**レスポンス:**
```json
{
  "success": true,
  "city": "Tokyo",
  "timestamp": "2025-11-19T10:30:00",
  "suitability": {
    "score": 85.5,
    "level": "非常に適している",
    "recommendation": "今は散歩に最適な時間です！",
    "reasons": ["天気と空気質が両方とも良好です"],
    "details": {
      "temperature_score": 100.0,
      "weather_score": 100.0,
      "humidity_score": 80.0,
      "wind_score": 100.0,
      "aqi_score": 80.0
    }
  },
  "weather": {
    "temperature": 22.5,
    "feels_like": 21.8,
    "humidity": 65,
    "weather": "Clear",
    "weather_description": "clear sky",
    "wind_speed": 3.5,
    "clouds": 20
  },
  "air_quality": {
    "aqi": 45,
    "pm25": 12.5,
    "pm10": 25.3,
    "o3": 30.2,
    "no2": 15.8
  }
}
```

### 2. 天気データの取得
```
GET /api/weather?city={city_name}
```

### 3. 空気質データの取得
```
GET /api/air-quality?city={city_name}
```

### 4. ヘルスチェック
```
GET /health
```

## 📊 評価基準

| スコア範囲 | レベル | 提案 |
|---------|------|------|
| 80-100  | 非常に適している | 今は散歩に最適な時間です！ |
| 60-79   | 適している | 散歩に適していますが、一部の状況に注意してください |
| 40-59   | 普通 | 散歩できますが、条件はあまり理想的ではありません |
| 0-39    | 不適 | 散歩計画を延期することをお勧めします |

## 🎨 機能特性

- ✅ 2つの実際のオープンソースAPIを統合
- ✅ インテリジェントなデータ融合アルゴリズム
- ✅ 完全なOpenAPIドキュメント
- ✅ インタラクティブAPIドキュメントページ(Swagger UI)
- ✅ 美しいWebフロントエンドインターフェース
- ✅ リアルタイムデータクエリ
- ✅ 複数都市対応
- ✅ 詳細なスコア説明
- ✅ CORSサポート

## 🛠️ 技術スタック

### バックエンド
- **Flask** - Python Webフレームワーク
- **Flask-CORS** - クロスオリジンリソース共有サポート
- **Requests** - HTTPクライアントライブラリ

### フロントエンド
- **ネイティブHTML/CSS/JavaScript** - 追加フレームワーク不要
- **Swagger UI** - APIドキュメント表示

### APIドキュメント
- **OpenAPI 3.0.3** - API仕様標準

## 🔧 開発説明

### 新しい評価要素の追加

`app.py`の`calculate_walk_suitability`関数に新しい評価ロジックを追加:

```python
def calculate_walk_suitability(weather_data, air_quality_data):
    # 新しい評価要素を追加
    new_factor_score = calculate_new_factor(weather_data)

    # 重みを更新
    weights = {
        'temp': 0.20,
        'weather': 0.20,
        'humidity': 0.10,
        'wind': 0.10,
        'aqi': 0.30,
        'new_factor': 0.10  # 新規追加
    }

    # 最終スコア計算を更新
    final_score = (
        temp_score * weights['temp'] +
        # ... その他の要素
        new_factor_score * weights['new_factor']
    )
```

### より多くの都市対応

APIはOpenWeatherMapとWAQIがサポートするすべての都市に対応しています。クエリパラメータに都市名(英語)を渡すだけで使用できます。

### カスタム評価基準

`calculate_walk_suitability`関数の評価ロジックを変更することで、評価基準をカスタマイズできます。

## 📝 注意事項

1. **API制限**: 無料APIには呼び出し回数制限があります、頻繁にリクエストしないでください
2. **都市名**: 英語の都市名を使用してクエリ(例: Tokyo, Beijing, London)
3. **データ精度**: データはサードパーティAPIから取得され、精度はデータソースに依存します
4. **CORS**: CORSサポートが設定されており、任意のドメインからAPIにアクセスできます

## 🤝 貢献

IssueとPull Requestの提出を歓迎します！

## 📄 ライセンス

MIT License

## 👤 著者

[あなたの名前/学籍番号]

## 🙏 謝辞

- OpenWeatherMap - 天気データAPIを提供
- World Air Quality Index - 空気質データAPIを提供
- Flask - 優れたPython Webフレームワーク
