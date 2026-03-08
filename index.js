const { Tool } = require("@openclaw/tool");

const AMAP_WEATHER_URL = "https://restapi.amap.com/v3/weather/weatherInfo";

const CITY_MAPPING = {
  "北京": "110000",
  "北京市": "110000",
  "上海": "310000",
  "上海市": "310000",
  "广州": "440100",
  "广州市": "440100",
  "深圳": "440300",
  "深圳市": "440300",
  "沈阳": "210100",
  "沈阳市": "210100",
  "沈阳浑南区": "210112",
  "浑南区": "210112",
  "杭州": "330100",
  "杭州市": "330100",
  "成都": "510100",
  "成都市": "510100",
  "武汉": "420100",
  "武汉市": "420100",
  "南京": "320100",
  "南京市": "320100",
  "天津": "120000",
  "天津市": "120000",
  "重庆": "500000",
  "重庆市": "500000",
  "西安": "610100",
  "西安市": "610100",
  "苏州": "320500",
  "苏州市": "320500",
  "郑州": "410100",
  "郑州市": "410100",
  "长沙": "430100",
  "长沙市": "430100",
  "济南": "370100",
  "济南市": "370100",
  "青岛": "370200",
  "青岛市": "370200",
  "大连": "210200",
  "大连市": "210200"
};

function getAdcode(city) {
  if (/^\d+$/.test(city)) {
    return city;
  }
  return CITY_MAPPING[city] || city;
}

function getApiKey() {
  return process.env.AMAP_API_KEY || process.env.AMAP_KEY || "";
}

async function fetchWeather(adcode, extensions = "base") {
  const apiKey = getApiKey();
  
  if (!apiKey) {
    throw new Error("未配置高德地图API密钥，请设置环境变量 AMAP_API_KEY");
  }
  
  const url = new URL(AMAP_WEATHER_URL);
  url.searchParams.set("city", adcode);
  url.searchParams.set("key", apiKey);
  url.searchParams.set("extensions", extensions);
  url.searchParams.set("output", "JSON");
  
  const response = await fetch(url.toString());
  const data = await response.json();
  
  if (data.status !== "1") {
    throw new Error(`API错误: ${data.info || "未知错误"} (code: ${data.infocode})`);
  }
  
  return data;
}

