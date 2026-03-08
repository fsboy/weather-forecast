---
name: "weather-forecast"
description: "查询城市天气信息，支持实时天气和天气预报。当用户询问天气、需要天气数据时自动激活。"
version: "1.0.0"
author: "TianHe Medical Kiosk Team"
tags:
  - weather
  - 天气
  - 天气预报
  - 高德地图
---

# Weather Forecast Skill

天气预报技能，基于高德地图Web服务API，为CoPaw提供天气查询能力。

## 功能特性

- 实时天气查询：获取城市当前天气状况
- 天气预报查询：获取未来3-4天天气预报
- 今日天气：便捷获取当天天气详情
- 城市名支持：支持中文城市名和adcode编码

## 安装配置

### 1. 复制技能到CoPaw目录

```bash
# 将技能复制到CoPaw的skills目录
cp -r weather-forecast ~/.copaw/skills/
```

### 2. 配置API密钥

**方式一：copaw init 交互式配置（推荐）**

```bash
copaw init
# 在 "Configure environment variables?" 步骤选择 Yes
# 添加环境变量：
#   Key: AMAP_API_KEY
#   Value: your_amap_api_key
```

**方式二：Console配置**

1. 启动CoPaw：`copaw app`
2. 打开 http://127.0.0.1:8088/
3. 进入 Settings → Environment Variables
4. 添加：`AMAP_API_KEY = your_amap_api_key`

**方式三：环境变量**

```bash
# macOS/Linux
export AMAP_API_KEY="your_amap_api_key"

# Windows PowerShell
$env:AMAP_API_KEY="your_amap_api_key"

# Windows CMD
set AMAP_API_KEY=your_amap_api_key
```

**方式四：config.json配置**

编辑 `~/.copaw/config.json`：

```json
{
  "env": {
    "AMAP_API_KEY": "your_amap_api_key",
    "DEFAULT_CITY": "110000"
  }
}
```

### 3. 配置默认城市（可选）

```bash
# 设置默认城市
export DEFAULT_CITY="210112"  # 沈阳浑南区
```

### 4. 重启CoPaw

```bash
copaw app --reload
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

| 城市名 | adcode | 城市名 | adcode |
|--------|--------|--------|--------|
| 北京 | 110000 | 上海 | 310000 |
| 广州 | 440100 | 深圳 | 440300 |
| 沈阳 | 210100 | 沈阳浑南区 | 210112 |
| 杭州 | 330100 | 成都 | 510100 |
| 武汉 | 420100 | 南京 | 320100 |

完整城市编码表：https://lbs.amap.com/api/webservice/download

## 工具说明

### get_realtime_weather

获取城市实时天气信息。

**参数：**
- city (string, 必填): 城市名称或adcode编码

**返回：**
```json
{
  "success": true,
  "city": "浑南区",
  "weather": "多云",
  "temperature": "7",
  "humidity": "45",
  "wind_direction": "西南",
  "wind_power": "1-3"
}
```

### get_forecast_weather

获取城市天气预报（包含当天及未来几天）。

**参数：**
- city (string, 必填): 城市名称或adcode编码

### get_today_weather

获取当天天气预报（便捷方法）。

**参数：**
- city (string, 必填): 城市名称或adcode编码

## API参考

本技能基于高德地图Web服务API：

- 服务地址：https://restapi.amap.com/v3/weather/weatherInfo
- 官方文档：https://lbs.amap.com/api/webservice/guide/api-advanced/weatherinfo

### 错误码

| infocode | 说明 |
|----------|------|
| 10000 | 成功 |
| 10001 | key不存在 |
| 10003 | 日调用量超限 |
| 10004 | 访问频率超限 |
| 10006 | 无效key |

## 获取API密钥

1. 访问 [高德开放平台](https://console.amap.com/)
2. 注册并登录
3. 创建应用 → 选择"Web服务"
4. 获取Key

## 注意事项

1. API密钥安全：使用环境变量或config.json配置，不要硬编码
2. 请求频率：高德API有调用频率限制，建议合理使用
3. 城市编码：支持城市名自动转换为adcode

## 更新日志

### v1.0.0 (2026-03-08)
- 初始版本
- 支持实时天气查询
- 支持天气预报查询
- 支持城市名和adcode编码

## 许可证

Apache License 2.0
