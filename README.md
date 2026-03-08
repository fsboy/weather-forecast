# Weather Forecast Skill

OpenClaw / CoPaw 天气预报技能，基于高德地图Web服务API。

## 快速开始

### 安装

```bash
cd ~/.openclaw/workspace/skills/weather-forecast
npm install
```

### 配置API密钥

**推荐方式：AgentSecrets**

```bash
# 安装 AgentSecrets
npm install -g @the-17/agentsecrets

# 初始化
agentsecrets init

# 保存密钥
agentsecrets secrets set AMAP_API_KEY=your_api_key
```

**备选方式：环境变量**

```bash
export AMAP_API_KEY="your_api_key"
```

**备选方式：openclaw.json**

```json
{
  "env": {
    "AMAP_API_KEY": "your_api_key"
  }
}
```

### 重启服务

```bash
openclaw gateway restart
```

## 使用示例

```
用户：北京今天天气怎么样？
用户：沈阳浑南区明天天气如何？
用户：查询上海市实时天气
```

## 支持的城市

| 城市 | 编码 |
|------|------|
| 北京 | 110000 |
| 上海 | 310000 |
| 广州 | 440100 |
| 深圳 | 440300 |
| 沈阳浑南区 | 210112 |

## 工具说明

| 工具 | 说明 |
|------|------|
| get_realtime_weather | 获取实时天气 |
| get_forecast_weather | 获取天气预报 |
| get_today_weather | 获取今日天气 |

## 获取API密钥

1. 访问 [高德开放平台](https://console.amap.com/)
2. 注册并登录
3. 创建应用，选择"Web服务"
4. 获取Key

## 许可证

Apache License 2.0
