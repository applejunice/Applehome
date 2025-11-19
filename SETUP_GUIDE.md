# 🚀 快速设置指南

## 第一步：获取API密钥

### 1. OpenWeatherMap API密钥

1. 访问 https://openweathermap.org/api
2. 点击 "Sign Up" 注册免费账号
3. 登录后，进入 "API keys" 标签页
4. 复制您的API密钥（或创建新的）

### 2. World Air Quality Index API密钥

1. 访问 https://aqicn.org/api/
2. 填写申请表单（姓名和邮箱）
3. 立即会通过邮件收到您的API Token

## 第二步：配置项目

### 方法A：使用环境变量（推荐）

```bash
# 1. 进入backend目录
cd backend

# 2. 复制环境变量模板
cp .env.example .env

# 3. 编辑.env文件，填入您的API密钥
# 使用任何文本编辑器打开.env文件
# 替换 your_openweather_api_key_here 为您的OpenWeatherMap密钥
# 替换 your_waqi_api_key_here 为您的WAQI密钥
```

### 方法B：直接修改代码

打开 `backend/app.py`，找到第12-13行：

```python
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'your_openweather_api_key_here')
WAQI_API_KEY = os.getenv('WAQI_API_KEY', 'your_waqi_api_key_here')
```

替换为：

```python
OPENWEATHER_API_KEY = '您的OpenWeatherMap密钥'
WAQI_API_KEY = '您的WAQI密钥'
```

## 第三步：安装依赖

```bash
# 确保您在backend目录下
cd backend

# 安装Python依赖
pip install -r requirements.txt

# 或使用pip3
pip3 install -r requirements.txt
```

## 第四步：启动服务

```bash
# 启动后端服务
python app.py

# 或使用python3
python3 app.py
```

您应该看到类似输出：
```
 * Running on http://0.0.0.0:5000
 * Running on http://127.0.0.1:5000
```

## 第五步：测试API

### 使用浏览器测试

在浏览器中访问：
```
http://localhost:5000/api/walk-suitability?city=Tokyo
```

### 使用curl测试

```bash
curl "http://localhost:5000/api/walk-suitability?city=Tokyo"
```

### 使用前端界面

1. 保持后端服务运行
2. 在浏览器中打开 `frontend/index.html`
3. 输入城市名称并点击"查询"

### 查看API文档

在浏览器中打开 `documentation/api-docs.html` 查看完整的交互式API文档。

## 常见问题

### Q: 出现 "ModuleNotFoundError: No module named 'flask'"

**A:** 需要安装依赖：
```bash
pip install -r requirements.txt
```

### Q: API返回错误 "天气数据获取失败"

**A:** 检查以下几点：
1. 确认API密钥是否正确配置
2. 确认网络连接正常
3. 确认城市名称使用英文（如 Tokyo, Beijing）

### Q: 前端无法连接后端

**A:** 确保：
1. 后端服务正在运行（http://localhost:5000）
2. 浏览器允许CORS跨域请求
3. 检查浏览器控制台是否有错误信息

### Q: 如何更换查询城市？

**A:**
- 在前端界面直接输入城市名称（英文）
- 或在API请求中修改city参数
- 支持的城市示例：Tokyo, Beijing, Shanghai, London, Paris, New York, Seoul

## 支持的城市列表（部分）

### 亚洲
- Tokyo, Osaka (日本)
- Beijing, Shanghai, Guangzhou, Shenzhen (中国)
- Seoul, Busan (韩国)
- Singapore (新加坡)
- Bangkok (泰国)
- Hanoi, Ho Chi Minh City (越南)

### 欧洲
- London (英国)
- Paris (法国)
- Berlin (德国)
- Rome (意大利)
- Madrid (西班牙)

### 美洲
- New York, Los Angeles, Chicago (美国)
- Toronto (加拿大)

### 大洋洲
- Sydney, Melbourne (澳大利亚)

## 下一步

- 查看 `README_PROJECT.md` 了解项目详细信息
- 查看 `documentation/api-docs.html` 了解完整API文档
- 尝试不同城市的查询
- 根据需要自定义评分算法
