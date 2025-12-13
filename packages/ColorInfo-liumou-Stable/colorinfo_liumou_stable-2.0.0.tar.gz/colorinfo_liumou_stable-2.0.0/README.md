# ColorInfo 🌈

一个功能强大的 Python 彩色日志工具，支持结构化日志记录

## 📊 项目状态

[![PyPI 版本](https://img.shields.io/pypi/v/ColorInfo_liumou_Stable.svg?color=blue)](https://pypi.org/project/ColorInfo_liumou_Stable/)
[![PyPI 下载量](https://img.shields.io/pypi/dm/ColorInfo_liumou_Stable.svg?color=green)](https://pypi.org/project/ColorInfo_liumou_Stable/)
[![Python 版本](https://img.shields.io/pypi/pyversions/ColorInfo_liumou_Stable.svg?color=orange)](https://pypi.org/project/ColorInfo_liumou_Stable/)
[![许可证](https://img.shields.io/pypi/l/ColorInfo_liumou_Stable.svg?color=red)](https://gitee.com/liumou_site/ColorInfo/blob/master/LICENSE)
[![代码大小](https://img.shields.io/github/languages/code-size/liumou_site/ColorInfo.svg?color=purple)](https://gitee.com/liumou_site/ColorInfo)
[![最后提交](https://img.shields.io/github/last-commit/liumou_site/ColorInfo.svg?color=yellow)](https://gitee.com/liumou_site/ColorInfo/commits/master)

## 🎯 核心特性

![结构化日志](https://img.shields.io/badge/结构化日志-支持-brightgreen.svg)
![彩色输出](https://img.shields.io/badge/彩色输出-支持-ff69b4.svg)
![JSON格式](https://img.shields.io/badge/JSON格式-支持-blue.svg)
![Go Zap风格](https://img.shields.io/badge/Go%20Zap风格-支持-orange.svg)
![中文文档](https://img.shields.io/badge/中文文档-完整-red.svg)

## ✨ 主要特性

* 🎨 **彩色输出** - 终端彩色日志显示
* 📝 **结构化日志** - 类似 Go Zap 的字段式日志记录
* 🌐 **多格式支持** - 纯文本和 JSON 格式输出
* 🔧 **使用简单** - 简洁的 API 设计
* 🎯 **中文注释** - 完整的中文文档和注释
* 🐍 **版本兼容** - 支持全部 Python3 版本 (>=3.0)
* 📊 **参数灵活** - 支持传入多个参数，无需格式化
* 🔍 **智能定位** - 自动显示调用文件和行号信息

## 📦 安装教程

### 快速安装

```shell
pip3 install --upgrade ColorInfo_liumou_Stable
```

### 开发安装

```shell
git clone https://gitee.com/liumou_site/ColorInfo.git
cd ColorInfo
pip3 install -e .
```

### 验证安装

```python
# 测试安装是否成功
from ColorInfo_liumou_Stable import ColorLogger, sugar, JSONStructuredLogger
print("✅ ColorInfo 安装成功！")
```

## 🚀 快速开始

### 基础使用

```python
from ColorInfo_liumou_Stable import ColorLogger, logger

# 创建日志记录器
log = ColorLogger(txt=True, fileinfo=True, basename=False)

# 记录不同级别的日志
log.info('信息消息')
log.error('错误消息')
log.debug('调试消息')
log.warning('警告消息')
```

### 结构化日志（类似 Go Zap）

```python
from ColorInfo_liumou_Stable import ColorLogger, sugar, JSONStructuredLogger

# 创建结构化日志记录器
structured_log = sugar(ColorLogger(txt=True, fileinfo=True, basename=False))

# 字段式日志记录
structured_log.info('用户登录', user_id=12345, username='admin', ip='192.168.1.1')
structured_log.error('数据库连接失败', error='ConnectionRefused', host='localhost', port=3306)
structured_log.debug('API 调用', endpoint='/api/users', method='GET', status=200, duration=45.2)
structured_log.warning('内存使用率高', usage_percent=85.3, threshold=80, service='web-server')

# JSON 格式结构化日志
json_log = JSONStructuredLogger(ColorLogger(txt=True, fileinfo=True, basename=False))
json_log.info('订单处理', order_id='ORD-2024-001', amount=99.99, customer='张三')
```

## 📋 完整示例

### 传统日志方式

```python
from ColorInfo_liumou_Stable import ColorLogger, logger

def demos():
    log = ColorLogger(txt=True, fileinfo=True, basename=False)
    log.info(msg='1', x="23")
    log.error('2', '22', '222')
    log.debug('3', '21')
    log.warning('4', '20', 22)

class Demo:
    def __init__(self):
        self.logger = logger
        self.logger.info("初始化")

    def de(self):
        self.logger.debug("de1")
        logger.info("de2")
        logger.warning("de3")
        logger.error("de4")

if __name__ == "__main__":
    d = Demo()
    d.de()
    demos()
```

### 结构化日志改进

```python
from ColorInfo_liumou_Stable import ColorLogger, sugar

def improved_logging():
    # 使用结构化日志改进传统调用
    structured_log = sugar(ColorLogger(txt=True, fileinfo=True, basename=False))
    
    # 更清晰的字段表达
    structured_log.info('1', x="23")
    
    # 为参数添加明确的字段名
    structured_log.error('2', code='22', message='222')
    
    # 为调试信息添加上下文
    structured_log.debug('3', value='21')
    
    # 为警告参数添加描述性字段名
    structured_log.warning('4', min_value='20', max_value=22)
```

## 🎨 输出效果

### 控制台输出

日志会在控制台显示彩色输出，包含时间、文件名、行号、类名、函数名和日志内容。

### 文件输出

同时支持将日志写入文件，包含完整的结构化信息：

```bash
2025-12-07 14:38:48 demo.py line: 17 Function: demos INFO : 1 x=23
2025-12-07 14:38:48 demo.py line: 18 Function: demos ERROR : 2 22 222
2025-12-07 14:38:48 structured.py line: 93 Class: StructuredLogger Function: info INFO : 用户登录 user_id=12345 username=admin ip=192.168.1.1
2025-12-07 14:38:48 structured.py line: 115 Class: StructuredLogger Function: error ERROR : 数据库连接失败 error=ConnectionRefused host=localhost port=3306
```

### JSON 格式输出

```json
{"message":"订单处理","timestamp":"2025-12-07T14:38:48.928281","fields":{"order_id":"ORD-2024-001","amount":99.99,"customer":"张三"}}
{"message":"支付失败","timestamp":"2025-12-07T14:38:48.928571","fields":{"error_code":"PAY_001","transaction_id":"TXN-123456"}}
```

## 🛠️ API 参考

### ColorLogger 类

* `info(msg, *args)` - 记录信息级别日志

* `error(msg, *args)` - 记录错误级别日志  
* `debug(msg, *args)` - 记录调试级别日志
* `warning(msg, *args)` - 记录警告级别日志

### 结构化日志类

* `StructuredLogger(base_logger)` - 字段式结构化日志

* `JSONStructuredLogger(base_logger)` - JSON 格式结构化日志
* `sugar(logger)` - 将普通日志转换为结构化日志

## 🔗 项目链接

* **PyPI 主页**: [https://pypi.org/project/ColorInfo_liumou_Stable/](https://pypi.org/project/ColorInfo_liumou_Stable/)
* **Gitee 仓库**: [https://gitee.com/liumou_site/ColorInfo.git](https://gitee.com/liumou_site/ColorInfo.git)

## 📸 效果截图

请在 Gitee 项目主页查看详细的彩色日志效果图片

![logg.png](./Demo.png)

## 📄 许可证

本项目采用开源许可证，详见项目仓库

---

**ColorInfo** - 让 Python 日志记录变得简单而强大！🚀
