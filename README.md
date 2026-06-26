# Stock PDF Reporter

> Generate professional PDF technical analysis reports for Chinese A-Share stocks with one command.

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/aiquants)
[![GitHub Sponsors](https://img.shields.io/badge/GitHub_Sponsors-30363D?style=for-the-badge&logo=github-sponsors&logoColor=#white)](https://github.com/sponsors/www31582)
[![PyPI](https://img.shields.io/badge/PyPI-3775A9?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/akshare-pdf-reporter/)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## ✨ Features

- **Real-time data**: Automatic A-share stock data via Sina Finance
- **Technical indicators**: MA5/10/20/60, MACD, RSI(14), Bollinger Bands, Volatility
- **Professional charts**: Price trend + volume + MACD + RSI in one report
- **Auto analysis**: Generates technical signals (Golden/Death Cross, Overbought/Oversold)
- **Beautiful PDF**: 5-page professional report with cover page
- **No API key**: Fully local, works out of the box
- **Chinese support**: Full Chinese font support

## 📦 Installation

```bash
pip install akshare-pdf-reporter
```

Or install dependencies manually:
```bash
pip install akshare fpdf2 matplotlib pandas numpy
```

## 🚀 Usage

```bash
# Quick report for Maotai (600519)
python stock_report.py 600519

# Specify days and output
python stock_report.py 000001 --days 120 -o my_report.pdf

# More stocks
python stock_report.py 601318   # China Ping An
python stock_report.py 300750   # CATL
python stock_report.py 000858   # Wuliangye
python stock_report.py 600036   # China Merchants Bank
```

## 📄 Report Sample

Download a sample: [test_report.pdf](https://github.com/www31582/stock-pdf-reporter/releases/download/v1.0.0/test_report.pdf)

The PDF includes:
1. **Cover Page** - Stock name, price, daily change
2. **Key Statistics** - Price levels, MA values, RSI, MACD, volatility
3. **Price Chart** - Close price + MA5/10/20 + volume bars
4. **Technical Indicators** - MACD + RSI combo chart
5. **Signal Analysis** - Auto-detected technical signals + overall rating

## 🤝 Support

If you find this tool useful, consider supporting development:

- ☕ [Buy Me a Coffee](https://buymeacoffee.com/aiquants) - One-time support
- ⭐ Star the repo - It helps others discover the tool
- 📢 Share with friends who trade A-shares

## 📝 License

MIT License - Free for commercial and personal use.

## ⚠️ Disclaimer

This tool is for educational and reference purposes only. Not financial advice. Trading stocks involves risk.