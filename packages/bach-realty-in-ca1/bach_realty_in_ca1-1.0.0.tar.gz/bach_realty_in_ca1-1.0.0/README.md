# Realty In Ca1 MCP Server

[English](./README_EN.md) | 简体中文 | [繁體中文](./README_ZH-TW.md)

用于访问 Realty In Ca1 API 的 MCP 服务器。

## 🚀 使用 EMCP 平台快速体验

**[EMCP](https://sit-emcp.kaleido.guru)** 是一个强大的 MCP 服务器管理平台，让您无需手动配置即可快速使用各种 MCP 服务器！

### 快速开始：

1. 🌐 访问 **[EMCP 平台](https://sit-emcp.kaleido.guru)**
2. 📝 注册并登录账号
3. 🎯 进入 **MCP 广场**，浏览所有可用的 MCP 服务器
4. 🔍 搜索或找到本服务器（`bach-realty_in_ca1`）
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

这是一个 MCP 服务器，用于访问 Realty In Ca1 API。

- **PyPI 包名**: `bach-realty_in_ca1`
- **版本**: 1.0.0
- **传输协议**: stdio


## 安装

### 从 PyPI 安装:

```bash
pip install bach-realty_in_ca1
```

### 从源码安装:

```bash
pip install -e .
```

## 运行

### 方式 1: 使用 uvx（推荐，无需安装）

```bash
# 运行（uvx 会自动安装并运行）
uvx --from bach-realty_in_ca1 bach_realty_in_ca1

# 或指定版本
uvx --from bach-realty_in_ca1@latest bach_realty_in_ca1
```

### 方式 2: 直接运行（开发模式）

```bash
python server.py
```

### 方式 3: 安装后作为命令运行

```bash
# 安装
pip install bach-realty_in_ca1

# 运行（命令名使用下划线）
bach_realty_in_ca1
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
    "bach-realty_in_ca1": {
      "command": "uvx",
      "args": ["--from", "bach-realty_in_ca1", "bach_realty_in_ca1"],
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
    "bach-realty_in_ca1": {
      "command": "uvx",
      "args": ["--from", "bach-realty_in_ca1", "bach_realty_in_ca1"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```


## 可用工具

此服务器提供以下工具:


### `propertiesget_statistics_deprecated`

Get statistic information of surround area by GEO location

**端点**: `GET /properties/get-statistics`


**参数**:

- `Longitude` (number) *必需*: Longitude of specific location

- `CultureId` (number): 1 - English|2 - French

- `Latitude` (number) *必需*: Latitude of specific location



---


### `propertiesget_scores`

Get scores of surround area by GEO location

**端点**: `GET /properties/get-scores`


**参数**:

- `lng` (number) *必需*: Longitude of specific location

- `locale` (string): en|fr

- `lat` (number) *必需*: Latitude of specific location



---


### `propertiesget_demographics`

Get demographics of surround area by GEO location

**端点**: `GET /properties/get-demographics`


**参数**:

- `lng` (number) *必需*: Longitude of specific location

- `lat` (number) *必需*: Latitude of specific location



---


### `propertiesdetail`

Get details information of specific property

**端点**: `GET /properties/detail`


**参数**:

- `ReferenceNumber` (string) *必需*: The value of MlsNumber field from .../list-commercial or .../list-residential endpoints

- `PropertyID` (string) *必需*: The value of Id field from .../list-commercial or .../list-residential endpoints

- `PreferedMeasurementUnit` (number): 1-Metric|2-Imperial

- `CultureId` (number): 1 - English|2 - French



---


### `propertieslist_by_mls`

List properties by listing ID or MLS number

**端点**: `GET /properties/list-by-mls`


**参数**:

- `ReferenceNumber` (string) *必需*: List ID or MLS number

- `CultureId` (number): 1 - English|2 - French



---


### `propertieslist_commercial`

List commercial properties both for lease and for sale

**端点**: `GET /properties/list-commercial`


**参数**:

- `LatitudeMax` (number) *必需*: Example value: 81.14747595814636

- `CurrentPage` (number): For paging purpose

- `LongitudeMin` (number) *必需*: South West longitude

- `LongitudeMax` (number) *必需*: North East longitude

- `LatitudeMin` (number) *必需*: South West latitude

- `RecordsPerPage` (number): Number items returned per request, max 50

- `BuildingSizeRange` (string): 0-5000:0-5,000 sqft|5001-10000:5,001-10,000 sqft|10001-15000:10,001-15,000 sqft|250001-0:Over 250,000 sqft. Ex : 0-5000

- `SortOrder` (string): A - ascending | D - descending

- `NumberOfDays` (number): Listed since

- `Keywords` (string): Get suitable values from …/keywords/list endpoint, separated by comma for multiple keywords, Ex : Inlaw suite,Income suite

- `BuildingTypeId` (number): 0-No Preference|1-House|2-Duplex|3-Triplex|5-Residential Commercial Mix|6-Mobile Home|12-Special Purpose|14-Other|16-Row / Townhouse|17-Apartment|19-Fourplex|20-Garden Home|26-Modular|27-Manufactured Home/Mobile|28-Commercial Apartment|29-Manufactured Home

- `BedRange` (string): 0-0:Any|1-1:1|1-0:1+|2-2:2|2-0:2+|3-3:3|3-0:3+|4-4:4|4-0:4+|5-5:5|5-0:5+

- `OpenHouseEndDate` (string): Format date as MM/dd/yyyy, ex : 03/31/2020

- `OpenHouseStartDate` (string): Format date as MM/dd/yyyy, ex : 03/20/2020

- `OpenHouse` (string): Example value: 

- `FarmTypeId` (number): 0-No Preference|1-Animal|2-Boarding|3-Cash Crop|4-Feed Lot|5-Nursery|6-Market Gardening|7-Hobby Farm|8-Vineyard|9-Orchard|10-Greenhouse|12-Mixed

- `CultureId` (number): 1 - English|2 - French

- `LandSizeRange` (string): 0-0:Any|1-0:1+ acres|2-0:2+ acres|5-0:5+ acres|10-0:10+ acres|50-0:50+ acres|100-0:100+ acres|200-0:200+ acres|300-0:300+ acres|400-0:400+ acres|500-0:500+ acres|1000-0:1000+ acres. Ex : 0-0

- `BathRange` (string): 0-0:Any|1-1:1|1-0:1+|2-2:2|2-0:2+|3-3:3|3-0:3+|4-4:4|4-0:4+|5-5:5|5-0:5+

- `SortBy` (number): 1-Price($)|6-Date|11-Virtual Tour|12-Open Houses|13-More Photos

- `PriceMax` (number): Filter by max price, applied when TransactionTypeId = 2

- `PriceMin` (number): Filter by min price, applied when TransactionTypeId = 2

- `UnitRange` (string): 0-0:Any|1-1:1|1-0:1+|2-2:2|2-0:2+|3-3:3|3-0:3+|4-4:4|4-0:4+|5-5:5|5-0:5+|….|9-0:9+

- `ZoningTypeGroupId` (number): 1-Agricultural|2-Commercial Mixed|3-Commercial Office|4-Commercial Retail|5-Industrial|6-Industrial-Heavy|7-Industrial-Light|8-Industrial-Medium|9-Institutional|10-Other|11-Recreational|12-Residential-High Density|13-Residential-Low Density|14-Residential - Medium Density

- `TransactionTypeId` (number): 2-For sale|3-For lease

- `ConstructionStyleId` (number): 0-No Preference|1-Attached|3-Detached|5-Semi-detached|7-Stacked|9-Link

- `PropertySearchTypeId` (number): 0-No Preference|1-Residential|2-Recreational|3-Condo/Strata|4-Agriculture|5-Parking|6-Vacant Land|8-Multi Family



---


### `propertieslist_residential`

List residential properties both for rent and for sale

**端点**: `GET /properties/list-residential`


**参数**:

- `LatitudeMax` (number) *必需*: Example value: 81.14747595814636

- `LatitudeMin` (number) *必需*: South West latitude

- `LongitudeMax` (number) *必需*: North East longitude

- `LongitudeMin` (number) *必需*: South West longitude

- `CurrentPage` (number): For paging purpose

- `RecordsPerPage` (number): Number items returned per request, max 50

- `SortOrder` (string): A - ascending | D - descending

- `SortBy` (number): 1-Price($)|6-Date|11-Virtual Tour|12-Open Houses|13-More Photos

- `CultureId` (number): 1 - English|2 - French

- `NumberOfDays` (number): Listed since

- `Keywords` (string): Get suitable values from …/keywords/list endpoint, separated by comma for multiple keywords, Ex : Inlaw suite,Income suite

- `BedRange` (string): 0-0:Any|1-1:1|1-0:1+|2-2:2|2-0:2+|3-3:3|3-0:3+|4-4:4|4-0:4+|5-5:5|5-0:5+

- `BathRange` (string): 0-0:Any|1-1:1|1-0:1+|2-2:2|2-0:2+|3-3:3|3-0:3+|4-4:4|4-0:4+|5-5:5|5-0:5+

- `LandSizeRange` (string): 0-0:Any|1-0:1+ acres|2-0:2+ acres|5-0:5+ acres|10-0:10+ acres|50-0:50+ acres|100-0:100+ acres|200-0:200+ acres|300-0:300+ acres|400-0:400+ acres|500-0:500+ acres|1000-0:1000+ acres. Ex : 0-0

- `BuildingSizeRange` (string): 0-5000:0-5,000 sqft|5001-10000:5,001-10,000 sqft|10001-15000:10,001-15,000 sqft|250001-0:Over 250,000 sqft Ex : 0-5000

- `UnitRange` (string): 0-0:Any|1-1:1|1-0:1+|2-2:2|2-0:2+|3-3:3|3-0:3+|4-4:4|4-0:4+|5-5:5|5-0:5+|….|9-0:9+

- `OpenHouseEndDate` (string): Format date as MM/dd/yyyy, ex : 03/31/2020

- `OpenHouseStartDate` (string): Format date as MM/dd/yyyy, ex : 03/20/2020

- `OpenHouse` (string): Example value: 

- `FarmTypeId` (number): 0-No Preference|1-Animal|2-Boarding|3-Cash Crop|4-Feed Lot|5-Nursery|6-Market Gardening|7-Hobby Farm|8-Vineyard|9-Orchard|10-Greenhouse|12-Mixed

- `PriceMin` (number): Filter by min price, applied when TransactionTypeId = 2

- `PriceMax` (number): Filter by max price, applied when TransactionTypeId = 2

- `RentMin` (string): Filter by min price, applied when TransactionTypeId = 3

- `RentMax` (number): Filter by max price, applied when TransactionTypeId = 3

- `BuildingTypeId` (number): 0-No Preference|1-House|2-Duplex|3-Triplex|5-Residential Commercial Mix|6-Mobile Home|12-Special Purpose|14-Other|16-Row / Townhouse|17-Apartment|19-Fourplex|20-Garden Home|26-Modular|27-Manufactured Home/Mobile|28-Commercial Apartment|29-Manufactured Home

- `ZoningTypeGroupId` (number): 1-Agricultural|2-Commercial Mixed|3-Commercial Office|4-Commercial Retail|5-Industrial|6-Industrial-Heavy|7-Industrial-Light|8-Industrial-Medium|9-Institutional|10-Other|11-Recreational|12-Residential-High Density|13-Residential-Low Density|14-Residential - Medium Density

- `TransactionTypeId` (number): 2-For sale|3-For rent

- `ConstructionStyleId` (number): 0-No Preference|1-Attached|3-Detached|5-Semi-detached|7-Stacked|9-Link

- `PropertySearchTypeId` (number): 0-No Preference|1-Residential|2-Recreational|3-Condo/Strata|4-Agriculture|5-Parking|6-Vacant Land|8-Multi Family

- `ParkingTypeId` (number): 1-Attached garage|2-Integrated garage|3-Detached garage|4-Garage|5-Carport|6-Underground|7-Indoor|8-Open|9-Covered|10-Parking pad|11-Paved Yard|35-Boat House|36-Concrete|37-Heated Garage



---


### `locationsv2auto_complete`

Get auto complete suggestions by city, ward, street name or an actual address

**端点**: `GET /locations/v2/auto-complete`


**参数**:

- `Query` (string) *必需*: City, ward, street name, etc... or an actual address

- `CultureId` (number): 1 - English|2 - French

- `IncludeLocations` (string): Example value: 



---


### `keywordslist`

List all supported tags/keywords for filtering

**端点**: `GET /keywords/list`



---


### `locationsauto_complete`

Get auto complete suggestions by city, ward, street name

**端点**: `GET /locations/auto-complete`


**参数**:

- `Area` (string) *必需*: City, ward, street name, etc...

- `CultureId` (number): 1 - English|2 - French



---


### `agentsdetail`

Get detail information of an agent

**端点**: `GET /agents/detail`


**参数**:

- `id` (number) *必需*: The value of IndividualID field returned in .../agents/list endpoint

- `CultureId` (number): 1 - English|2 - French



---


### `agentsget_listings`

Get properties listed by agent

**端点**: `GET /agents/get-listings`


**参数**:

- `CurrentPage` (number): For paging purpose

- `RecordsPerPage` (number): Number items returned per request, max 50

- `SortOrder` (string): A - ascending | D - descending

- `SortBy` (number): One of the following : 1-Price($)|6-Date|11-Virtual Tour|12-Open Houses|13-More Photos

- `CultureId` (number): 1 - English|2 - French

- `OrganizationId` (number) *必需*: The value of OrganizationID field returned in .../agents/list or .../agents/detail endpoint



---


### `agentslist`

List agents with options and filters

**端点**: `GET /agents/list`


**参数**:

- `CurrentPage` (number): For paging purpose

- `RecordsPerPage` (number): Number items returned per request, max 50

- `SortOrder` (string): A - ascending | D - descending

- `SortBy` (number): 11-No Preference|3-Last Name|2-First Name|8-City|9-Province

- `CultureId` (number): 1 - English|2 - French

- `FirstName` (string): Search by agent's first name

- `LastName` (string): Search by agent's last name

- `CompanyName` (string): Search by company name

- `City` (string): Search by city name

- `ProvinceIds` (number): One of the following : 1-Alberta|3-British Columbia|8-Manitoba|6-New Brunswick|10-Newfoundland & Labrador|11-Northwest Territories|5-Nova Scotia|9-Nunavut|2-Ontario|12-Prince Edward Island|4-Quebec|7-Saskatchewan|13-Yukon

- `Languages` (number): One of the following : 1-English|2-French|3-Chinese (Mandarin)|36-Chinese (Cantonese)|9-Punjabi |23-Hindi|13-Tagalog (Filipino)|11-Arabic |19-Russian|5-German |55-Aboriginal languages|50-Afrikaans|54-Albanian|22-American Sign Language (ASL)|56-Amharic|42-Armenian|106-Assyrian|57-Azeri|58-Bahasa Malaysia|39-Bangla|59-Belorussian|35-Bulgarian|40-Burmese|60-Catalan|105-Chaldean|16-Cree |61-Creole|25-Croatian|26-Czech|27-Danish|43-Dari|12-Dutch |62-Estonian|45-Farsi|51-Finnish|63-Flemish|64-Friesian

- `Specialties` (number): One of the following : 2-Residential Property Management|4-Residential Brokerage|8-Residential Development|10-Residential Valuation|12-Residential Financing|14-Residential Leasing|16-Residential Legal|18-Residential Relocation|17-Relocation|28-2nd Home|33-Age Restricted/Active Adult Community Properties|36-Agriculture Land|9-Appraisal|3-Business Brokerage|35-Condos|5-Consulting|7-Development Land|24-Farm/Ranch|32-Golf Community Properties|25-Hospitality|21-Industrial|11-Investment|29-Luxury Home

- `Designations` (number): One of the following : 1-Accredited Buyer Representative|2-Accredited Buyer Representative Manager|3-At Home With Diversity Certification|4-Accredited Land Consultant|5-Accredited Residential Manager® |6-Associate Reserve Planner|7-Certified Commercial Investment Member|8-Certified International Property Specialist|9-Certified Leasing Officer|10-Certified Manager of Condominiums|11-Certified Property Manager® |12-Certified Real Estate Specialist|13-Certified Real Estate Brokerage Manager|14-Coun

- `isCccMember` (string): Example value: 



---



## 技术栈

- **传输协议**: stdio
- **HTTP 客户端**: httpx


## 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件。

## 开发

此服务器由 [API-to-MCP](https://github.com/BACH-AI-Tools/api-to-mcp) 工具生成。

版本: 1.0.0
