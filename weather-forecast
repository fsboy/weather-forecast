#!/usr/bin/env python3
"""
Weather Forecast Skill - Command Line Entry Point
天气预报技能命令行入口
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from weather_tools import get_realtime_weather, get_forecast_weather, get_today_weather
from weather_tools import format_weather_result, format_forecast_result, get_default_city
import asyncio
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="天气预报查询工具 - Weather Forecast Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  weather-forecast --city "沈阳浑南区"
  weather-forecast --city "北京" --type forecast
  weather-forecast --city "上海" --type today
        """
    )
    
    parser.add_argument(
        "--city", 
        type=str, 
        help="城市名称（如：北京、上海、沈阳浑南区）或城市编码adcode"
    )
    
    parser.add_argument(
        "--type", 
        type=str, 
        choices=["realtime", "forecast", "today"],
        default="realtime",
        help="查询类型：realtime(实时天气), forecast(天气预报), today(今日天气)"
    )
    
    args = parser.parse_args()
    
    async def run_query():
        city = args.city or get_default_city()
        
        if args.type == "realtime":
            result = await get_realtime_weather(city)
            print(format_weather_result(result))
        elif args.type == "forecast":
            result = await get_forecast_weather(city)
            print(format_forecast_result(result))
        elif args.type == "today":
            result = await get_today_weather(city)
            if result.get("success"):
                print(f"📍 {result['city']}（{result.get('province', '')}）今日天气")
                print(f"📅 {result['date']} 星期{result['week']}")
                print(f"☀️ 白天：{result['day_weather']} {result['day_temp']}°C {result['day_wind']}风 {result['day_power']}级")
                print(f"🌙 夜间：{result['night_weather']} {result['night_temp']}°C {result['night_wind']}风 {result['night_power']}级")
            else:
                print(f"查询失败: {result.get('error_message', '未知错误')}")
    
    try:
        asyncio.run(run_query())
    except KeyboardInterrupt:
        print("\n查询已取消")
        sys.exit(0)
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
