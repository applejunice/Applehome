from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# API配置
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'your_openweather_api_key_here')
WAQI_API_KEY = os.getenv('WAQI_API_KEY', 'your_waqi_api_key_here')

def get_weather_data(city):
    """
    获取天气数据 (OpenWeatherMap API)
    """
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'weather': data['weather'][0]['main'],
            'weather_description': data['weather'][0]['description'],
            'wind_speed': data['wind']['speed'],
            'clouds': data['clouds']['all']
        }
    except Exception as e:
        raise Exception(f"天气数据获取失败: {str(e)}")

def get_air_quality_data(city):
    """
    获取空气质量数据 (World Air Quality Index API)
    """
    try:
        url = f"http://api.waqi.info/feed/{city}/?token={WAQI_API_KEY}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data['status'] != 'ok':
            raise Exception("空气质量数据返回状态异常")

        aqi = data['data']['aqi']
        iaqi = data['data'].get('iaqi', {})

        return {
            'aqi': aqi,
            'pm25': iaqi.get('pm25', {}).get('v', None),
            'pm10': iaqi.get('pm10', {}).get('v', None),
            'o3': iaqi.get('o3', {}).get('v', None),
            'no2': iaqi.get('no2', {}).get('v', None)
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
        'service': 'Walk Suitability API',
        'version': '1.0.0',
        'description': '散步适合度指数服务 - 整合天气和空气质量数据',
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
    app.run(debug=True, host='0.0.0.0', port=5000)
