#!/usr/bin/env python3
"""
API测试脚本
用于测试Walk Suitability API的各个端点
"""

import requests
import json
import sys

BASE_URL = "http://localhost:5000"

def print_section(title):
    """打印分隔线"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def test_health():
    """测试健康检查端点"""
    print_section("测试 /health 端点")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def test_root():
    """测试根路径"""
    print_section("测试 / 端点")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def test_weather(city="Tokyo"):
    """测试天气API"""
    print_section(f"测试 /api/weather 端点 (城市: {city})")
    try:
        response = requests.get(f"{BASE_URL}/api/weather", params={"city": city})
        print(f"状态码: {response.status_code}")
        data = response.json()

        if data.get('success'):
            print("✅ 成功获取天气数据")
            print(f"城市: {data['city']}")
            print(f"温度: {data['data']['temperature']}°C")
            print(f"天气: {data['data']['weather_description']}")
            print(f"湿度: {data['data']['humidity']}%")
            print(f"风速: {data['data']['wind_speed']} m/s")
        else:
            print(f"❌ 失败: {data.get('error', '未知错误')}")

        return data.get('success', False)
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def test_air_quality(city="Tokyo"):
    """测试空气质量API"""
    print_section(f"测试 /api/air-quality 端点 (城市: {city})")
    try:
        response = requests.get(f"{BASE_URL}/api/air-quality", params={"city": city})
        print(f"状态码: {response.status_code}")
        data = response.json()

        if data.get('success'):
            print("✅ 成功获取空气质量数据")
            print(f"城市: {data['city']}")
            print(f"AQI: {data['data']['aqi']}")
            print(f"PM2.5: {data['data'].get('pm25', 'N/A')}")
            print(f"PM10: {data['data'].get('pm10', 'N/A')}")
        else:
            print(f"❌ 失败: {data.get('error', '未知错误')}")

        return data.get('success', False)
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def test_walk_suitability(city="Tokyo"):
    """测试散步适合度API"""
    print_section(f"测试 /api/walk-suitability 端点 (城市: {city})")
    try:
        response = requests.get(f"{BASE_URL}/api/walk-suitability", params={"city": city})
        print(f"状态码: {response.status_code}")
        data = response.json()

        if data.get('success'):
            print("✅ 成功获取散步适合度数据")
            print(f"\n城市: {data['city']}")
            print(f"\n📊 散步适合度指数:")
            print(f"  总分: {data['suitability']['score']} 分")
            print(f"  等级: {data['suitability']['level']}")
            print(f"  建议: {data['suitability']['recommendation']}")

            print(f"\n🌤️  天气信息:")
            print(f"  温度: {data['weather']['temperature']}°C")
            print(f"  天气: {data['weather']['weather_description']}")

            print(f"\n💨 空气质量:")
            print(f"  AQI: {data['air_quality']['aqi']}")

            print(f"\n📋 评分详情:")
            for key, value in data['suitability']['details'].items():
                print(f"  {key}: {value}")

            print(f"\n💡 评估要点:")
            for reason in data['suitability']['reasons']:
                print(f"  • {reason}")
        else:
            print(f"❌ 失败: {data.get('error', '未知错误')}")

        return data.get('success', False)
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def main():
    """主测试函数"""
    print("\n" + "🚀 Walk Suitability API 测试".center(60))
    print("=" * 60)

    # 检查服务是否运行
    print("\n正在检查服务状态...")
    try:
        requests.get(f"{BASE_URL}/health", timeout=2)
        print("✅ 服务正在运行")
    except:
        print("❌ 无法连接到服务")
        print(f"\n请确保后端服务已启动:")
        print("  cd backend")
        print("  python app.py")
        sys.exit(1)

    # 运行测试
    results = []

    results.append(("Health Check", test_health()))
    results.append(("Root Endpoint", test_root()))
    results.append(("Weather API", test_weather("Tokyo")))
    results.append(("Air Quality API", test_air_quality("Tokyo")))
    results.append(("Walk Suitability API", test_walk_suitability("Tokyo")))

    # 测试其他城市
    print_section("测试其他城市")
    for city in ["Beijing", "London", "Paris"]:
        print(f"\n🌍 测试城市: {city}")
        result = test_walk_suitability(city)
        results.append((f"Walk Suitability - {city}", result))

    # 汇总结果
    print_section("测试结果汇总")
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")

    print(f"\n总计: {passed}/{total} 测试通过")

    if passed == total:
        print("\n🎉 所有测试通过！")
    else:
        print("\n⚠️  部分测试失败，请检查配置")
        print("\n可能的原因:")
        print("1. API密钥未配置或无效")
        print("2. 网络连接问题")
        print("3. 城市名称不正确")

if __name__ == "__main__":
    main()
