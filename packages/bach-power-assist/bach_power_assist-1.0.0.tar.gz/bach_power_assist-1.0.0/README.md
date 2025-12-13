# Power Assist MCP Server

[English](./README_EN.md) | 简体中文 | [繁體中文](./README_ZH-TW.md)

用于访问 Power Assist API 的 MCP 服务器。

## 🚀 使用 EMCP 平台快速体验

**[EMCP](https://sit-emcp.kaleido.guru)** 是一个强大的 MCP 服务器管理平台，让您无需手动配置即可快速使用各种 MCP 服务器！

### 快速开始：

1. 🌐 访问 **[EMCP 平台](https://sit-emcp.kaleido.guru)**
2. 📝 注册并登录账号
3. 🎯 进入 **MCP 广场**，浏览所有可用的 MCP 服务器
4. 🔍 搜索或找到本服务器（`bach-power_assist`）
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

这是一个 MCP 服务器，用于访问 Power Assist API。

- **PyPI 包名**: `bach-power_assist`
- **版本**: 1.0.0
- **传输协议**: stdio


## 安装

### 从 PyPI 安装:

```bash
pip install bach-power_assist
```

### 从源码安装:

```bash
pip install -e .
```

## 运行

### 方式 1: 使用 uvx（推荐，无需安装）

```bash
# 运行（uvx 会自动安装并运行）
uvx --from bach-power_assist bach_power_assist

# 或指定版本
uvx --from bach-power_assist@latest bach_power_assist
```

### 方式 2: 直接运行（开发模式）

```bash
python server.py
```

### 方式 3: 安装后作为命令运行

```bash
# 安装
pip install bach-power_assist

# 运行（命令名使用下划线）
bach_power_assist
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
    "bach-power_assist": {
      "command": "uvx",
      "args": ["--from", "bach-power_assist", "bach_power_assist"],
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
    "bach-power_assist": {
      "command": "uvx",
      "args": ["--from", "bach-power_assist", "bach_power_assist"],
      "env": {
        "API_KEY": "your_api_key_here"
      }
    }
  }
}
```


## 可用工具

此服务器提供以下工具:


### `regex`

Validates that a String against a supplied RegEx pattern. Include the leading and trailing '/' in your RegEx pattern and optionally append flags.

**端点**: `POST /api/validate/regex`



---


### `median`

Calculates the median from an Array of numbers. Strings that can be converted to numbers are allowed, but formatting such as commas are NOT supported.

**端点**: `POST /api/math/median`



---


### `countinstances`

Get the number of occurrences of a substring within a string.

**端点**: `POST /api/string/countInstances`



---


### `regexreplace`

Find and replace within a String using a RegEx pattern. Include the leading and trailing '/' in your pattern and optionally append flags. If the /g flag is used, it will replace all occurrences. Use the /i flag to make the search ignore case.

**端点**: `POST /api/string/regexReplace`



---


### `every`

This action returns True if all of the items in an array match a specified condition; otherwise, it returns False.

**端点**: `POST /api/array/every`



---


### `words`

Split string by delimiter (String or RegEx pattern). The action splits by whitespace by default. If using RegEx, include the leading and trailing '/' in your pattern and optionally append flags.

**端点**: `POST /api/string/words`



---


### `isarray`

Validate whether a supplied Value is an Array.

**端点**: `POST /api/types/isArray`



---


### `reverse`

Reverse the order of an Array of any data type and returns it.

**端点**: `POST /api/array/reverse`



---


### `findfirst`

Accepts an array of any data type, including objects. Returns the first item that matches the specified condition. If no item matches the condition, Null is returned. Use the 'this' keyword for the propertyName when the array is of a simple data type, such as string, integer, or boolean.

**端点**: `POST /api/array/findFirst`



---


### `slugify`

Transform text into an ASCII slug which can be used in safely in URLs. Replaces whitespaces, accentuated, and special characters with a dash. Many non-ASCII characters are transformed to similar versions in the ASCII character set.

**端点**: `POST /api/string/slugify`



---


### `trimend`

Trim whitespace (by default) or specified characters from the end of a string.

**端点**: `POST /api/string/trimEnd`



---


### `replaceall`

In a string, find and replace all instances of a substring. This action is case sensitive. Does not accept RegEx. To use RegEx and control case sensitivity, see the \

**端点**: `POST /api/string/replaceAll`



---


### `trimstart`

Trim whitespace (the default) or specified characters only at the start of a string.

**端点**: `POST /api/string/trimStart`



---


### `trim`

Trims leading and trailing whitespace (the default) or specified characters from a string.

**端点**: `POST /api/string/trim`



---


### `escapehtml`

Convert HTML special characters, like \u003c and \u003e, to their entity equivalents (for example \u0026lt; and \u0026gt;). This action supports cent, yen, euro, pound, lt, gt, copy, reg, quote, amp, and apos.

**端点**: `POST /api/string/escapeHtml`



---


### `wordcount`

Count the words in a String by a delimiter (String or RegEx pattern). The delimiter is whitespace by default. If using RegEx, include the leading and trailing '/' in your pattern and optionally append flags.

**端点**: `POST /api/string/wordCount`



---


### `prepend`

Given an Array and a Value, this action adds the Value as the first item in the Array and returns the resulting Array. If an Array is supplied as the Value, a flat array will be returned with each of the items prepended.

**端点**: `POST /api/array/prepend`



---


### `groupby`

Group an Array of items. Accepts an Array of any data type. Returns a \

**端点**: `POST /api/array/groupBy`



---


### `filter`

Filter an Array of any data type (except nested Arrays) based on a specified condition.  If the array consists of a simple data type such as String, Integer, or Boolean, use the 'this' keyword in the propertyName parameter. If the array consists of Objects, specify the property to compare against in the propertyName parameter.

**端点**: `POST /api/array/filter`



---


### `sort`

Perform a simple sort on an Array of any data type and returns it. If an empty Array is provided, it will be returned.

**端点**: `POST /api/array/sort`



---


### `floor`

Rounds a number down to the nearest integer. Supports numbers passed in as strings, but does NOT support commas or other formatting in number strings. If an integer is passed in, it will be returned unchanged.

**端点**: `POST /api/math/floor`



---


### `ceil`

Rounds a number up to the nearest integer. Supports numbers passed in as strings, but does NOT support commas or other formatting in number strings. If an integer is passed in, it will be returned unchanged.

**端点**: `POST /api/math/ceil`



---


### `random`

Generates a pseudo-random number between the minimum of 0 and the specified maximum (maximum must be 1, 10, 100, 1000, 10000).

**端点**: `POST /api/math/random`



---


### `average`

Calculates the average (mean) from an Array of numbers. Strings that can be converted to numbers are allowed, but formatting such as commas are NOT supported.

**端点**: `POST /api/math/average`



---


### `mode`

Calculates the mode (the number that occurs most often) from an Array of numbers. Strings that can be converted to numbers are allowed, but formatting such as commas are NOT supported. If multiple instances of the same number are passed in separately,  one as a string and one as a number, they will be counted as instances of the same number.  If no numbers occur more than once, the last number in the array will be returned.

**端点**: `POST /api/math/mode`



---


### `round`

Rounds a number to the nearest integer. If an integer is passed in, it will be returned unchanged. Supports numbers passed in as strings, but does NOT support commas or other formatting in number strings.

**端点**: `POST /api/math/round`



---


### `objecttoarray`

Accepts an Object and returns an Array based on the Object's keys, allowing looping on the Object. If Null or an empty object is passed in, an empty Array will be returned.

**端点**: `POST /api/array/objectToArray`



---


### `clean_whitespace`

Trim and replace multiple spaces with a single space. (This includes whitespace characters like \  and \ .) For cleaning special characters out of a string for a URL, use Slugify.

**端点**: `POST /api/string/clean`



---


### `cleandiacritics`

Replace all diacritic characters (letters with glyphs) in a string with the closest ASCII equivalents.

**端点**: `POST /api/string/cleanDiacritics`



---


### `striphtml`

Remove all HTML and XML tags from a string.

**端点**: `POST /api/string/stripHtml`



---


### `unescapehtml`

Convert entity characters (for example, \u0026lt;) to HTML equivalents (for example, \u003c). This action supports cent, yen, euro, pound, lt, gt, copy, reg, quote, amp, apos, and nbsp.

**端点**: `POST /api/string/unescapeHtml`



---


### `capitalize`

Sets the first character of the string to upper case, and all subsequent characters to lower case.

**端点**: `POST /api/string/capitalize`



---


### `chop`

Chop the string into an Array based on an interval, which defines the size of the pieces.

**端点**: `POST /api/string/chop`



---


### `isnullorempty`

Check if value is null or empty. Can be used for Strings, Arrays, or Objects.

**端点**: `POST /api/types/isNullOrEmpty`



---


### `sortbyproperty`

Accepts an Array of Objects and sorts it by the object Property specified. If any objects lack the specified property, it will still perform the sort. Optionally accepts the parameter 'descending'. If left out, it will default to ascending. If an empty Array is provided, it will be returned.

**端点**: `POST /api/array/sortByProperty`



---


### `isstring`

Validates whether a supplied value is of type String.

**端点**: `POST /api/types/isString`



---


### `isobject`

Validate whether a supplied Value is an Object. Empty Objects will evaluate to True. Arrays and other data types will evaluate to False.

**端点**: `POST /api/types/isObject`



---


### `isnumber`

Validates that a value is a Number. Numbers inside strings, such as \

**端点**: `POST /api/types/isNumber`



---


### `removefirst`

Accepts an Array of any data type. Returns an Array with the first Item that matches the specified condition removed. If no Item matches the condition, the entire Array is returned.

**端点**: `POST /api/array/removeFirst`



---


### `any`

This action returns True if any of the items in an array match a specified condition; otherwise, it returns False. If the array consists of a simple data type such as String, Integer, or Boolean, use the 'this' keyword in the propertyName parameter. If the array consists of Objects, specify the property to compare against in the propertyName parameter.

**端点**: `POST /api/array/any`



---


### `email`

Validates that a String matches the common email format. Does NOT send an email. Returns True if the validation passes; otherwise, False.

**端点**: `POST /api/validate/email`



---



## 技术栈

- **传输协议**: stdio
- **HTTP 客户端**: httpx


## 许可证

MIT License - 详见 [LICENSE](./LICENSE) 文件。

## 开发

此服务器由 [API-to-MCP](https://github.com/BACH-AI-Tools/api-to-mcp) 工具生成。

版本: 1.0.0
