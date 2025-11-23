#!/usr/bin/env python3
"""
APIテストスクリプト
Walk Suitability APIの各エンドポイントをテスト
"""

import requests
import json
import sys

BASE_URL = "http://localhost:5000"

def print_section(title):
    """区切り線を印刷"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def test_health():
    """ヘルスチェックエンドポイントのテスト"""
    print_section("/health エンドポイントのテスト")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def test_root():
    """ルートパスのテスト"""
    print_section("/ エンドポイントのテスト")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def test_weather(city="Tokyo"):
    """天気APIのテスト"""
    print_section(f"/api/weather エンドポイントのテスト (都市: {city})")
    try:
        response = requests.get(f"{BASE_URL}/api/weather", params={"city": city})
        print(f"ステータスコード: {response.status_code}")
        data = response.json()

        if data.get('success'):
            print("✅ 天気データ取得成功")
            print(f"都市: {data['city']}")
            print(f"気温: {data['data']['temperature']}°C")
            print(f"天気: {data['data']['weather_description']}")
            print(f"湿度: {data['data']['humidity']}%")
            print(f"風速: {data['data']['wind_speed']} m/s")
        else:
            print(f"❌ 失敗: {data.get('error', '不明なエラー')}")

        return data.get('success', False)
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def test_air_quality(city="Tokyo"):
    """空気質APIのテスト"""
    print_section(f"/api/air-quality エンドポイントのテスト (都市: {city})")
    try:
        response = requests.get(f"{BASE_URL}/api/air-quality", params={"city": city})
        print(f"ステータスコード: {response.status_code}")
        data = response.json()

        if data.get('success'):
            print("✅ 空気質データ取得成功")
            print(f"都市: {data['city']}")
            print(f"AQI: {data['data']['aqi']}")
            print(f"PM2.5: {data['data'].get('pm25', 'N/A')}")
            print(f"PM10: {data['data'].get('pm10', 'N/A')}")
        else:
            print(f"❌ 失敗: {data.get('error', '不明なエラー')}")

        return data.get('success', False)
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def test_walk_suitability(city="Tokyo"):
    """散歩適性APIのテスト"""
    print_section(f"/api/walk-suitability エンドポイントのテスト (都市: {city})")
    try:
        response = requests.get(f"{BASE_URL}/api/walk-suitability", params={"city": city})
        print(f"ステータスコード: {response.status_code}")
        data = response.json()

        if data.get('success'):
            print("✅ 散歩適性データ取得成功")
            print(f"\n都市: {data['city']}")
            print(f"\n📊 散歩適性指数:")
            print(f"  総合スコア: {data['suitability']['score']} 点")
            print(f"  レベル: {data['suitability']['level']}")
            print(f"  提案: {data['suitability']['recommendation']}")

            print(f"\n🌤️  天気情報:")
            print(f"  気温: {data['weather']['temperature']}°C")
            print(f"  天気: {data['weather']['weather_description']}")

            print(f"\n💨 空気質:")
            print(f"  AQI: {data['air_quality']['aqi']}")

            print(f"\n📋 スコア詳細:")
            for key, value in data['suitability']['details'].items():
                print(f"  {key}: {value}")

            print(f"\n💡 評価ポイント:")
            for reason in data['suitability']['reasons']:
                print(f"  • {reason}")
        else:
            print(f"❌ 失敗: {data.get('error', '不明なエラー')}")

        return data.get('success', False)
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def main():
    """メインテスト関数"""
    print("\n" + "🚀 Walk Suitability API テスト".center(60))
    print("=" * 60)

    # サービスが実行中かチェック
    print("\nサービス状態を確認中...")
    try:
        requests.get(f"{BASE_URL}/health", timeout=2)
        print("✅ サービスは実行中です")
    except:
        print("❌ サービスに接続できません")
        print(f"\nバックエンドサービスが起動していることを確認してください:")
        print("  cd backend")
        print("  python app.py")
        sys.exit(1)

    # テストを実行
    results = []

    results.append(("Health Check", test_health()))
    results.append(("Root Endpoint", test_root()))
    results.append(("Weather API", test_weather("Tokyo")))
    results.append(("Air Quality API", test_air_quality("Tokyo")))
    results.append(("Walk Suitability API", test_walk_suitability("Tokyo")))

    # 他の都市をテスト
    print_section("他の都市のテスト")
    for city in ["Beijing", "London", "Paris"]:
        print(f"\n🌍 テスト都市: {city}")
        result = test_walk_suitability(city)
        results.append((f"Walk Suitability - {city}", result))

    # 結果を集計
    print_section("テスト結果サマリー")
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ 合格" if result else "❌ 不合格"
        print(f"{status} - {name}")

    print(f"\n合計: {passed}/{total} テスト合格")

    if passed == total:
        print("\n🎉 すべてのテストが合格しました！")
    else:
        print("\n⚠️  一部のテストが失敗しました、設定を確認してください")
        print("\n考えられる原因:")
        print("1. APIキーが未設定または無効")
        print("2. ネットワーク接続の問題")
        print("3. 都市名が正しくない")

if __name__ == "__main__":
    main()
