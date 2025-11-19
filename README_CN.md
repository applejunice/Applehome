# 散步适合度指数 API

## 🎯 项目简介

这是一个智能的Web服务，通过整合**OpenWeatherMap**天气API和**World Air Quality Index**空气质量API，为用户提供科学的散步建议。

### 核心功能

输入城市名称 → 获取天气数据 + 空气质量数据 → 融合计算 → 输出散步适合度指数（0-100分）

## 📊 数据融合算法

| 评分因素 | 权重 | 说明 |
|---------|------|------|
| 温度 | 25% | 最佳范围: 15-25°C |
| 天气状况 | 25% | 晴天最佳，雨雪降分 |
| 空气质量 | 30% | 根据AQI指数评估 |
| 湿度 | 10% | 最佳范围: 40-70% |
| 风速 | 10% | 最佳范围: <5m/s |

**最终得分 = 加权平均**

## 🚀 3分钟快速开始

### 1️⃣ 获取免费API密钥

**OpenWeatherMap:**
- 访问: https://openweathermap.org/api
- 注册并获取API Key

**World Air Quality Index:**
- 访问: https://aqicn.org/api/
- 填表获取Token（立即发送到邮箱）

### 2️⃣ 配置API密钥

编辑 `backend/app.py` 第12-13行：

```python
OPENWEATHER_API_KEY = '你的OpenWeatherMap密钥'
WAQI_API_KEY = '你的WAQI密钥'
```

### 3️⃣ 安装并运行

```bash
# 安装依赖
cd backend
pip install -r requirements.txt

# 启动服务
python app.py
```

### 4️⃣ 访问界面

- **前端界面**: 用浏览器打开 `frontend/index.html`
- **API文档**: 用浏览器打开 `documentation/api-docs.html`

## 📱 使用示例

### 网页界面
1. 打开 `frontend/index.html`
2. 输入城市名称（如：Tokyo, Beijing, London）
3. 点击"查询"按钮
4. 查看散步适合度指数和详细数据

### API调用
```bash
curl "http://localhost:5000/api/walk-suitability?city=Tokyo"
```

**响应示例:**
```json
{
  "success": true,
  "city": "Tokyo",
  "suitability": {
    "score": 85.5,
    "level": "非常适合",
    "recommendation": "现在是散步的绝佳时机！"
  }
}
```

## 📁 项目结构

```
.
├── backend/              # 后端服务
│   ├── app.py           # Flask应用
│   ├── requirements.txt # 依赖列表
│   └── test_api.py      # 测试脚本
│
├── documentation/        # API文档
│   ├── api-docs.yml     # OpenAPI规范
│   └── api-docs.html    # 交互式文档
│
├── frontend/            # 前端界面
│   └── index.html       # Web界面
│
├── report/              # 报告文件夹
│
└── README_PROJECT.md    # 详细说明
```

## 🎓 作业要求对照

✅ **调用2个以上公共API**
- OpenWeatherMap API (天气)
- World Air Quality Index API (空气质量)

✅ **数据融合**
- 加权算法融合5个维度数据
- 生成独特的散步适合度指数

✅ **OpenAPI文档 (YAML)**
- `documentation/api-docs.yml`

✅ **交互式API文档**
- `documentation/api-docs.html`
- 基于Swagger UI

✅ **Web前端**
- `frontend/index.html`
- 美观且响应式设计

## 🛠️ 技术栈

- **后端**: Python + Flask + Flask-CORS
- **前端**: HTML + CSS + JavaScript
- **API文档**: OpenAPI 3.0 + Swagger UI
- **第三方API**: OpenWeatherMap + WAQI

## 📖 文档说明

- `README_PROJECT.md` - 完整的项目文档（英文）
- `SETUP_GUIDE.md` - 详细的设置指南
- `CHECKLIST.md` - 提交前检查列表
- `README_CN.md` - 本文件（中文简介）

## 🧪 测试

```bash
# 运行自动化测试
cd backend
python test_api.py
```

## 💡 使用提示

1. **城市名称**: 使用英文（Tokyo, Beijing, London等）
2. **API限制**: 免费API有调用次数限制，请勿频繁请求
3. **网络要求**: 需要能访问国际API服务

## 🌍 支持的城市（示例）

- 日本: Tokyo, Osaka
- 中国: Beijing, Shanghai, Guangzhou
- 韩国: Seoul, Busan
- 欧洲: London, Paris, Berlin, Rome
- 美洲: New York, Los Angeles, Toronto

## 📝 报告截图建议

1. 前端界面显示高分（非常适合）
2. 前端界面显示低分（不适合）
3. API文档页面
4. API响应数据
5. 不同城市的对比

## ⚠️ 注意事项

- ❌ 不要提交包含真实API密钥的文件
- ✅ 使用 `.env.example` 作为模板
- ✅ 在报告中说明如何获取API密钥
- ✅ 测试所有功能正常工作后再提交

## 🎉 完成检查

提交前请确认：
- [ ] 代码可以正常运行
- [ ] API密钥已配置（测试用）
- [ ] 所有端点都能正常响应
- [ ] 前端界面显示正常
- [ ] API文档可以打开
- [ ] 报告已完成并包含截图
- [ ] ZIP文件包含所有必要文件

---

祝你顺利完成作业！🎓✨
