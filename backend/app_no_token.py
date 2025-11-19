from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

def get_weather_data(city):
    """
    获取天气数据 (Open-Meteo API - 完全免费，无需token)
    使用geocoding获取坐标，然后获取天气
    """
    try:
        # 1. 先通过城市名获取坐标
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=zh&format=json"
        geo_response = requests.get(geocode_url, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get('results'):
            raise Exception(f"找不到城市: {city}")

        location = geo_data['results'][0]
        lat = location['latitude']
        lon = location['longitude']

        # 2. 使用坐标获取天气数据
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,cloud_cover,wind_speed_10m&timezone=auto"
        weather_response = requests.get(weather_url, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data['current']

        # 天气代码映射
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
        raise Exception(f"天气数据获取失败: {str(e)}")

def get_air_quality_data(city):
    """
    获取空气质量数据 (Open-Meteo Air Quality API - 完全免费，无需token)
    """
    try:
        # 1. 先通过城市名获取坐标
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=zh&format=json"
        geo_response = requests.get(geocode_url, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get('results'):
            raise Exception(f"找不到城市: {city}")

        location = geo_data['results'][0]
        lat = location['latitude']
        lon = location['longitude']

        # 2. 使用坐标获取空气质量数据
        air_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone,us_aqi,european_aqi&timezone=auto"
        air_response = requests.get(air_url, timeout=10)
        air_response.raise_for_status()
        air_data = air_response.json()

        current = air_data['current']

        # 使用美国AQI标准
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
        raise Exception(f"空气质量数据获取失败: {str(e)}")

def calculate_walk_suitability(weather_data, air_quality_data):
    """
    计算散步适合度指数 (0-100)
    综合考虑温度、天气状况、湿度、风速、空气质量
    """
    score = 100
    reasons = []

    # 1. 温度评分 (最佳温度: 15-25°C)
    temp = weather_data['temperature']
    if 15 <= temp <= 25:
        temp_score = 100
    elif 10 <= temp < 15 or 25 < temp <= 30:
        temp_score = 80
        reasons.append(f"温度{temp}°C略微不太理想")
    elif 5 <= temp < 10 or 30 < temp <= 35:
        temp_score = 60
        reasons.append(f"温度{temp}°C较为极端")
    else:
        temp_score = 30
        reasons.append(f"温度{temp}°C非常不适合")

    # 2. 天气状况评分
    weather_main = weather_data['weather']
    if weather_main in ['Clear', 'Clouds']:
        weather_score = 100
    elif weather_main in ['Mist', 'Haze', 'Fog']:
        weather_score = 70
        reasons.append("天气有雾霾")
    elif weather_main in ['Drizzle', 'Rain']:
        weather_score = 40
        reasons.append("正在下雨")
    elif weather_main in ['Thunderstorm', 'Snow']:
        weather_score = 20
        reasons.append(f"恶劣天气: {weather_main}")
    else:
        weather_score = 60

    # 3. 湿度评分 (最佳湿度: 40-70%)
    humidity = weather_data['humidity']
    if 40 <= humidity <= 70:
        humidity_score = 100
    elif 30 <= humidity < 40 or 70 < humidity <= 80:
        humidity_score = 80
    else:
        humidity_score = 60
        if humidity > 80:
            reasons.append(f"湿度{humidity}%过高")
        else:
            reasons.append(f"湿度{humidity}%过低")

    # 4. 风速评分 (最佳风速: < 5 m/s)
    wind_speed = weather_data['wind_speed']
    if wind_speed < 5:
        wind_score = 100
    elif 5 <= wind_speed < 10:
        wind_score = 70
        reasons.append(f"风速{wind_speed}m/s较大")
    else:
        wind_score = 40
        reasons.append(f"风速{wind_speed}m/s很大")

    # 5. 空气质量评分
    aqi = air_quality_data['aqi']
    if aqi <= 50:
        aqi_score = 100
        aqi_level = "优秀"
    elif aqi <= 100:
        aqi_score = 80
        aqi_level = "良好"
    elif aqi <= 150:
        aqi_score = 60
        aqi_level = "中等"
        reasons.append(f"空气质量{aqi_level} (AQI: {aqi})")
    elif aqi <= 200:
        aqi_score = 40
        aqi_level = "较差"
        reasons.append(f"空气质量{aqi_level} (AQI: {aqi})")
    elif aqi <= 300:
        aqi_score = 20
        aqi_level = "差"
        reasons.append(f"空气质量{aqi_level} (AQI: {aqi})")
    else:
        aqi_score = 10
        aqi_level = "严重污染"
        reasons.append(f"空气质量{aqi_level} (AQI: {aqi})")

    # 综合评分 (加权平均)
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

    # 确定适合度等级
    if final_score >= 80:
        level = "非常适合"
        recommendation = "现在是散步的绝佳时机！"
    elif final_score >= 60:
        level = "适合"
        recommendation = "适合散步，请注意以下情况。"
    elif final_score >= 40:
        level = "一般"
        recommendation = "可以散步，但条件不是很理想。"
    else:
        level = "不适合"
        recommendation = "建议推迟散步计划。"

    return {
        'score': round(final_score, 1),
        'level': level,
        'recommendation': recommendation,
        'reasons': reasons if reasons else ["天气和空气质量都很好"],
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
    API根路径
    """
    return jsonify({
        'service': 'Walk Suitability API (No Token Required)',
        'version': '2.0.0',
        'description': '散步适合度指数服务 - 使用完全免费的开放API，无需注册token',
        'apis_used': {
            'weather': 'Open-Meteo Weather API (https://open-meteo.com)',
            'air_quality': 'Open-Meteo Air Quality API (https://open-meteo.com)'
        },
        'endpoints': {
            '/api/walk-suitability': 'GET - 获取城市的散步适合度指数',
            '/api/weather': 'GET - 获取天气数据',
            '/api/air-quality': 'GET - 获取空气质量数据',
            '/health': 'GET - 健康检查'
        }
    })

@app.route('/health')
def health():
    """
    健康检查端点
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/weather')
def get_weather():
    """
    获取指定城市的天气数据
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
    获取指定城市的空气质量数据
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
    获取指定城市的散步适合度指数
    整合天气和空气质量数据，计算综合评分
    """
    city = request.args.get('city', 'Tokyo')

    try:
        # 获取天气和空气质量数据
        weather_data = get_weather_data(city)
        air_quality_data = get_air_quality_data(city)

        # 计算散步适合度
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
    print("🎉 Walk Suitability API - No Token Required!")
    print("=" * 60)
    print("✅ 使用完全免费的Open-Meteo API")
    print("✅ 无需注册，无需API密钥")
    print("✅ 立即可用")
    print("=" * 60)
    print("📡 服务启动在: http://localhost:5000")
    print("🌐 前端界面: 打开 frontend/index.html")
    print("📚 API文档: 打开 documentation/api-docs.html")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
