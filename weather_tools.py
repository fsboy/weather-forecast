"""
Weather Forecast Skill for CoPaw
基于高德地图Web服务API的天气预报技能
"""

import os
import aiohttp
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict


AMAP_WEATHER_URL = "https://restapi.amap.com/v3/weather/weatherInfo"

CITY_MAPPING = {
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
    "大连市": "210200",
}


def get_adcode(city: str) -> str:
    """
    将城市名转换为adcode编码
    
    Args:
        city: 城市名称或adcode编码
        
    Returns:
        adcode编码
    """
    if city.isdigit():
        return city
    return CITY_MAPPING.get(city, city)


def get_api_key() -> str:
    """
    获取高德地图API密钥
    
    优先级：
    1. 环境变量 AMAP_API_KEY
    2. 环境变量 AMAP_KEY
    3. 默认城市编码
    
    Returns:
        API密钥
    """
    return os.environ.get("AMAP_API_KEY") or os.environ.get("AMAP_KEY", "")


def get_default_city() -> str:
    """
    获取默认城市编码
    
    Returns:
        默认城市adcode
    """
    return os.environ.get("DEFAULT_CITY", "110000")


@dataclass
class WeatherResult:
    """实时天气结果"""
    success: bool
    city: str = ""
    adcode: str = ""
    weather: str = ""
    temperature: str = ""
    wind_direction: str = ""
    wind_power: str = ""
    humidity: str = ""
    report_time: str = ""
    error_message: str = ""


@dataclass
class ForecastDay:
    """单日预报数据"""
    date: str
    week: str
    day_weather: str
    night_weather: str
    day_temp: str
    night_temp: str
    day_wind: str
    night_wind: str
    day_power: str
    night_power: str


@dataclass
class WeatherForecastResult:
    """天气预报结果"""
    success: bool
    city: str = ""
    adcode: str = ""
    province: str = ""
    report_time: str = ""
    forecasts: List[Dict[str, Any]] = field(default_factory=list)
    error_message: str = ""


