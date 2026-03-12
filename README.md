# ailab

一个用于实验 MCP（Model Context Protocol）能力的仓库。

## 今日天气 MCP

本仓库提供了一个可直接运行的 MCP 服务：`weather_mcp.py`。

### 功能

- 提供 `today_weather(city: str)` 工具。
- 输入城市名，返回该城市“今日天气摘要”（温度、体感、湿度、风速、最高/最低温、日出日落）。
- 使用 Open-Meteo（免 API Key）获取地理编码与天气数据。

## 1) 安装与启动

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python weather_mcp.py
```

> `weather_mcp.py` 默认用 **stdio** 方式启动 MCP 服务，适合被 MCP 客户端拉起并调用。

## 2) 在客户端里注册这个 MCP

你需要把 `weather_mcp.py` 配到 MCP 客户端配置中。核心是这段：

```json
{
  "mcpServers": {
    "today-weather": {
      "command": "python",
      "args": ["/workspace/ailab/weather_mcp.py"]
    }
  }
}
```

如果你使用虚拟环境，推荐写成更稳妥的绝对路径（避免客户端找不到依赖）：

```json
{
  "mcpServers": {
    "today-weather": {
      "command": "/workspace/ailab/.venv/bin/python",
      "args": ["/workspace/ailab/weather_mcp.py"]
    }
  }
}
```

## 3) 怎么调用这个 MCP（最关键）

在支持 MCP 的客户端（如 Claude Desktop / Cursor / Cline 等）里：

1. 确认客户端已加载到 `today-weather` 这个 server。  
2. 选择工具（tool）`today_weather`。  
3. 传入参数：

```json
{"city": "北京"}
```

### 调用示例

- 工具名：`today_weather`
- 参数示例：`{"city": "Shanghai"}`

返回示例（节选）：

```text
Beijing, China 今日天气（2026-01-01）
天气：晴
当前温度：2.1°C（体感 -1.0°C）
相对湿度：42%
风速：12.4 km/h
今日最高/最低：5.3°C / -2.8°C
日出/日落：2026-01-01T07:34 / 2026-01-01T17:02
```

## 4) 常见问题

### Q1: 为什么我“能启动脚本”，但在客户端看不到工具？

通常是客户端没有正确加载 MCP 配置，或 `command` 路径不对。优先检查：

- `command` 是否为可执行 Python 路径；
- `args` 是否是 `weather_mcp.py` 的绝对路径；
- 客户端重启后是否生效。

### Q2: 城市查不到怎么办？

这个服务会先走 Open-Meteo 地理编码，建议尝试：

- 改用英文城市名（例如 `Guangzhou`）；
- 增加地区信息（例如 `Nanjing`、`Nanjing Jiangsu`）。

### Q3: 能否直接 `python weather_mcp.py --city 北京` 调用？

当前版本是 MCP 工具服务，不是 CLI 查询脚本。你需要通过 MCP 客户端来调用 `today_weather`。
