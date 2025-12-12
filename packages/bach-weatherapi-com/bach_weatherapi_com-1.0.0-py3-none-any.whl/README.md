# Weatherapi Com MCP Server

[English](./README_EN.md) | 简体中文 | [繁體中文](./README_ZH-TW.md)

用于访问 Weatherapi Com API 的 MCP 服务器。

## 🚀 使用 EMCP 平台快速体验

**[EMCP](https://sit-emcp.kaleido.guru)** 是一个强大的 MCP 服务器管理平台，让您无需手动配置即可快速使用各种 MCP 服务器！

### 快速开始：

1. 🌐 访问 **[EMCP 平台](https://sit-emcp.kaleido.guru)**
2. 📝 注册并登录账号
3. 🎯 进入 **MCP 广场**，浏览所有可用的 MCP 服务器
4. 🔍 搜索或找到本服务器（`bach-weatherapi_com`）
5. 🎉 点击 **"安装 MCP"** 按钮
6. ✅ 完成！即可在您的应用中使用

### EMCP 平台优势：

- ✨ **零配置**：无需手动编辑配置文件
- 🎨 **可视化管理**：图形界面轻松管理所有 MCP 服务器
- 🔐 **安全可靠**：统一管理 API 密钥和认证信息
- 🚀 **一键安装**：MCP 广场提供丰富的服务器选择
- 📊 **使用统计**：实时查看服务调用情况

立即访问 **[EMCP 平台](https://sit-emcp.kaleido.guru)** 开始您的 MCP 之旅！


---

## 简介

这是一个 MCP 服务器，用于访问 Weatherapi Com API。

- **PyPI 包名**: `bach-weatherapi_com`
- **版本**: 1.0.0
- **传输协议**: stdio


## 安装

### 从 PyPI 安装:

```bash
pip install bach-weatherapi_com
```

### 从源码安装:

```bash
pip install -e .
```

## 运行

### 方式 1: 使用 uvx（推荐，无需安装）

```bash
# 运行（uvx 会自动安装并运行）
uvx --from bach-weatherapi_com bach_weatherapi_com

# 或指定版本
uvx --from bach-weatherapi_com@latest bach_weatherapi_com
```

### 方式 2: 直接运行（开发模式）

```bash
python server.py
```

### 方式 3: 安装后作为命令运行

```bash
# 安装
pip install bach-weatherapi_com

# 运行（命令名使用下划线）
bach_weatherapi_com
```

## 配置

### API 认证

此 API 需要认证。请设置环境变量:

```bash
export API_KEY="your_api_key_here"
```

### 环境变量

| 变量名 | 说明 | 必需 |
|--------|------|------|
| `API_KEY` | API 密钥 | 是 |
| `PORT` | 不适用 | 否 |
| `HOST` | 不适用 | 否 |



### 在 Cursor 中使用

编辑 Cursor MCP 配置文件 `~/.cursor/mcp.json`:


```json
{
  "mcpServers": {
    "bach-weatherapi_com": {
      "command": "uvx",
      "args": ["--from", "bach-weatherapi_com", "bach_weatherapi_com"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### 在 Claude Desktop 中使用

编辑 Claude Desktop 配置文件 `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "bach-weatherapi_com": {
      "command": "uvx",
      "args": ["--from", "bach-weatherapi_com", "bach_weatherapi_com"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```


## 可用工具

此服务器提供以下工具:


### `alerts_api`

Alerts API returns alerts and warnings issued by government agencies (USA, UK, Europe and Rest of the World) as an array if available for the location provided.

**端点**: `GET /alerts.json`


**参数**:

- `q` (string) *必需*: Example value: london



---


### `future_weather_api`

Future weather API method returns weather in a 3 hourly interval in future for a date between 14 days and 300 days from today in the future.

**端点**: `GET /future.json`


**参数**:

- `q` (string) *必需*: Query parameter based on which data is sent back. It could be following: Latitude and Longitude (Decimal degree) e.g: q=48.8567,2.3508 city name e.g.: q=Paris US zip e.g.: q=10001 UK postcode e.g: q=SW1 Canada postal code e.g: q=G2J metar: e.g: q=metar:EGLL iata:<3 digit airport code> e.g: q=iata:DXB auto:ip IP lookup e.g: q=auto:ip IP address (IPv4 and IPv6 supported) e.g: q=100.0.0.1

- `lang` (string): Returns 'condition:text' field in API in the desired language

- `dt` (string) *必需*: 'dt' should be between 14 days and 300 days from today in the future in yyyy-MM-dd format (i.e. dt=2023-01-01)



---


### `realtime_weather_api`

Current weather or realtime weather API method allows a user to get up to date current weather information in json and xml. The data is returned as a Current Object.

**端点**: `GET /current.json`


**参数**:

- `q` (string) *必需*: Query parameter based on which data is sent back. It could be following: Latitude and Longitude (Decimal degree) e.g: q=48.8567,2.3508 city name e.g.: q=Paris US zip e.g.: q=10001 UK postcode e.g: q=SW1 Canada postal code e.g: q=G2J metar: e.g: q=metar:EGLL iata:<3 digit airport code> e.g: q=iata:DXB auto:ip IP lookup e.g: q=auto:ip IP address (IPv4 and IPv6 supported) e.g: q=100.0.0.1



---


### `sports_api`

Sports API method allows a user to get listing of all upcoming sports events for football, cricket and golf in json.

**端点**: `GET /sports.json`


**参数**:

- `q` (string) *必需*: Example value: London



---


### `astronomy_api`

Astronomy API method allows a user to get up to date information for sunrise, sunset, moonrise, moonset, moon phase and illumination in json.

**端点**: `GET /astronomy.json`


**参数**:

- `q` (string) *必需*: Query parameter based on which data is sent back. It could be following: Latitude and Longitude (Decimal degree) e.g: q=48.8567,2.3508 city name e.g.: q=Paris US zip e.g.: q=10001 UK postcode e.g: q=SW1 Canada postal code e.g: q=G2J metar: e.g: q=metar:EGLL iata:<3 digit airport code> e.g: q=iata:DXB auto:ip IP lookup e.g: q=auto:ip IP address (IPv4 and IPv6 supported) e.g: q=100.0.0.1

- `dt` (string): Date



---


### `searchautocomplete_api`

Search or Autocomplete API returns matching cities and towns.

**端点**: `GET /search.json`


**参数**:

- `q` (string) *必需*: Query parameter based on which data is sent back. It could be following: Latitude and Longitude (Decimal degree) e.g: q=48.8567,2.3508 city name e.g.: q=Paris US zip e.g.: q=10001 UK postcode e.g: q=SW1 Canada postal code e.g: q=G2J metar: e.g: q=metar:EGLL iata:<3 digit airport code> e.g: q=iata:DXB auto:ip IP lookup e.g: q=auto:ip IP address (IPv4 and IPv6 supported) e.g: q=100.0.0.1



---


### `marine_weather_api`

Marine weather API returns upto next 7 day marine and sailing weather forecast and tide data for global marine/sea points.

**端点**: `GET /marine.json`


**参数**:

- `q` (string) *必需*: Query parameter based on which data is sent back. It could be following: Latitude and Longitude (Decimal degree) e.g: q=48.8567,2.3508 city name e.g.: q=Paris US zip e.g.: q=10001 UK postcode e.g: q=SW1 Canada postal code e.g: q=G2J metar: e.g: q=metar:EGLL iata:<3 digit airport code> e.g: q=iata:DXB auto:ip IP lookup e.g: q=auto:ip IP address (IPv4 and IPv6 supported) e.g: q=100.0.0.1

- `days` (number): Example value: 1

- `lang` (string): Example value: 



---


### `history_weather_api`

History weather API method returns historical weather for a date on or after 1st Jan, 2010 (depending upon subscription level) as json.

**端点**: `GET /history.json`


**参数**:

- `q` (string) *必需*: Query parameter based on which data is sent back. It could be following: Latitude and Longitude (Decimal degree) e.g: q=48.8567,2.3508 city name e.g.: q=Paris US zip e.g.: q=10001 UK postcode e.g: q=SW1 Canada postal code e.g: q=G2J metar: e.g: q=metar:EGLL iata:<3 digit airport code> e.g: q=iata:DXB auto:ip IP lookup e.g: q=auto:ip IP address (IPv4 and IPv6 supported) e.g: q=100.0.0.1

- `lang` (string): Returns 'condition:text' field in API in the desired language

- `hour` (number): Restricting history output to a specific hour in a given day.

- `dt` (string) *必需*: For history API 'dt' should be on or after 1st Jan, 2010 in yyyy-MM-dd format

- `end_dt` (string): Restrict date output for History API method. Should be on or after 1st Jan, 2010. Make sure end_dt is equal to or greater than 'dt'.



---


### `forecast_weather_api`

Forecast weather API method returns upto next 14 day weather forecast and weather alert as json. It contains astronomy data, day weather forecast and hourly interval weather information for a given city.

**端点**: `GET /forecast.json`


**参数**:

- `q` (string) *必需*: Query parameter based on which data is sent back. It could be following: Latitude and Longitude (Decimal degree) e.g: q=48.8567,2.3508 city name e.g.: q=Paris US zip e.g.: q=10001 UK postcode e.g: q=SW1 Canada postal code e.g: q=G2J metar: e.g: q=metar:EGLL iata:<3 digit airport code> e.g: q=iata:DXB auto:ip IP lookup e.g: q=auto:ip IP address (IPv4 and IPv6 supported) e.g: q=100.0.0.1

- `days` (number): Number of days of forecast required.

- `lang` (string): Returns 'condition:text' field in API in the desired language

- `dt` (string): If passing 'dt', it should be between today and next 10 day in yyyy-MM-dd format.



---


### `ip_lookup_api`

IP Lookup API method allows a user to get up to date information for an IP address in json.

**端点**: `GET /ip.json`


**参数**:

- `q` (string) *必需*: e.g: q=auto:ip IP address (IPv4 and IPv6 supported) e.g: q=100.0.0.1



---


### `time_zone_api`

Time Zone API method allows a user to get up to date time zone and local time information in json.

**端点**: `GET /timezone.json`


**参数**:

- `q` (string) *必需*: Query parameter based on which data is sent back. It could be following: Latitude and Longitude (Decimal degree) e.g: q=48.8567,2.3508 city name e.g.: q=Paris US zip e.g.: q=10001 UK postcode e.g: q=SW1 Canada postal code e.g: q=G2J metar: e.g: q=metar:EGLL iata:<3 digit airport code> e.g: q=iata:DXB auto:ip IP lookup e.g: q=auto:ip IP address (IPv4 and IPv6 supported) e.g: q=100.0.0.1



---



## 技术栈

- **传输协议**: stdio
- **HTTP 客户端**: httpx


## 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件。

## 开发

此服务器由 [API-to-MCP](https://github.com/BACH-AI-Tools/api-to-mcp) 工具生成。

版本: 1.0.0
