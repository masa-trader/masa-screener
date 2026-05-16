import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# =====================================================================
#  🔒 【 後台安全管理 】可在這裡隨時更換你的登入密碼
# =====================================================================
MASA_PASSWORD = "masa888"  # 預設密碼為 masa888，你可以自由修改成任何字串

# =====================================================================
#  📢 【 麻紗觀察清單 】每天收盤更新股票，直接改這裡即可！
# =====================================================================
masa_watchlist = ["NVDA", "TSLA", "AAPL", "AMD", "TSM", "MSFT", "COIN", "MARA"]

# =====================================================================
#  ⚡ 【 費城半導體成分股 】(SOX 精選高波動動能股)
# =====================================================================
sox_tickers = [
    "NVDA", "AMD", "TSM", "AVGO", "QCOM", "ASML", "INTC", "TXN", "AMAT", "LRCX",
    "ADI", "MU", "MCHP", "ON", "MPWR", "KLAC", "MRVL", "SWKS", "QRVO", "NXPI",
    "LATT", "TER", "ENPH", "WOLF", "AMKR"
]

# =====================================================================
#  🔥 【 納斯達克 100 】完整核心成分股大池子 (100檔完整陣容)
# =====================================================================
nasdaq100_tickers = [
    "AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "GOOG", "TSLA", "AVGO", "COST",
    "NFLX", "AMD", "QCOM", "TMUS", "INTC", "TXN", "AMGN", "INTU", "ISRG", "HON",
    "AMAT", "BKNG", "VRTX", "ADI", "PANW", "MDLZ", "REGN", "LRCX", "GILD", "ADP",
    "MU", "MELI", "CSX", "KLAC", "ASML", "SNPS", "CDNS", "MAR", "ORLY", "CTAS",
    "NXPI", "PDD", "WDAY", "MNST", "CPRT", "CHTR", "PCAR", "AEP", "MCHP", "KDP",
    "PAYX", "DDOG", "ADSK", "FAST", "ODFL", "ROST", "EXC", "IDXX", "BKR", "CSGP",
    "CTSH", "ON", "FTNT", "TEAM", "CDW", "ANSS", "MDB", "GEHC", "MPWR", "TTWO",
    "CEG", "WBD", "ILMN", "KHC", "CHKP", "DXCM", "ALGN", "EBAY", "EA", "EXPE", 
    "BIIB", "VRSK", "MRNA", "VRSN", "AZN", "SBUX", "LULU", "FANG", "MCHP", "ADSK"
]

# =====================================================================
#  👑 【 標普 100 】完整超大權值股大池子 (100檔完整陣容)
# =====================================================================
sp100_tickers = [
    "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "GOOG", "META", "UNH", "LLY", "JPM", 
    "XOM", "TSLA", "V", "JNJ", "PG", "AVGO", "MA", "HD", "CVX", "MRK", "COST", 
    "ABBV", "PEP", "ADBE", "MCD", "WMT", "CRM", "BAC", "CSCO", "ACN", "T", "VZ", 
    "DIS", "CMCSA", "PFE", "NFLX", "NKE", "LOW", "INTU", "PM", "TXN", "COP", "MS", 
    "UNP", "AMGN", "HON", "IBM", "GE", "CAT", "GS", "BKNG", "DE", "RTX", "LMT", 
    "BLK", "TJX", "MDLZ", "REGN", "NOW", "SYK", "PLD", "AMT", "ISRG", "TGT", "MMC", 
    "SCHW", "ETN", "SLB", "ADI", "PGR", "WM", "BSX", "ZTS", "HCA", "ITW", "CI", 
    "CL", "CME", "EMR", "HUM", "FDX", "NSC", "BDX", "MO", "OXY", "MPC", "PSX",
    "MCO", "MAR", "ORCL", "ABT", "AXP", "BA", "C", "CVS", "DHR", "DUK", "NEE", "WFC"
]

# =====================================================================
#  🌏 【 熱門亞洲 ADR 精選 】
# =====================================================================
adr_tickers = ["TSM", "BABA", "PDD", "NIO", "LI", "XPEV", "JD", "BIDU", "NTES", "FUTU"]


# =====================================================================
#  🔑 密碼驗證核心機制 
# =====================================================================
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.set_page_config(page_title="權限驗證 - 麻紗宅在家", layout="centered", page_icon="🔒")
    st.title("🔒 麻紗宅在家專屬選股程式")
    st.subheader("本系統僅供指定學員與合作夥伴使用，請進行身份驗證。")
    
    pwd_input = st.text_input("🔑 請輸入專屬授權密碼：", type="password")
    if st.button("確認登入", type="primary"):
        if pwd_input == MASA_PASSWORD:
            st.session_state["authenticated"] = True
            st.success("驗證成功！正在載入系統...")
            st.rerun()
        else:
            st.error("❌ 密碼錯誤！請重新輸入，或聯繫「麻紗宅在家」管理員獲取授權。")
    st.stop()


