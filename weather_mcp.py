from __future__ import annotations

import json
import urllib.parse
import urllib.request
from datetime import datetime

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("today-weather")


def _fetch_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def _geocode_city(city: str) -> tuple[float, float, str, str]:
    query = urllib.parse.quote(city)
    geo_url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={query}&count=1&language=zh&format=json"
    )
    geo = _fetch_json(geo_url)

    results = geo.get("results") or []
    if not results:
        raise ValueError(f"未找到城市：{city}")

    first = results[0]
    latitude = first["latitude"]
    longitude = first["longitude"]
    name = first.get("name", city)
    country = first.get("country", "")
    return latitude, longitude, name, country


def _weather_code_text(code: int) -> str:
    mapping = {
        0: "晴",
        1: "大体晴朗",
        2: "局部多云",
        3: "阴",
        45: "雾",
        48: "冻雾",
        51: "小毛毛雨",
        53: "中毛毛雨",
        55: "大毛毛雨",
        61: "小雨",
        63: "中雨",
        65: "大雨",
        71: "小雪",
        73: "中雪",
        75: "大雪",
        80: "小阵雨",
        81: "中阵雨",
        82: "强阵雨",
        95: "雷暴",
    }
    return mapping.get(code, f"未知天气代码({code})")


@mcp.tool(description="查询某个城市今日天气（默认中文输出）")
def today_weather(city: str) -> str:
    """查询某个城市今日天气。

    参数:
        city: 城市名称，例如“北京”“Shanghai”。
    """
    latitude, longitude, city_name, country = _geocode_city(city)

    weather_url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        "&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m"
        "&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset"
        "&timezone=auto"
    )
    weather = _fetch_json(weather_url)

    current = weather["current"]
    daily = weather["daily"]

    date_text = datetime.now().strftime("%Y-%m-%d")
    max_temp = daily["temperature_2m_max"][0]
    min_temp = daily["temperature_2m_min"][0]
    sunrise = daily["sunrise"][0]
    sunset = daily["sunset"][0]

    desc = _weather_code_text(int(current["weather_code"]))
    region = f"{city_name}, {country}" if country else city_name

    return (
        f"{region} 今日天气（{date_text}）\n"
        f"天气：{desc}\n"
        f"当前温度：{current['temperature_2m']}°C（体感 {current['apparent_temperature']}°C）\n"
        f"相对湿度：{current['relative_humidity_2m']}%\n"
        f"风速：{current['wind_speed_10m']} km/h\n"
        f"今日最高/最低：{max_temp}°C / {min_temp}°C\n"
        f"日出/日落：{sunrise} / {sunset}"
    )


if __name__ == "__main__":
    mcp.run()
