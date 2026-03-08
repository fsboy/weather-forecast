---
name: "weather-forecast"
description: "查询城市天气信息，支持实时天气和天气预报。当用户询问天气、需要天气数据时自动激活。"
version: "1.0.0"
author: "TianHe Medical Kiosk Team"
keywords:
  - weather
  - 天气
  - 天气预报
  - 高德地图
  - amap
---

# Weather Forecast Skill

天气预报技能，基于高德地图Web服务API，为OpenClaw/CoPaw提供天气查询能力。

## 功能特性

- **实时天气查询**：获取城市当前天气状况
- **天气预报查询**：获取未来3-4天天气预报
- **今日天气**：便捷获取当天天气详情
- **城市名支持**：支持中文城市名和adcode编码

## 安装配置

### 1. 安装依赖

```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/weather-forecast

# 安装依赖
npm install
```

### 2. 配置API密钥

**推荐方式：使用AgentSecrets（安全）**

```bash
# 安装 AgentSecrets
npm install -g @the-17/agentsecrets

# 初始化
agentsecrets init

# 保存高德地图API密钥
agentsecrets secrets set AMAP_API_KEY=your_amap_api_key_here
```

**备选方式：环境变量**

```bash
# macOS/Linux
export AMAP_API_KEY="your_amap_api_key_here"

# Windows PowerShell
$env:AMAP_API_KEY="your_amap_api_key_here"
```

**备选方式：openclaw.json配置**

在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "env": {
    "AMAP_API_KEY": "your_amap_api_key_here"
  }
}
```

### 3. 重启Gateway

```bash
openclaw gateway restart
```

## 使用方法

### 对话示例

```
用户：北京今天天气怎么样？
Agent：正在查询北京天气...

用户：沈阳浑南区明天天气如何？
Agent：正在查询沈阳浑南区天气预报...

用户：查询上海市实时天气
Agent：正在获取上海实时天气数据...
```

### 支持的城市名

| 城市名 | adcode |
|--------|--------|
| 北京/北京市 | 110000 |
| 上海/上海市 | 310000 |
| 广州/广州市 | 440100 |
| 深圳/深圳市 | 440300 |
| 沈阳/沈阳市 | 210100 |
| 沈阳浑南区/浑南区 | 210112 |
| 杭州/杭州市 | 330100 |
| 成都/成都市 | 510100 |

完整城市编码表：https://lbs.amap.com/api/webservice/download

## 工具列表

### get_realtime_weather

获取城市实时天气信息。

**参数：**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| city | string | 是 | 城市名称或adcode编码 |

**返回示例：**
```json
{
  "success": true,
  "city": "浑南区",
  "weather": "多云",
  "temperature": "7",
  "humidity": "45",
  "wind_direction": "西南",
  "wind_power": "1-3",
  "report_time": "2026-03-08 22:31:53"
}
```

### get_forecast_weather

获取城市天气预报（包含当天及未来几天）。

**参数：**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| city | string | 是 | 城市名称或adcode编码 |

**返回示例：**
```json
{
  "success": true,
  "city": "浑南区",
  "province": "辽宁",
  "forecasts": [
    {
      "date": "2026-03-08",
      "week": "7",
      "day_weather": "多云",
      "night_weather": "晴",
      "day_temp": "7",
      "night_temp": "-6"
    }
  ]
}
```

### get_today_weather

获取当天天气预报（便捷方法）。

**参数：**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| city | string | 是 | 城市名称或adcode编码 |

## API参考

本技能基于高德地图Web服务API：

- **服务地址**：`https://restapi.amap.com/v3/weather/weatherInfo`
- **官方文档**：https://lbs.amap.com/api/webservice/guide/api-advanced/weatherinfo

### 请求参数

| 参数 | 必填 | 说明 |
|------|------|------|
| key | 是 | API密钥 |
| city | 是 | 城市adcode |
| extensions | 否 | base=实况, all=预报 |

### 错误码

| infocode | 说明 |
|----------|------|
| 10000 | 成功 |
| 10001 | key不存在 |
| 10003 | 日调用量超限 |
| 10004 | 访问频率超限 |
| 10006 | 无效key |

## 数据更新频率

- **实时天气**：每小时更新多次
- **预报天气**：每天8:00、11:00、18:00左右更新

## 注意事项

1. **API密钥安全**：请勿在代码中硬编码密钥，使用AgentSecrets或环境变量
2. **请求频率**：高德API有调用频率限制，建议合理使用
3. **城市编码**：支持城市名自动转换为adcode，也可直接使用adcode

## 更新日志

### v1.0.0 (2026-03-08)
- 初始版本
- 支持实时天气查询
- 支持天气预报查询
- 支持城市名和adcode编码
- 集成AgentSecrets密钥管理

## 许可证

Apache License 2.0

## 相关链接

- [高德开放平台](https://lbs.amap.com/)
- [API文档](https://lbs.amap.com/api/webservice/guide/api-advanced/weatherinfo)
- [城市编码表](https://lbs.amap.com/api/webservice/download)
