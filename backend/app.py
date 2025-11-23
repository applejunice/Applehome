from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

def get_weather_data(city):
    """
    天気データ取得 (Open-Meteo API - 完全無料、トークン不要)
    ジオコーディングで座標を取得し、天気データを取得
    """
    try:
        # 1. まず都市名から座標を取得
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=zh&format=json"
        geo_response = requests.get(geocode_url, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get('results'):
            raise Exception(f"都市が見つかりません: {city}")

        location = geo_data['results'][0]
        lat = location['latitude']
        lon = location['longitude']

        # 2. 座標を使用して天気データを取得
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,cloud_cover,wind_speed_10m&timezone=auto"
        weather_response = requests.get(weather_url, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data['current']

        # 天気コードマッピング
        weather_code_map = {
            0: ('Clear', 'clear sky'),
            1: ('Clouds', 'mainly clear'),
            2: ('Clouds', 'partly cloudy'),
            3: ('Clouds', 'overcast'),
            45: ('Fog', 'foggy'),
            48: ('Fog', 'depositing rime fog'),
            51: ('Drizzle', 'light drizzle'),
            53: ('Drizzle', 'moderate drizzle'),
            55: ('Drizzle', 'dense drizzle'),
            61: ('Rain', 'slight rain'),
            63: ('Rain', 'moderate rain'),
            65: ('Rain', 'heavy rain'),
            71: ('Snow', 'slight snow'),
            73: ('Snow', 'moderate snow'),
            75: ('Snow', 'heavy snow'),
            80: ('Rain', 'slight rain showers'),
            81: ('Rain', 'moderate rain showers'),
            82: ('Rain', 'violent rain showers'),
            95: ('Thunderstorm', 'thunderstorm'),
            96: ('Thunderstorm', 'thunderstorm with slight hail'),
            99: ('Thunderstorm', 'thunderstorm with heavy hail'),
        }

        weather_code = current.get('weather_code', 0)
        weather_main, weather_desc = weather_code_map.get(weather_code, ('Clear', 'unknown'))

        return {
            'temperature': current['temperature_2m'],
            'feels_like': current['apparent_temperature'],
            'humidity': current['relative_humidity_2m'],
            'weather': weather_main,
            'weather_description': weather_desc,
            'wind_speed': current['wind_speed_10m'],
            'clouds': current['cloud_cover'],
            'city_name': location['name'],
            'country': location.get('country', '')
        }
    except Exception as e:
        raise Exception(f"天気データ取得失敗: {str(e)}")

def get_air_quality_data(city):
    """
    空気質データ取得 (Open-Meteo Air Quality API - 完全無料、トークン不要)
    """
    try:
        # 1. まず都市名から座標を取得
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=zh&format=json"
        geo_response = requests.get(geocode_url, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get('results'):
            raise Exception(f"都市が見つかりません: {city}")

        location = geo_data['results'][0]
        lat = location['latitude']
        lon = location['longitude']

        # 2. 座標を使用して空気質データを取得
        air_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone,us_aqi,european_aqi&timezone=auto"
        air_response = requests.get(air_url, timeout=10)
        air_response.raise_for_status()
        air_data = air_response.json()

        current = air_data['current']

        # 米国AQI基準を使用
        aqi = current.get('us_aqi', current.get('european_aqi', 50))

        return {
            'aqi': int(aqi) if aqi else 50,
            'pm25': current.get('pm2_5'),
            'pm10': current.get('pm10'),
            'o3': current.get('ozone'),
            'no2': current.get('nitrogen_dioxide'),
            'co': current.get('carbon_monoxide')
        }
    except Exception as e:
        raise Exception(f"空気質データ取得失敗: {str(e)}")

def calculate_walk_suitability(weather_data, air_quality_data):
    """
    散歩適性指数を計算 (0-100)
    気温、天気状況、湿度、風速、空気質を総合的に考慮
    """
    score = 100
    reasons = []

    # 1. 気温評価 (最適気温: 15-25°C)
    temp = weather_data['temperature']
    if 15 <= temp <= 25:
        temp_score = 100
    elif 10 <= temp < 15 or 25 < temp <= 30:
        temp_score = 80
        reasons.append(f"気温{temp}°Cはやや理想的ではありません")
    elif 5 <= temp < 10 or 30 < temp <= 35:
        temp_score = 60
        reasons.append(f"気温{temp}°Cはかなり極端です")
    else:
        temp_score = 30
        reasons.append(f"気温{temp}°Cは非常に不適です")

    # 2. 天気状況評価
    weather_main = weather_data['weather']
    if weather_main in ['Clear', 'Clouds']:
        weather_score = 100
    elif weather_main in ['Mist', 'Haze', 'Fog']:
        weather_score = 70
        reasons.append("天気に霧や靄があります")
    elif weather_main in ['Drizzle', 'Rain']:
        weather_score = 40
        reasons.append("雨が降っています")
    elif weather_main in ['Thunderstorm', 'Snow']:
        weather_score = 20
        reasons.append(f"悪天候: {weather_main}")
    else:
        weather_score = 60

    # 3. 湿度評価 (最適湿度: 40-70%)
    humidity = weather_data['humidity']
    if 40 <= humidity <= 70:
        humidity_score = 100
    elif 30 <= humidity < 40 or 70 < humidity <= 80:
        humidity_score = 80
    else:
        humidity_score = 60
        if humidity > 80:
            reasons.append(f"湿度{humidity}%は高すぎます")
        else:
            reasons.append(f"湿度{humidity}%は低すぎます")

    # 4. 風速評価 (最適風速: < 5 m/s)
    wind_speed = weather_data['wind_speed']
    if wind_speed < 5:
        wind_score = 100
    elif 5 <= wind_speed < 10:
        wind_score = 70
        reasons.append(f"風速{wind_speed}m/sはやや強いです")
    else:
        wind_score = 40
        reasons.append(f"風速{wind_speed}m/sは非常に強いです")

    # 5. 空気質評価
    aqi = air_quality_data['aqi']
    if aqi <= 50:
        aqi_score = 100
        aqi_level = "優秀"
    elif aqi <= 100:
        aqi_score = 80
        aqi_level = "良好"
    elif aqi <= 150:
        aqi_score = 60
        aqi_level = "普通"
        reasons.append(f"空気質{aqi_level} (AQI: {aqi})")
    elif aqi <= 200:
        aqi_score = 40
        aqi_level = "やや悪い"
        reasons.append(f"空気質{aqi_level} (AQI: {aqi})")
    elif aqi <= 300:
        aqi_score = 20
        aqi_level = "悪い"
        reasons.append(f"空気質{aqi_level} (AQI: {aqi})")
    else:
        aqi_score = 10
        aqi_level = "深刻な汚染"
        reasons.append(f"空気質{aqi_level} (AQI: {aqi})")

    # 総合評価 (加重平均)
    weights = {
        'temp': 0.25,
        'weather': 0.25,
        'humidity': 0.1,
        'wind': 0.1,
        'aqi': 0.3
    }

    final_score = (
        temp_score * weights['temp'] +
        weather_score * weights['weather'] +
        humidity_score * weights['humidity'] +
        wind_score * weights['wind'] +
        aqi_score * weights['aqi']
    )

    # 適性レベルを決定
    if final_score >= 80:
        level = "非常に適している"
        recommendation = "今は散歩に最適な時間です！"
    elif final_score >= 60:
        level = "適している"
        recommendation = "散歩に適していますが、以下の状況にご注意ください。"
    elif final_score >= 40:
        level = "普通"
        recommendation = "散歩できますが、条件はあまり理想的ではありません。"
    else:
        level = "不適"
        recommendation = "散歩計画を延期することをお勧めします。"

    return {
        'score': round(final_score, 1),
        'level': level,
        'recommendation': recommendation,
        'reasons': reasons if reasons else ["天気と空気質が両方とも良好です"],
        'details': {
            'temperature_score': round(temp_score, 1),
            'weather_score': round(weather_score, 1),
            'humidity_score': round(humidity_score, 1),
            'wind_score': round(wind_score, 1),
            'aqi_score': round(aqi_score, 1)
        }
    }

@app.route('/')
def index():
    """
    APIルートパス
    """
    return jsonify({
        'service': 'Walk Suitability API (No Token Required)',
        'version': '2.0.0',
        'description': '散歩適性指数サービス - 完全無料のオープンAPIを使用、トークン登録不要',
        'apis_used': {
            'weather': 'Open-Meteo Weather API (https://open-meteo.com)',
            'air_quality': 'Open-Meteo Air Quality API (https://open-meteo.com)'
        },
        'endpoints': {
            '/api/walk-suitability': 'GET - 都市の散歩適性指数を取得',
            '/api/weather': 'GET - 天気データを取得',
            '/api/air-quality': 'GET - 空気質データを取得',
            '/health': 'GET - ヘルスチェック'
        }
    })

@app.route('/health')
def health():
    """
    ヘルスチェックエンドポイント
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/weather')
def get_weather():
    """
    指定都市の天気データを取得
    """
    city = request.args.get('city', 'Tokyo')

    try:
        weather_data = get_weather_data(city)
        return jsonify({
            'success': True,
            'city': city,
            'data': weather_data,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/air-quality')
def get_air_quality():
    """
    指定都市の空気質データを取得
    """
    city = request.args.get('city', 'Tokyo')

    try:
        air_quality_data = get_air_quality_data(city)
        return jsonify({
            'success': True,
            'city': city,
            'data': air_quality_data,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/walk-suitability')
def get_walk_suitability():
    """
    指定都市の散歩適性指数を取得
    天気と空気質データを統合し、総合評価を計算
    """
    city = request.args.get('city', 'Tokyo')

    try:
        # 天気と空気質データを取得
        weather_data = get_weather_data(city)
        air_quality_data = get_air_quality_data(city)

        # 散歩適性を計算
        suitability = calculate_walk_suitability(weather_data, air_quality_data)

        return jsonify({
            'success': True,
            'city': city,
            'timestamp': datetime.now().isoformat(),
            'suitability': suitability,
            'weather': weather_data,
            'air_quality': air_quality_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🎉 Walk Suitability API - トークン不要!")
    print("=" * 60)
    print("✅ 完全無料のOpen-Meteo APIを使用")
    print("✅ 登録不要、APIキー不要")
    print("✅ すぐに使用可能")
    print("=" * 60)
    print("📡 サービス起動: http://localhost:5000")
    print("🌐 フロントエンドインターフェース: frontend/index.html を開く")
    print("📚 APIドキュメント: documentation/api-docs.html を開く")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
