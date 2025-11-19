# Walk Suitability API - 散步适合度指数服务

## 📖 项目概述

本项目是一个创新的Web服务，通过整合**两个开源的第三方API**，为用户提供科学、全面的散步建议。系统会根据实时天气和空气质量数据，计算出独特的"散步适合度指数"(0-100分)。

## 🌟 项目特点

### 使用的开源第三方API

1. **OpenWeatherMap API** (https://openweathermap.org/api)
   - 提供实时天气数据
   - 包括温度、湿度、风速、天气状况等信息
   - 免费API，每分钟60次调用限制

2. **World Air Quality Index API** (https://aqicn.org/api/)
   - 提供全球城市的空气质量指数(AQI)
   - 包括PM2.5、PM10、O3、NO2等污染物数据
   - 免费API，每分钟1000次调用限制

### 数据融合方法

本服务通过创新的加权算法融合两个API的数据：

- **温度权重: 25%** - 评估温度是否适合户外活动（最佳范围15-25°C）
- **天气状况权重: 25%** - 判断天气类型（晴天、雨天、雪天等）
- **空气质量权重: 30%** - 根据AQI指数评估空气污染程度
- **湿度权重: 10%** - 考虑人体舒适度（最佳范围40-70%）
- **风速权重: 10%** - 评估风力影响（最佳范围<5m/s）

最终输出一个综合的散步适合度指数，并给出具体建议。

## 📁 项目结构

```
.
├── backend/
│   ├── app.py              # Flask后端应用
│   ├── requirements.txt    # Python依赖
│   └── .env.example        # 环境变量示例
├── documentation/
│   ├── api-docs.html       # 交互式API文档
│   └── api-docs.yml        # OpenAPI规范
├── frontend/
│   └── index.html          # Web前端界面
└── README_PROJECT.md       # 项目说明文档
```

## 🚀 快速开始

### 前置要求

- Python 3.8+
- pip (Python包管理器)

### 1. 获取API密钥

#### OpenWeatherMap API
1. 访问 https://openweathermap.org/api
2. 注册免费账号
3. 在"API keys"页面获取您的API密钥

#### World Air Quality Index API
1. 访问 https://aqicn.org/api/
2. 填写申请表单获取免费API Token
3. 通常会立即通过邮件收到Token

### 2. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑.env文件，填入您的API密钥
# OPENWEATHER_API_KEY=你的OpenWeatherMap密钥
# WAQI_API_KEY=你的WAQI密钥
```

或者直接在app.py中修改API密钥（不推荐用于生产环境）：

```python
OPENWEATHER_API_KEY = 'your_actual_api_key_here'
WAQI_API_KEY = 'your_actual_token_here'
```

### 4. 启动后端服务

```bash
cd backend
python app.py
```

服务将在 http://localhost:5000 启动

### 5. 访问前端界面

在浏览器中打开：
```
frontend/index.html
```

或者使用简单的HTTP服务器：
```bash
cd frontend
python -m http.server 8080
# 然后访问 http://localhost:8080
```

### 6. 查看API文档

在浏览器中打开：
```
documentation/api-docs.html
```

## 📡 API端点

### 1. 获取散步适合度指数
```
GET /api/walk-suitability?city={city_name}
```

**示例:**
```bash
curl "http://localhost:5000/api/walk-suitability?city=Tokyo"
```

**响应:**
```json
{
  "success": true,
  "city": "Tokyo",
  "timestamp": "2025-11-19T10:30:00",
  "suitability": {
    "score": 85.5,
    "level": "非常适合",
    "recommendation": "现在是散步的绝佳时机！",
    "reasons": ["天气和空气质量都很好"],
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

### 2. 获取天气数据
```
GET /api/weather?city={city_name}
```

### 3. 获取空气质量数据
```
GET /api/air-quality?city={city_name}
```

### 4. 健康检查
```
GET /health
```

## 📊 评分标准

| 分数范围 | 等级 | 建议 |
|---------|------|------|
| 80-100  | 非常适合 | 现在是散步的绝佳时机！ |
| 60-79   | 适合 | 适合散步，请注意某些情况 |
| 40-59   | 一般 | 可以散步，但条件不是很理想 |
| 0-39    | 不适合 | 建议推迟散步计划 |

## 🎨 功能特性

- ✅ 整合两个真实的开源API
- ✅ 智能的数据融合算法
- ✅ 完整的OpenAPI文档
- ✅ 交互式API文档页面（Swagger UI）
- ✅ 美观的Web前端界面
- ✅ 实时数据查询
- ✅ 多城市支持
- ✅ 详细的评分解释
- ✅ CORS支持

## 🛠️ 技术栈

### 后端
- **Flask** - Python Web框架
- **Flask-CORS** - 跨域资源共享支持
- **Requests** - HTTP客户端库

### 前端
- **原生HTML/CSS/JavaScript** - 无需额外框架
- **Swagger UI** - API文档展示

### API文档
- **OpenAPI 3.0.3** - API规范标准

## 🔧 开发说明

### 添加新的评分因素

在`app.py`的`calculate_walk_suitability`函数中添加新的评分逻辑：

```python
def calculate_walk_suitability(weather_data, air_quality_data):
    # 添加新的评分因素
    new_factor_score = calculate_new_factor(weather_data)

    # 更新权重
    weights = {
        'temp': 0.20,
        'weather': 0.20,
        'humidity': 0.10,
        'wind': 0.10,
        'aqi': 0.30,
        'new_factor': 0.10  # 新增
    }

    # 更新最终评分计算
    final_score = (
        temp_score * weights['temp'] +
        # ... 其他因素
        new_factor_score * weights['new_factor']
    )
```

### 支持更多城市

API支持所有OpenWeatherMap和WAQI支持的城市。只需在查询参数中传入城市名称（英文）即可。

### 自定义评分标准

修改`calculate_walk_suitability`函数中的评分逻辑来自定义评分标准。

## 📝 注意事项

1. **API限制**: 免费API有调用次数限制，请勿频繁请求
2. **城市名称**: 使用英文城市名称查询（如Tokyo, Beijing, London）
3. **数据准确性**: 数据来自第三方API，准确性取决于数据源
4. **CORS**: 已配置CORS支持，可从任何域名访问API

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 👤 作者

[您的姓名/学号]

## 🙏 致谢

- OpenWeatherMap - 提供天气数据API
- World Air Quality Index - 提供空气质量数据API
- Flask - 优秀的Python Web框架