async def fetch_weather(adcode: str, extensions: str = "base") -> Dict[str, Any]:
    """
    调用高德地图天气API
    
    Args:
        adcode: 城市编码
        extensions: base=实况天气, all=预报天气
        
    Returns:
        API响应数据
        
    Raises:
        ValueError: API密钥未配置
        RuntimeError: API调用失败
    """
    api_key = get_api_key()
    
    if not api_key:
        raise ValueError(
            "未配置高德地图API密钥。请通过以下方式之一配置：\n"
            "1. 环境变量: export AMAP_API_KEY='your_api_key'\n"
            "2. CoPaw配置: copaw init → Configure environment variables\n"
            "3. config.json: {\"env\": {\"AMAP_API_KEY\": \"your_api_key\"}}"
        )
    
    params = {
        "city": adcode,
        "key": api_key,
        "extensions": extensions,
        "output": "JSON"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(AMAP_WEATHER_URL, params=params) as response:
            data = await response.json()
            
            if data.get("status") != "1":
                raise RuntimeError(
                    f"API错误: {data.get('info', '未知错误')} "
                    f"(code: {data.get('infocode')})"
                )
            
            return data


async def get_realtime_weather(city: str) -> Dict[str, Any]:
    """
    获取城市实时天气信息
    
    Args:
        city: 城市名称（如：北京、上海、沈阳浑南区）或城市编码adcode
        
    Returns:
        包含实时天气信息的字典
        
    Example:
        result = await get_realtime_weather("沈阳浑南区")
        if result["success"]:
            print(f"{result['city']}: {result['weather']}, {result['temperature']}°C")
    """
    adcode = get_adcode(city)
    
    try:
        data = await fetch_weather(adcode, "base")
        
        lives = data.get("lives", [])
        if not lives:
            return asdict(WeatherResult(
                success=False,
                error_message=f"未找到城市 '{city}' 的天气数据"
            ))
        
        live = lives[0]
        return asdict(WeatherResult(
            success=True,
            city=live.get("city", ""),
            adcode=live.get("adcode", ""),
            weather=live.get("weather", ""),
            temperature=live.get("temperature", ""),
            wind_direction=live.get("winddirection", ""),
            wind_power=live.get("windpower", ""),
            humidity=live.get("humidity", ""),
            report_time=live.get("reporttime", "")
        ))
        
    except ValueError as e:
        return asdict(WeatherResult(success=False, error_message=str(e)))
    except Exception as e:
        return asdict(WeatherResult(success=False, error_message=f"查询失败: {str(e)}"))


async def get_forecast_weather(city: str) -> Dict[str, Any]:
    """
    获取城市天气预报信息（包含当天及未来几天）
    
    Args:
        city: 城市名称（如：北京、上海、沈阳浑南区）或城市编码adcode
        
    Returns:
        包含天气预报信息的字典
        
    Example:
        result = await get_forecast_weather("沈阳浑南区")
        if result["success"]:
            for day in result["forecasts"]:
                print(f"{day['date']}: {day['day_weather']} {day['day_temp']}°C")
    """
    adcode = get_adcode(city)
    
    try:
        data = await fetch_weather(adcode, "all")
        
        forecasts_data = data.get("forecasts", [])
        if not forecasts_data:
            return asdict(WeatherForecastResult(
                success=False,
                error_message=f"未找到城市 '{city}' 的天气预报数据"
            ))
        
        forecast = forecasts_data[0]
        casts = forecast.get("casts", [])
        
        forecast_days = [
            {
                "date": cast.get("date", ""),
                "week": cast.get("week", ""),
                "day_weather": cast.get("dayweather", ""),
                "night_weather": cast.get("nightweather", ""),
                "day_temp": cast.get("daytemp", ""),
                "night_temp": cast.get("nighttemp", ""),
                "day_wind": cast.get("daywind", ""),
                "night_wind": cast.get("nightwind", ""),
                "day_power": cast.get("daypower", ""),
                "night_power": cast.get("nightpower", "")
            }
            for cast in casts
        ]
        
        return {
            "success": True,
            "city": forecast.get("city", ""),
            "adcode": forecast.get("adcode", ""),
            "province": forecast.get("province", ""),
            "report_time": forecast.get("reporttime", ""),
            "forecasts": forecast_days,
            "error_message": ""
        }
        
    except ValueError as e:
        return {"success": False, "error_message": str(e), "forecasts": []}
    except Exception as e:
        return {"success": False, "error_message": f"查询失败: {str(e)}", "forecasts": []}


async def get_today_weather(city: str) -> Dict[str, Any]:
    """
    获取当天天气预报（便捷方法）
    
    Args:
        city: 城市名称（如：北京、上海、沈阳浑南区）或城市编码adcode
        
    Returns:
        包含今日天气信息的字典
        
    Example:
        weather = await get_today_weather("沈阳浑南区")
        print(f"今天: {weather['day_weather']}, {weather['day_temp']}°C / {weather['night_temp']}°C")
    """
    result = await get_forecast_weather(city)
    
    if not result.get("success"):
        return result
    
    forecasts = result.get("forecasts", [])
    if not forecasts:
        return {
            "success": False,
            "error_message": "无预报数据",
            "city": result.get("city", "")
        }
    
    today = forecasts[0]
    return {
        "success": True,
        "city": result.get("city", ""),
        "province": result.get("province", ""),
        "date": today.get("date", ""),
        "week": today.get("week", ""),
        "day_weather": today.get("day_weather", ""),
        "night_weather": today.get("night_weather", ""),
        "day_temp": today.get("day_temp", ""),
        "night_temp": today.get("night_temp", ""),
        "day_wind": today.get("day_wind", ""),
        "night_wind": today.get("night_wind", ""),
        "day_power": today.get("day_power", ""),
        "night_power": today.get("night_power", "")
    }


def format_weather_result(result: Dict[str, Any]) -> str:
    """
    格式化实时天气结果为可读文本
    
    Args:
        result: get_realtime_weather返回的结果
        
    Returns:
        格式化的天气文本
    """
    if not result.get("success"):
        return f"查询失败: {result.get('error_message', '未知错误')}"
    
    return (
        f"📍 {result['city']} 实时天气\n"
        f"🌤️ 天气：{result['weather']}\n"
        f"🌡️ 温度：{result['temperature']}°C\n"
        f"💧 湿度：{result['humidity']}%\n"
        f"🌬️ 风向：{result['wind_direction']}风 {result['wind_power']}级\n"
        f"📅 更新时间：{result['report_time']}"
    )


def format_forecast_result(result: Dict[str, Any]) -> str:
    """
    格式化天气预报结果为可读文本
    
    Args:
        result: get_forecast_weather返回的结果
        
    Returns:
        格式化的天气预报文本
    """
    if not result.get("success"):
        return f"查询失败: {result.get('error_message', '未知错误')}"
    
    week_map = {"1": "一", "2": "二", "3": "三", "4": "四", "5": "五", "6": "六", "7": "日"}
    
    lines = [
        f"📍 {result['city']}（{result['province']}）天气预报",
        f"📅 发布时间：{result['report_time']}",
        ""
    ]
    
    for i, cast in enumerate(result.get("forecasts", [])):
        day_label = "今天" if i == 0 else "明天" if i == 1 else f"后天起第{i}天"
        week = week_map.get(cast.get("week", ""), cast.get("week", ""))
        
        lines.extend([
            f"【{day_label} {cast['date']} 星期{week}】",
            f"  ☀️ 白天：{cast['day_weather']} {cast['day_temp']}°C {cast['day_wind']}风 {cast['day_power']}级",
            f"  🌙 夜间：{cast['night_weather']} {cast['night_temp']}°C {cast['night_wind']}风 {cast['night_power']}级",
            ""
        ])
    
    return "\n".join(lines)


# CoPaw Skill 入口
SKILL_TOOLS = [
    {
        "name": "get_realtime_weather",
        "function": get_realtime_weather,
        "description": "获取城市实时天气信息，包括温度、湿度、风向、风力等。当用户询问当前天气、实时天气时使用。",
        "parameters": {
            "city": {
                "type": "string",
                "description": "城市名称（如：北京、上海、沈阳浑南区）或城市编码adcode",
                "required": True
            }
        }
    },
    {
        "name": "get_forecast_weather",
        "function": get_forecast_weather,
        "description": "获取城市天气预报，包含当天及未来3-4天的天气情况。当用户询问天气预报、未来天气、明天天气时使用。",
        "parameters": {
            "city": {
                "type": "string",
                "description": "城市名称（如：北京、上海、沈阳浑南区）或城市编码adcode",
                "required": True
            }
        }
    },
    {
        "name": "get_today_weather",
        "function": get_today_weather,
        "description": "获取当天天气预报的便捷方法，返回今日天气详情。当用户询问今天天气、今日天气时使用。",
        "parameters": {
            "city": {
                "type": "string",
                "description": "城市名称（如：北京、上海、沈阳浑南区）或城市编码adcode",
                "required": True
            }
        }
    }
]


if __name__ == "__main__":
    import asyncio
    
    async def demo():
        """演示天气查询功能"""
        city = "沈阳浑南区"
        
        print("=== 实时天气 ===")
        result = await get_realtime_weather(city)
        print(format_weather_result(result))
        
        print("\n=== 今日天气 ===")
        today = await get_today_weather(city)
        if today.get("success"):
            print(f"日期: {today['date']} (星期{today['week']})")
            print(f"白天: {today['day_weather']} {today['day_temp']}°C")
            print(f"夜间: {today['night_weather']} {today['night_temp']}°C")
        
        print("\n=== 天气预报 ===")
        forecast = await get_forecast_weather(city)
        print(format_forecast_result(forecast))
    
    asyncio.run(demo())
