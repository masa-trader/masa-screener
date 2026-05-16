import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# --- 網頁前端配置 ---
st.set_page_config(page_title="Masa 動能自訂 KDJ+RSI 篩選器", layout="centered")
st.title("🚀 Masa 動能自訂 KDJ+RSI 終極篩選器")
st.markdown("請在下方輸入你想掃描的股票代號，系統將自動分析**今日**是否符合進出場條件。")

# --- 預設自選股池 ---
default_tickers = "NVDA, TSLA, AAPL, AMD, MSFT, AMZN, META, GOOGL, NFLX, TSM, BABA"

# --- 使用者互動輸入框 ---
user_input = st.text_area("👉 輸入股票代號（多檔請用「逗號 ,」或「換行」分隔）：", value=default_tickers, height=150)

# --- 核心策略運算邏輯 ---
def scan_kdj_rsi_strategy(ticker):
    try:
        # 下載近 4 個月的日 K 資料，確保數據足夠計算
        df = yf.download(ticker, period='4mo', progress=False)
        if df.empty or len(df) < 30:
            return None
        
        # 清理 yfinance 新版多重索引架構
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
        
        close = df['Close'].astype(float)
        high = df['High'].astype(float)
        low = df['Low'].astype(float)
        volume = df['Volume'].astype(float)
        
        # 1. 運算 RSI 24 (Wilder RMA 算法)
        delta = close.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.ewm(alpha=1/24, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1/24, adjust=False).mean()
        rs = avg_gain / avg_loss
        rsi24 = 100 - (100 / (1 + rs))
        
        # 2. 運算中式標準 KDJ (9, 3, 3) 遞迴算法
        low_9 = low.rolling(window=9).min()
        high_9 = high.rolling(window=9).max()
        rsv = (close - low_9) / (high_9 - low_9) * 100
        rsv = rsv.fillna(50)
        
        k_values = [50.0]
        d_values = [50.0]
        for i in range(1, len(df)):
            k_next = (2 * k_values[-1] + rsv.iloc[i]) / 3
            d_next = (2 * d_values[-1] + k_next) / 3
            k_values.append(k_next)
            d_values.append(d_next)
            
        df['J'] = 3 * pd.Series(k_values, index=df.index) - 2 * pd.Series(d_values, index=df.index)
        df['RSI24'] = rsi24
        
        # 3. 核心結合值與量縮判定
        combo = df['J'] + df['RSI24']
        current_combo = combo.iloc[-1]
        vol_cond = volume.iloc[-1] < volume.iloc[-2]
        
        # 4. 交易狀態判定分流
        status = "觀望"
        if ((current_combo > 100 and current_combo <= 170) or current_combo < 30) and vol_cond:
            status = "🔥 做多買進"
        elif (current_combo > 170) and vol_cond:
            status = "🚨 做空賣出"
        elif (current_combo < 100 and current_combo >= 30) and vol_cond:
            status = "⚠️ 多單出場"
            
        return {
            "股票代號": ticker.upper().strip(),
            "當日 J+RSI24": round(current_combo, 2),
            "是否量縮": "是" if vol_cond else "否",
            "今日訊號": status
        }
    except:
        return None

# --- 網頁按鈕事件 ---
if st.button("🚀 開始全自動掃描", type="primary"):
    # 解析輸入內容並清洗字串
    raw_tickers = user_input.replace("\n", ",").split(",")
    tickers = [t.strip().upper() for t in raw_tickers if t.strip()]
    
    if not tickers:
        st.warning("請輸入至少一檔股票代號！")
    else:
        with st.spinner("正在抓取最新市場數據並計算中，請稍候..."):
            results = []
            for t in tickers:
                res = scan_kdj_rsi_strategy(t)
                if res:
                    results.append(res)
            
            # --- 渲染前端表格 ---
            if results:
                result_df = pd.DataFrame(results)
                
                # 篩選：有訊號 vs 觀望中
                active_signals = result_df[result_df["今日訊號"] != "觀望"]
                watchlist_signals = result_df[result_df["今日訊號"] == "觀望"]
                
                st.subheader("🎯 今日觸發交易訊號標的")
                if not active_signals.empty:
                    st.dataframe(
                        active_signals, 
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.success("掃描完畢：今天自選清單中沒有任何股票觸發進出場條件。")
                
                st.divider()
                
                # 折疊選單：顯示其餘正常的股票數據
                with st.expander("🔍 查看其餘盤整觀望中標的數據"):
                    st.dataframe(watchlist_signals, use_container_width=True, hide_index=True)
            else:
                st.error("無法讀取任何股票數據，請檢查代號是否輸入正確。")