# =====================================================================
#  🎉 驗證通過：進入主網頁畫面
# =====================================================================
st.set_page_config(page_title="麻紗宅在家專屬選股程式", layout="centered", page_icon="🚀")
st.title("🚀 麻紗宅在家專屬選股程式")

# 🚨 官方聲明警語 (置頂顯眼處)
st.warning("⚠️ **【系統警語】** 本選股程式所有計算結果均由大數據分析所得，內容僅供技術分析教學與學術研究參考，絕無任何買賣推薦與投資建議。金融市場交易具備高度風險，使用上請務必搭配教學思維，審慎獨立思考並自行評估判斷。")

# --- 💡 安全不洩密的操作指南折疊區 ---
with st.expander("📖 點我查看：系統快速上手與訊號操作指南"):
    st.markdown("""
    本系統後台搭載**「複合式多因子動能評分模型」**，結合了短線靈敏度、中長線動能濾網與主力籌碼的量能限制，專門捕捉市場高勝率的**波段動能轉折點**。
    
    ### 📌 快速上手三步驟：
    1. **選定板塊**：在下方單選鈕中，選擇您今天想要掃描的市場板塊。
    2. **一鍵啟動**：點擊最下方的紅色按鈕「開始全自動大規模雷達掃描」。
    3. **解讀數據**：系統將自動過濾出符合當日轉折訊號的股票。
    
    ### 🚦 交易訊號解讀指南：
    * 🟢 **做多買進**：代表多方動能成功引爆、或極端超賣區強勢落底反彈，屬於高勝率潛在起漲波段。
    * 🔴 **做空賣出**：代表短線動能已衝向極端過熱之頂峰，追高風險極大，策略觸發反向或壓制訊號。
    * 🟡 **多單出場**：代表原本的上升波段動能出現短期衰退，屬於技術面獲利了結、規避回檔風險的安全訊號。
    
    ### 💬 常見問題 QA：
    * **為什麼有時候掃描完是一片空白？**
      答：本模型的選股條件極其嚴苛。寧可錯過、不可做錯。若沒有符合條件的標的，代表今日市場處於曖昧盤整期，此時「空倉觀望」便是最頂尖的策略。
    """)

st.divider()

# --- 選擇掃描模式 ---
scan_mode = st.radio(
    "🎯 **請選擇你想掃描的股票板塊：**",
    [
        "📋 自訂清單（手動輸入）", 
        "⭐ 麻紗觀察清單（尚待更新中）", 
        "⚡ 費城半導體強勢股", 
        "🔥 納斯達克 100 龍頭", 
        "👑 標普 100 超大權值", 
        "🌏 熱門亞洲 ADR 精選"
    ],
    horizontal=False
)

# 💡 防呆機制：如果使用者切換了「股票板塊」，自動清空上一次的掃描記憶，避免畫面錯亂
if "last_scan_mode" not in st.session_state:
    st.session_state["last_scan_mode"] = scan_mode

if st.session_state["last_scan_mode"] != scan_mode:
    if "scan_results" in st.session_state:
        del st.session_state["scan_results"]
    st.session_state["last_scan_mode"] = scan_mode


# --- 根據選取的模式，自動切換輸入的股票池 ---
if "📋 自訂清單" in scan_mode:
    default_tickers = "NVDA, TSLA, AAPL"
    user_input = st.text_area("👉 請輸入股票代號（多檔請用「英文逗號 ,」或「換行」分隔）：", value=default_tickers, height=100)
elif "⭐ 麻紗觀察清單" in scan_mode:
    st.success(f"📌 已成功載入【麻紗觀察清單】核心標的（共 {len(masa_watchlist)} 檔）。")
    user_input = ",".join(masa_watchlist)
elif "⚡ 費城半導體" in scan_mode:
    st.success(f"📌 已成功載入【費城半導體 (SOX)】高動能成分股（共 {len(sox_tickers)} 檔）。")
    user_input = ",".join(sox_tickers)
elif "🔥 納斯達克" in scan_mode:
    st.info(f"💡 已選擇【納斯達克 100】科技權值股，系統將自動進行大規模掃描（共 {len(nasdaq100_tickers)} 檔）。")
    user_input = ",".join(nasdaq100_tickers)
elif "👑 標普 100" in scan_mode:
    st.info(f"💡 已選擇【標普 100】全美百大核心權值股，大規模掃描大約需要 15 秒（共 {len(sp100_tickers)} 檔）。")
    user_input = ",".join(sp100_tickers)
