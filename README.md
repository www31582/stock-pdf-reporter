# A-Share Stock PDF Report Generator

一个专业的 A股技术分析 PDF 报告生成工具，使用 Python 和 akshare 数据源。

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/yourusername)
[![ko-fi](https://img.shields.io/badge/Ko--fi-F16061?style=flat&logo=ko-fi&logoColor=white)](https://ko-fi.com/yourusername)

## Features

- ✅ 自动获取 A 股实时数据（前复权）
- 📊 专业级技术分析图表（价格走势、成交量、MACD、RSI）
- 📈 核心技术指标计算（MA5/10/20/60、布林带、MACD、RSI）
- 📄 生成精美的 PDF 分析报告
- 🎯 自动技术信号分析（均线、MACD 金叉死叉、超买超卖）
- 🇨🇳 中文界面，完美支持中文字体

## Installation

```bash
pip install akshare fpdf2 matplotlib pandas numpy
```

## Usage

```bash
# 基础用法 - 生成贵州茅台60天报告
python stock_report.py 600519.SH

# 指定天数
python stock_report.py 000001.SZ --days 90

# 指定输出文件
python stock_report.py 300750.SZ --days 120 -o my_report.pdf

# 更多股票
python stock_report.py 601318.SH  # 中国平安
python stock_report.py 000858.SZ  # 五粮液
python stock_report.py 002415.SZ  # 海康威视
python stock_report.py 600036.SH  # 招商银行
```

## Output Example

生成的 PDF 报告包含：
1. **封面** - 股票名称、代码、最新价格、涨跌幅
2. **核心指标概览** - 价格统计、均线、RSI、MACD、波动率
3. **价格走势图** - 收盘价曲线 + MA5/10/20 + 成交量柱状图
4. **技术指标图** - MACD + RSI 组合图表
5. **技术信号分析** - 均线排列、超买超卖、MACD 金叉死叉、布林带、量价分析
6. **综合判断** - 多空信号汇总

## Sample Report

运行后即可看到类似如下输出：
```
🚀 正在获取 600519.SH 过去 60 天的数据...
✅ 获取到 42 条数据
✅ 技术指标计算完成
📊 生成图表...
📄 生成PDF报告...
✅ 报告已生成: D:/projects/600519_SH_report.pdf
```

## License

MIT

## Support

如果这个工具对你有帮助，欢迎请我喝杯咖啡 ☕
