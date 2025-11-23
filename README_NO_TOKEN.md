# 🎉 トークン不要版 - すぐに使えます！

## ✨ 良いお知らせ

**いかなるトークンやAPIキーも不要**な版を作成しました！

### 使用するAPI

1. **Open-Meteo Weather API** (https://open-meteo.com)
   - 完全無料
   - 登録不要
   - APIキー不要
   - 天気データを提供

2. **Open-Meteo Air Quality API** (https://open-meteo.com)
   - 完全無料
   - 登録不要
   - APIキー不要
   - 空気質データを提供

## 🚀 すぐに使用(2ステップ)

### ステップ1: 依存関係のインストール

```bash
cd backend
pip install -r requirements.txt
```

### ステップ2: トークン不要版を実行

```bash
python app_no_token.py
```

これだけです！**いかなるキーも設定不要**！

## 🎯 テスト

### 方法1: フロントエンドインターフェースを使用
1. バックエンドサービスを実行したまま
2. ブラウザで開く: `frontend/index.html`
3. 都市名を入力(例: Tokyo, Beijing, London)
4. "查询"をクリック

### 方法2: APIに直接アクセス
ブラウザで開く:
```
http://localhost:5000/api/walk-suitability?city=Tokyo
```

### 方法3: APIドキュメントを表示
ブラウザで開く: `documentation/api-docs.html`

## 📊 対応都市

世界の主要都市に対応(英語名):
- Tokyo, Osaka (日本)
- Beijing, Shanghai, Guangzhou (中国)
- Seoul, Busan (韓国)
- London, Paris, Berlin, Rome (ヨーロッパ)
- New York, Los Angeles, Chicago (米国)
- Sydney, Melbourne (オーストラリア)

## 🆚 2つのバージョンの比較

### app.py (トークン必要)
✅ OpenWeatherMap + WAQIを使用
❌ 登録してAPIキーを取得する必要あり
⏱️ セットアップに5-10分必要

### app_no_token.py (推奨)
✅ Open-Meteo APIを使用
✅ 完全無料、登録不要
✅ すぐに使用可能、設定ゼロ
⏱️ セットアップ0分

## 📝 課題要件の適合性

✅ **少なくとも2つの異なる公開APIを呼び出し**
- Open-Meteo Weather API
- Open-Meteo Air Quality API

✅ **データ融合**
- 加重アルゴリズムで天気と空気質を融合
- 散歩適性指数を生成

✅ **課題要件に完全適合**

## ⚡ クイックスタートコマンド

コピー&ペースト実行:

```bash
# 1. ディレクトリに移動
cd backend

# 2. 依存関係をインストール(一度だけ)
pip install -r requirements.txt

# 3. トークン不要版を実行
python app_no_token.py
```

その後ブラウザで `frontend/index.html` を開くだけ！

## 💡 トークン必要版に切り替えたい場合

後でOpenWeatherMapとWAQIを使用したい場合(データがより正確かもしれません):

```bash
# APIキー取得後
python app.py
```

しかし課題には **app_no_token.py で十分**！

---

## 🎓 まとめ

`app_no_token.py` を使用する利点:
- ✅ 設定ゼロ、すぐに実行
- ✅ アカウント登録不要
- ✅ APIキーの有効化を待つ必要なし
- ✅ 課題要件に完全適合
- ✅ データは正確で信頼できる

**このバージョンでの課題完了を推奨！**
