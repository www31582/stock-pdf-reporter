#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A-Share Stock PDF Report Generator
Generate professional PDF reports for Chinese A-share stocks.
Ideal for quantitative traders, analysts, and investors.

Usage:
    python stock_report.py 600519 --days 60 --output report.pdf
    python stock_report.py 000001 --days 90

Powered by akshare (Sina Finance data)
Note: This is a fully local tool - no API key needed.
"""
import os, sys, argparse, warnings, time, traceback
from datetime import datetime, timedelta
warnings.filterwarnings('ignore')

try:
    import akshare as ak
except ImportError:
    sys.exit('pip install akshare')

try:
    from fpdf import FPDF
except ImportError:
    sys.exit('pip install fpdf2')

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as fm
from io import BytesIO

# Chinese font
CHINESE_FONTS = [
    'C:/Windows/Fonts/msyh.ttf', 'C:/Windows/Fonts/simhei.ttf',
    'C:/Windows/Fonts/simsun.ttc', 'C:/Windows/Fonts/yahei.ttf',
    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttf',
]

def find_font():
    for fp in CHINESE_FONTS:
        if os.path.exists(fp):
            try: return fp, fm.FontProperties(fname=fp)
            except: continue
    win = r'C:\Windows\Fonts'
    if os.path.exists(win):
        for f in os.listdir(win):
            if any(k in f.lower() for k in ['yahei','simhei','msyh','noto']):
                fp=os.path.join(win,f)
                try: return fp, fm.FontProperties(fname=fp)
                except: continue
    return None,None

FONT_PATH, FONT_PROP = find_font()
if FONT_PATH:
    try:
        fm.fontManager.addfont(FONT_PATH)
        matplotlib.rcParams['font.family'] = os.path.splitext(os.path.basename(FONT_PATH))[0]
    except: pass
    matplotlib.rcParams['axes.unicode_minus'] = False

def parse_symbol(sym):
    sym = sym.upper().replace('.SH','').replace('.SZ','').replace('．','').replace('。','')
    if sym.startswith('SH') or sym.startswith('SZ'):
        sym = sym[2:]
    prefixes = {
        '6': 'sh', '9': 'sh',
        '0': 'sz', '3': 'sz', '2': 'sz',
    }
    p = prefixes.get(sym[0], 'sh')
    return p + sym, sym

def get_stock_data(symbol, days=60):
    api_sym, code = parse_symbol(symbol)
    end = datetime.now().strftime('%Y%m%d')
    start = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
    
    for attempt in range(3):
        try:
            df = ak.stock_zh_a_daily(symbol=api_sym, start_date=start, end_date=end, adjust='qfq')
            if df is not None and not df.empty:
                df.index = pd.to_datetime(df['date'])
                df = df.sort_index()
                return df
        except Exception as e:
            if attempt < 2: time.sleep(2)
            else: raise ValueError(f'Failed for {symbol}: {e}')

def compute_indicators(df):
    df = df.copy()
    if len(df) < 5:
        raise ValueError(f'Need at least 5 data points, got {len(df)}')
    c = df['close'].values
    df['MA5'] = pd.Series(c).rolling(5).mean().values
    df['MA10'] = pd.Series(c).rolling(10).mean().values
    df['MA20'] = pd.Series(c).rolling(20).mean().values
    df['MA60'] = pd.Series(c).rolling(60).mean().values
    df['VOL_MA5'] = pd.Series(df['volume'].values).rolling(5).mean().values
    
    delta = pd.Series(c).diff()
    gain = delta.where(delta>0,0).rolling(14).mean()
    loss = (-delta.where(delta<0,0)).rolling(14).mean()
    rs = gain / loss.replace(0,np.nan)
    df['RSI'] = (100-100/(1+rs)).values
    
    ema12 = pd.Series(c).ewm(span=12).mean()
    ema26 = pd.Series(c).ewm(span=26).mean()
    dif = ema12 - ema26
    dea = dif.ewm(span=9).mean()
    df['MACD_DIF'] = dif.values; df['MACD_DEA'] = dea.values
    df['MACD_BAR'] = 2*(dif-dea).values
    
    sma20 = pd.Series(c).rolling(20).mean()
    std20 = pd.Series(c).rolling(20).std()
    df['BOLL_UP'] = (sma20+2*std20).values
    df['BOLL_MID'] = sma20.values
    df['BOLL_DN'] = (sma20-2*std20).values
    df['VOLATILITY'] = pd.Series(c).pct_change().rolling(20).std().values
    return df

def plot_charts(df, symbol):
    dates = pd.to_datetime(df.index)
    close = df['close'].values
    
    fig = plt.figure(figsize=(10, 11))
    fig.patch.set_facecolor('white')
    
    # Price panel
    ax1 = plt.subplot(3,1,(1,2))
    ax1.plot(dates, close, '#333333', lw=1.5, label='Close')
    if 'MA5' in df: ax1.plot(dates, df['MA5'].values, '#f39c12', lw=1, alpha=0.7, label='MA5')
    if 'MA10' in df: ax1.plot(dates, df['MA10'].values, '#3498db', lw=1, alpha=0.7, label='MA10')
    if 'MA20' in df: ax1.plot(dates, df['MA20'].values, '#9b59b6', lw=1, alpha=0.7, label='MA20')
    ax1.fill_between(dates, df['low'].values, df['high'].values, alpha=0.08, color='#666')
    ax1.set_ylabel('Price (CNY)', fontsize=10)
    ax1.set_title(f'{symbol} Stock Price & Technical Analysis', fontsize=13, fontweight='bold', pad=10)
    ax1.legend(loc='upper left', fontsize=8, ncol=4)
    ax1.grid(True, alpha=0.3)
    
    # Volume
    ax3 = plt.subplot(3,1,3)
    colors = ['#e74c3c' if df['close'].values[i]>=df['open'].values[i] else '#27ae60' for i in range(len(df))]
    ax3.bar(dates, df['volume'].values, color=colors, alpha=0.6, width=0.6)
    ax3.set_ylabel('Volume', fontsize=10)
    ax3.grid(True, alpha=0.3)
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.tight_layout()
    
    buf = BytesIO()
    fig.savefig(buf, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig); buf.seek(0)
    
    # MACD+RSI panel
    fig2 = plt.figure(figsize=(10, 5.5))
    fig2.patch.set_facecolor('white')
    ax4 = plt.subplot(2,1,1)
    ax4.plot(dates, df['MACD_DIF'].values, '#3498db', lw=1, label='DIF')
    ax4.plot(dates, df['MACD_DEA'].values, '#e74c3c', lw=1, label='DEA')
    bar_c = ['#e74c3c' if v>=0 else '#2ecc71' for v in df['MACD_BAR'].values]
    ax4.bar(dates, df['MACD_BAR'].values, color=bar_c, alpha=0.4, width=0.6)
    ax4.axhline(0, color='gray', lw=0.5)
    ax4.set_ylabel('MACD', fontsize=10); ax4.legend(loc='upper left', fontsize=8); ax4.grid(True, alpha=0.3)
    
    ax5 = plt.subplot(2,1,2)
    ax5.plot(dates, df['RSI'].values, '#9b59b6', lw=1.5)
    ax5.axhline(70, color='#e74c3c', ls='--', alpha=0.7, lw=0.8)
    ax5.axhline(30, color='#27ae60', ls='--', alpha=0.7, lw=0.8)
    ax5.axhline(50, color='gray', ls=':', alpha=0.4, lw=0.5)
    ax5.fill_between(dates, 30, 70, alpha=0.05, color='#2ecc71')
    ax5.set_ylabel('RSI', fontsize=10); ax5.set_ylim(0,100)
    ax5.legend(['RSI(14)'], loc='upper left', fontsize=8); ax5.grid(True, alpha=0.3)
    ax5.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.tight_layout()
    
    buf2 = BytesIO()
    fig2.savefig(buf2, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig2); buf2.seek(0)
    return buf, buf2

class PDF(FPDF):
    def __init__(self, symbol, font_path):
        super().__init__('P','mm','A4')
        self.symbol = symbol; self.font_path = font_path
        if font_path:
            self.add_font('CJK','',font_path,uni=True)
            self.add_font('CJK','B',font_path,uni=True)
    
    def _header(self):
        if self.page_no()>1:
            self.set_font('CJK','',7)
            self.set_text_color(130,130,130)
            self.cell(0,5,f'{self.symbol} - Stock Report',0,0,'L')
            self.cell(0,5,datetime.now().strftime('%Y-%m-%d'),0,1,'R')
            self.set_draw_color(200,200,200); self.line(10,12,200,12); self.ln(5)
    
    def _footer(self):
        self.set_y(-15)
        self.set_font('CJK','',7); self.set_text_color(150,150,150)
        self.cell(0,10,f'Page {self.page_no()} | Generated by AI Quant Tools | For reference only',0,0,'C')
    
    def cover(self, df):
        self.add_page()
        self.set_fill_color(41,128,185); self.rect(0,0,210,6,'F')
        self.ln(25)
        self.set_font('CJK','B',26); self.set_text_color(41,128,185)
        self.cell(0,12,f'{self.symbol}',0,1,'C')
        self.ln(3)
        self.set_draw_color(41,128,185); self.set_line_width(0.5)
        self.line(70,self.get_y(),140,self.get_y())
        self.ln(10)
        self.set_font('CJK','B',20); self.set_text_color(50,50,50)
        self.cell(0,10,'Technical Analysis Report',0,1,'C')
        self.set_font('CJK','',10); self.set_text_color(130,130,130)
        self.cell(0,8,'A-Share Stock Technical Analysis Report',0,1,'C')
        self.ln(15)
        
        latest = df.iloc[-1]; prev = df.iloc[-2]
        chg = (latest['close']-prev['close'])/prev['close']*100
        bx,by,bw,bh = 50,self.get_y(),110,45
        self.set_fill_color(240,248,255); self.set_draw_color(41,128,185)
        self.set_line_width(0.5); self.rect(bx,by,bw,bh,'DF')
        self.set_xy(bx,by+8)
        self.set_font('CJK','',10); self.set_text_color(80,80,80)
        self.cell(bw,7,f'Latest Close: {latest["close"]:.2f} CNY',0,1,'C')
        chg_c = (231,76,60) if chg>=0 else (39,174,96)
        self.set_text_color(*chg_c); self.set_font('CJK','B',14)
        self.cell(bw,9,f'Change: {chg:+.2f}%',0,1,'C')
        self.set_text_color(80,80,80); self.set_font('CJK','',10)
        self.cell(bw,7,f'Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}',0,1,'C')
        self.ln(35)
        self.set_font('CJK','',8); self.set_text_color(150,150,150)
        self.cell(0,5,'Disclaimer: This report is auto-generated for reference only. Not investment advice.',0,1,'C')
    
    def summary(self, df, ind):
        self.add_page()
        self.set_font('CJK','B',16); self.set_text_color(41,128,185)
        self.cell(0,10,'Key Statistics',0,1,'L')
        self.set_draw_color(41,128,185); self.line(10,self.get_y(),200,self.get_y()); self.ln(5)
        
        l = df.iloc[-1]; cp = (l['close'] - df.iloc[-2]['close'])/df.iloc[-2]['close']*100
        left = [
            ('Close',f'{l["close"]:.2f}'),('Change',f'{cp:+.2f}%'),
            ('High',f'{l["high"]:.2f}'),('Low',f'{l["low"]:.2f}'),
            ('Volume',f'{l["volume"]/10000:.0f}K'),('Amount',f'{l.get("amount",0)/1e8:.2f}B' if 'amount' in l else '--'),
        ]
        i = ind.iloc[-1]
        right = [
            ('MA5',f'{i["MA5"]:.2f}' if not pd.isna(i["MA5"]) else '--'),
            ('MA20',f'{i["MA20"]:.2f}' if not pd.isna(i["MA20"]) else '--'),
            ('RSI(14)',f'{i["RSI"]:.1f}' if not pd.isna(i["RSI"]) else '--'),
            ('MACD',f'{i["MACD_DIF"]:.2f}' if not pd.isna(i["MACD_DIF"]) else '--'),
            ('Volatility',f'{i["VOLATILITY"]*100:.2f}%' if not pd.isna(i["VOLATILITY"]) else '--'),
            ('Days',f'{len(df)}'),
        ]
        for j in range(6):
            self.set_font('CJK','',9); self.set_text_color(100,100,100)
            self.cell(35,7,f'  {left[j][0]}',0,0,'L')
            self.set_font('CJK','B',10); self.set_text_color(50,50,50)
            self.cell(55,7,f'{left[j][1]}',0,0,'L')
            self.set_font('CJK','',9); self.set_text_color(100,100,100)
            self.cell(35,7,f'  {right[j][0]}',0,0,'L')
            self.set_font('CJK','B',10); self.set_text_color(50,50,50)
            self.cell(0,7,f'{right[j][1]}',0,1,'L')
            if j<5:
                self.set_draw_color(235,235,235); self.line(15,self.get_y(),195,self.get_y())
        pr = (l['close']/df.iloc[0]['close']-1)*100
        self.ln(3)
        self.set_font('CJK','',9); self.set_text_color(100,100,100)
        self.cell(0,6,f'  Period Return: {pr:+.2f}%  |  Range High: {df["high"].max():.2f}  |  Range Low: {df["low"].min():.2f}',0,1)
    
    def add_chart(self, title, buf, h=95):
        self.add_page()
        self.set_font('CJK','B',12); self.set_text_color(41,128,185)
        self.cell(0,8,title,0,1,'L'); self.ln(2)
        buf.seek(0); self.image(buf,x=20,w=170,h=h)
    
    def analysis(self, df, ind):
        self.add_page()
        self.set_font('CJK','B',16); self.set_text_color(41,128,185)
        self.cell(0,10,'Technical Signal Analysis',0,1,'L')
        self.set_draw_color(41,128,185); self.line(10,self.get_y(),200,self.get_y()); self.ln(8)
        
        l = ind.iloc[-1]; cp = df['close'].values[-1]
        signals = []
        if not pd.isna(l.get('MA5',np.nan)) and not pd.isna(l.get('MA20',np.nan)):
            signals.append(('BULLISH' if l['MA5']>l['MA20'] else 'BEARISH','MA Trend',f'MA5={l["MA5"]:.2f}, MA20={l["MA20"]:.2f}'))
        if not pd.isna(l.get('RSI',np.nan)):
            if l['RSI']>70: signals.append(('WARNING','RSI Overbought',f'RSI({l["RSI"]:.1f}) > 70'))
            elif l['RSI']<30: signals.append(('BULLISH','RSI Oversold',f'RSI({l["RSI"]:.1f}) < 30'))
            else: signals.append(('NEUTRAL','RSI Neutral',f'RSI({l["RSI"]:.1f}) in 30-70 range'))
        if not pd.isna(l.get('MACD_DIF',np.nan)) and not pd.isna(l.get('MACD_DEA',np.nan)):
            if l['MACD_DIF']>l['MACD_DEA']:
                signals.append(('BULLISH','MACD Golden Cross','DIF > DEA, bullish momentum'))
            else:
                signals.append(('BEARISH','MACD Death Cross','DIF < DEA, bearish momentum'))
        if not pd.isna(l.get('BOLL_UP',np.nan)) and not pd.isna(l.get('BOLL_DN',np.nan)):
            if cp > l['BOLL_UP']: signals.append(('WARNING','Bollinger Top',f'Price({cp:.2f}) touches upper band({l["BOLL_UP"]:.2f})'))
            elif cp < l['BOLL_DN']: signals.append(('BULLISH','Bollinger Bottom',f'Price({cp:.2f}) touches lower band({l["BOLL_DN"]:.2f})'))
            else: signals.append(('NEUTRAL','Bollinger Mid','Price within Bollinger bands'))
        
        for s in signals:
            emoji = {'BULLISH':'+','BEARISH':'-','WARNING':'!','NEUTRAL':'~'}.get(s[0],'?')
            self.set_font('CJK','B',11); self.set_text_color(50,50,50)
            self.cell(0,7,f'{emoji} {s[1]}',0,1)
            self.set_font('CJK','',9); self.set_text_color(110,110,110)
            self.cell(0,6,f'   {s[2]}',0,1); self.ln(2)
        
        self.ln(3); self.set_draw_color(200,200,200); self.line(10,self.get_y(),200,self.get_y()); self.ln(6)
        bullish = sum(1 for s in signals if s[0]=='BULLISH')
        bearish = sum(1 for s in signals if s[0]=='BEARISH')
        self.set_font('CJK','B',12)
        if bullish>bearish: self.set_text_color(39,174,96); self.cell(0,8,'Overall: BULLISH',0,1,'C')
        elif bearish>bullish: self.set_text_color(231,76,60); self.cell(0,8,'Overall: BEARISH',0,1,'C')
        else: self.set_text_color(52,152,219); self.cell(0,8,'Overall: NEUTRAL',0,1,'C')

def main():
    parser = argparse.ArgumentParser(description='A-Share Stock PDF Report Generator')
    parser.add_argument('symbol', help='Stock code, e.g. 600519, 000001, 300750')
    parser.add_argument('--days', type=int, default=60, help='Lookback days (default: 60)')
    parser.add_argument('--output','-o', default=None, help='Output PDF path')
    args = parser.parse_args()
    
    sym = args.symbol; days = args.days
    out = args.output or f'{sym}_report.pdf'
    
    print(f'Fetching {sym} data (past {days} days)...')
    df = get_stock_data(sym, days)
    print(f'Got {len(df)} records')
    
    ind = compute_indicators(df)
    print('Indicators computed')
    
    l = df.iloc[-1]; pr = (l['close']-df.iloc[-2]['close'])/df.iloc[-2]['close']*100
    print(f'Latest: {l["close"]:.2f} ({pr:+.2f}%)')
    
    print('Generating charts...')
    chart1, chart2 = plot_charts(ind, sym)
    
    print('Generating PDF...')
    pdf = PDF(sym, FONT_PATH)
    pdf.cover(df)
    pdf.summary(df, ind)
    pdf.add_chart('Price & Volume', chart1, h=105)
    pdf.add_chart('MACD & RSI Indicators', chart2, h=65)
    pdf.analysis(df, ind)
    pdf.output(out)
    print(f'Report saved: {os.path.abspath(out)}')

if __name__=='__main__':
    main()