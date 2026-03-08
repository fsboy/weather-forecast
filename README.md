# Weather Forecast Skill for CoPaw

基于高德地图Web服务API的天气预报技能，专为CoPaw设计。

## 快速开始

### 安装

```bash
# 复制技能到CoPaw目录
cp -r weather-forecast ~/.copaw/skills/
```

### 配置API密钥

**方式一：copaw init（推荐）**

```bash
copaw init
# 在 "Configure environment variables?" 选择 Yes
# 添加: AMAP_API_KEY = your_api_key
```

**方式二：Console配置**

1. `copaw app`
2. 打开 http://127.0.0.1:8088/
3. Settings → Environment Variables
4. 添加 `AMAP_API_KEY`

**方式三：环境变量**

```bash
export AMAP_API_KEY="your_api_key"
```

**方式四：config.json**

编辑 `~/.copaw/config.json`：

```json
{
  "env": {
    "AMAP_API_KEY": "your_api_key"
  }
}
```

### 启动

```bash
copaw app
```

## 使用示例

```
用户：北京今天天气怎么样？
用户：沈阳浑南区明天天气如何？
用户：查询上海市实时天气
```

## 文件结构

```
weather-forecast/
├── SKILL.md          # 技能描述
├── weather_tools.py  # Python工具实现
└── README.md         # 使用说明
```

## 支持的城市

| 城市 | 编码 | 城市 | 编码 |
|------|------|------|------|
| 北京 | 110000 | 上海 | 310000 |
| 广州 | 440100 | 深圳 | 440300 |
| 沈阳浑南区 | 210112 | 杭州 | 330100 |

## 工具列表

| 工具 | 说明 |
|------|------|
| get_realtime_weather | 获取实时天气 |
| get_forecast_weather | 获取天气预报 |
| get_today_weather | 获取今日天气 |

## 获取API密钥

1. 访问 [高德开放平台](https://console.amap.com/)
2. 创建应用 → 选择"Web服务"
3. 获取Key

## 依赖

```bash
pip install aiohttp
```

## 许可证

Apache License 2.0