else:
    st.success(f"📌 已成功載入【熱門亞洲 ADR 精選】（共 {len(adr_tickers)} 檔）。")
    user_input = ",".join(adr_tickers)

# --- 核心策略運算邏輯 ---
def scan_kdj_rsi_strategy(ticker):
    try:
        df = yf.download(ticker, period='4mo', progress=False)
        if df.empty or len(df) < 30:
            return None
        
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
        
        close = df['Close'].astype(float)
        high = df['High'].astype(float)
        low = df['Low'].astype(float)
        volume = df['Volume'].astype(float)
        
        # 1. RSI 24
        delta = close.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.ewm(alpha=1/24, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1/24, adjust=False).mean()
        rsi24 = 100 - (100 / (1 + avg_gain / avg_loss))
        
        # 2. 中式標準 KDJ 9,3,3 遞迴
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
        
        df['Combo'] = df['J'] + df['RSI24']
        df['Vol_Cond'] = volume < volume.shift(1)
        
        def get_status_at(index_pos):
            c = df['Combo'].iloc[index_pos]
            vc = df['Vol_Cond'].iloc[index_pos]
            if vc:
                if (c > 100 and c <= 170) or (c < 30):
                    return "🟢 做多買進"
                elif c > 170:
                    return "🔴 做空賣出"
                elif c < 100 and c >= 30:
                    return "🟡 多單出場"
            return "盤整觀望"
        
        status_today = get_status_at(-1)
        status_yesterday = get_status_at(-2)
        
        signal_type = "🔄 訊號延續"
        if status_today != "盤整觀望" and status_today != status_yesterday:
            signal_type = "🆕 今日新觸發"
            
        return {
            "股票代號": ticker.upper().strip(),
            "模型即時動能評分": round(df['Combo'].iloc[-1], 2),
            "交易訊號判定": status_today,
            "訊號型態": signal_type
        }
    except:
        return None

# --- 網頁按鈕事件 ---
if st.button("🚀 開始全自動大規模雷達掃描", type="primary"):
    raw_tickers = user_input.replace("\n", ",").split(",")
    tickers = [t.strip().upper() for t in raw_tickers if t.strip()]
    
    if not tickers:
        st.warning("請輸入或選擇至少一檔股票代號！")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        results = []
        total_stocks = len(tickers)
        
        for idx, t in enumerate(tickers):
            status_text.text(f"⏳ 正在掃描量化模型 ({idx+1}/{total_stocks}): {t} ...")
            res = scan_kdj_rsi_strategy(t)
            if res:
                results.append(res)
            progress_bar.progress((idx + 1) / total_stocks)
            
        status_text.text("✅ 大數據量化計算完畢！")
        progress_bar.empty()
        
        # 💡 【核心修復點】將掃描結果存入記憶體中
        st.session_state["scan_results"] = results

# =====================================================================
#  💡 【核心修復點】渲染結果區移至按鈕外部，從記憶體讀取數據
# =====================================================================
if "scan_results" in st.session_state:
    results = st.session_state["scan_results"]
    
    if results:
        result_df = pd.DataFrame(results)
        active_signals = result_df[result_df["交易訊號判定"] != "盤整觀望"]
        watchlist_signals = result_df[result_df["交易訊號判定"] == "盤整觀望"]
        
        st.subheader("🎯 今日【觸發交易訊號】標的")
        
        if not active_signals.empty:
            # 互動篩選按鈕
            view_filter = st.radio(
                "🔍 **訊號即時篩選顯示：**",
                ["顯示全部觸發標的", "僅顯示今日全新觸發（第一天發動）"],
                horizontal=True,
                key="filter_status_radio"
            )
            
            if "僅顯示今日全新觸發" in view_filter:
                filtered_df = active_signals[active_signals["訊號型態"] == "🆕 今日新觸發"]
                if not filtered_df.empty:
                    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
                else:
                    # 💡 【核心修復點】如果今天沒有新觸發，不再閃退，而是優雅提示，且下方「盤整觀望中」依然能正常觀看
                    st.info("💡 沒有新觸發的股票")
            else:
                st.dataframe(active_signals, use_container_width=True, hide_index=True)
        else:
            st.success("🎉 今日這批股票中，沒有任何標的觸發進出場條件，請繼續耐心觀望。")
        
        st.divider()
        with st.expander("🔍 查看其餘【盤整觀望中】標的之即時綜合數據"):
            if "訊號型態" in watchlist_signals.columns:
                watchlist_signals = watchlist_signals.drop(columns=["訊號型態"])
            st.dataframe(watchlist_signals, use_container_width=True, hide_index=True)
    else:
        st.error("數據載入超時，請檢查網路或重新點擊掃描。")
