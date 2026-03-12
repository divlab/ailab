# ailab

一个用于实验 MCP（Model Context Protocol）能力的仓库。

## 今日天气 MCP

本仓库提供了一个可直接运行的 MCP 服务：`weather_mcp.py`。

### 功能

- 提供 `today_weather(city: str)` 工具。
- 输入城市名，返回该城市“今日天气摘要”（温度、体感、湿度、风速、最高/最低温、日出日落）。
- 使用 Open-Meteo（免 API Key）获取地理编码与天气数据。

### 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 运行

```bash
python weather_mcp.py
```

默认将以 MCP 服务方式启动。

### 在 MCP 客户端中配置（示例）

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

### 调用示例

在支持 MCP 的客户端中调用：

- 工具名：`today_weather`
- 参数示例：`{"city": "北京"}`

返回示例（节选）：

```text
北京, China 今日天气（2026-01-01）
天气：晴
当前温度：2.1°C（体感 -1.0°C）
...
```