module.exports = {
  create: (options) => {
    const realtimeWeatherTool = new Tool({
      name: "get_realtime_weather",
      description: "获取城市实时天气信息，包括温度、湿度、风向、风力等。当用户询问当前天气、实时天气时使用。",
      parameters: {
        city: {
          type: "string",
          description: "城市名称（如：北京、上海、沈阳浑南区）或城市编码adcode",
          required: true
        }
      },
      execute: async (toolCallId, args) => {
        try {
          const adcode = getAdcode(args.city);
          const data = await fetchWeather(adcode, "base");
          
          if (!data.lives || data.lives.length === 0) {
            return {
              result: `未找到城市 "${args.city}" 的天气数据`,
              error: true
            };
          }
          
          const live = data.lives[0];
          const result = `📍 ${live.city} 实时天气\n` +
            `🌤️ 天气：${live.weather}\n` +
            `🌡️ 温度：${live.temperature}°C\n` +
            `💧 湿度：${live.humidity}%\n` +
            `🌬️ 风向：${live.winddirection}风 ${live.windpower}级\n` +
            `📅 更新时间：${live.reporttime}`;
          
          return {
            result,
            data: {
              success: true,
              city: live.city,
              adcode: live.adcode,
              weather: live.weather,
              temperature: live.temperature,
              humidity: live.humidity,
              wind_direction: live.winddirection,
              wind_power: live.windpower,
              report_time: live.reporttime
            }
          };
        } catch (error) {
          return {
            result: `查询天气失败：${error.message}`,
            error: true
          };
        }
      }
    });

    const forecastWeatherTool = new Tool({
      name: "get_forecast_weather",
      description: "获取城市天气预报，包含当天及未来3-4天的天气情况。当用户询问天气预报、未来天气、明天天气时使用。",
      parameters: {
        city: {
          type: "string",
          description: "城市名称（如：北京、上海、沈阳浑南区）或城市编码adcode",
          required: true
        }
      },
      execute: async (toolCallId, args) => {
        try {
          const adcode = getAdcode(args.city);
          const data = await fetchWeather(adcode, "all");
          
          if (!data.forecasts || data.forecasts.length === 0) {
            return {
              result: `未找到城市 "${args.city}" 的天气预报数据`,
              error: true
            };
          }
          
          const forecast = data.forecasts[0];
          const casts = forecast.casts || [];
          
          let result = `📍 ${forecast.city}（${forecast.province}）天气预报\n`;
          result += `📅 发布时间：${forecast.reporttime}\n\n`;
          
          const weekMap = ["日", "一", "二", "三", "四", "五", "六"];
          
          casts.forEach((cast, index) => {
            const dayLabel = index === 0 ? "今天" : index === 1 ? "明天" : `后天起第${index}天`;
            result += `【${dayLabel} ${cast.date} 星期${weekMap[parseInt(cast.week)] || cast.week}】\n`;
            result += `  ☀️ 白天：${cast.dayweather} ${cast.daytemp}°C ${cast.daywind}风 ${cast.daypower}级\n`;
            result += `  🌙 夜间：${cast.nightweather} ${cast.nighttemp}°C ${cast.nightwind}风 ${cast.nightpower}级\n\n`;
          });
          
          return {
            result,
            data: {
              success: true,
              city: forecast.city,
              adcode: forecast.adcode,
              province: forecast.province,
              report_time: forecast.reporttime,
              forecasts: casts.map(cast => ({
                date: cast.date,
                week: cast.week,
                day_weather: cast.dayweather,
                night_weather: cast.nightweather,
                day_temp: cast.daytemp,
                night_temp: cast.nighttemp,
                day_wind: cast.daywind,
                night_wind: cast.nightwind,
                day_power: cast.daypower,
                night_power: cast.nightpower
              }))
            }
          };
        } catch (error) {
          return {
            result: `查询天气预报失败：${error.message}`,
            error: true
          };
        }
      }
    });

    const todayWeatherTool = new Tool({
      name: "get_today_weather",
      description: "获取当天天气预报的便捷方法，返回今日天气详情。当用户询问今天天气、今日天气时使用。",
      parameters: {
        city: {
          type: "string",
          description: "城市名称（如：北京、上海、沈阳浑南区）或城市编码adcode",
          required: true
        }
      },
      execute: async (toolCallId, args) => {
        try {
          const adcode = getAdcode(args.city);
          const data = await fetchWeather(adcode, "all");
          
          if (!data.forecasts || data.forecasts.length === 0 || !data.forecasts[0].casts || data.forecasts[0].casts.length === 0) {
            return {
              result: `未找到城市 "${args.city}" 的天气数据`,
              error: true
            };
          }
          
          const forecast = data.forecasts[0];
          const today = forecast.casts[0];
          const weekMap = ["日", "一", "二", "三", "四", "五", "六"];
          
          const result = `📍 ${forecast.city} 今日天气\n` +
            `📅 ${today.date} 星期${weekMap[parseInt(today.week)] || today.week}\n\n` +
            `☀️ 白天：${today.dayweather} ${today.daytemp}°C\n` +
            `   风向：${today.daywind}风 ${today.daypower}级\n\n` +
            `🌙 夜间：${today.nightweather} ${today.nighttemp}°C\n` +
            `   风向：${today.nightwind}风 ${today.nightpower}级`;
          
          return {
            result,
            data: {
              success: true,
              city: forecast.city,
              province: forecast.province,
              date: today.date,
              week: today.week,
              day_weather: today.dayweather,
              night_weather: today.nightweather,
              day_temp: today.daytemp,
              night_temp: today.nighttemp,
              day_wind: today.daywind,
              night_wind: today.nightwind,
              day_power: today.daypower,
              night_power: today.nightpower
            }
          };
        } catch (error) {
          return {
            result: `查询今日天气失败：${error.message}`,
            error: true
          };
        }
      }
    });

    return [realtimeWeatherTool, forecastWeatherTool, todayWeatherTool];
  }
};
