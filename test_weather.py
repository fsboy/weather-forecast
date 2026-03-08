import asyncio
import os
os.environ['AMAP_API_KEY'] = '20cd0490c65571a0c86b67e6e4826741'

from weather_tools import get_realtime_weather, get_forecast_weather, get_today_weather
from weather_tools import format_weather_result, format_forecast_result

async def test():
    print("=" * 50)
    print("测试1：查询沈阳浑南区实时天气")
    print("=" * 50)
    result = await get_realtime_weather("沈阳浑南区")
    print(format_weather_result(result))
    
    print("\n" + "=" * 50)
    print("测试2：查询北京今日天气")
    print("=" * 50)
    today = await get_today_weather("北京")
    if today.get("success"):
        print(f"📍 {today['city']}（{today.get('province', '')}）今日天气")
        print(f"📅 {today['date']} 星期{today['week']}")
        print(f"☀️ 白天：{today['day_weather']} {today['day_temp']}°C {today['day_wind']}风 {today['day_power']}级")
        print(f"🌙 夜间：{today['night_weather']} {today['night_temp']}°C {today['night_wind']}风 {today['night_power']}级")
    else:
        print(f"查询失败: {today.get('error_message', '未知错误')}")
    
    print("\n" + "=" * 50)
    print("测试3：查询上海天气预报")
    print("=" * 50)
    forecast = await get_forecast_weather("上海")
    print(format_forecast_result(forecast))

if __name__ == "__main__":
    asyncio.run(test())
