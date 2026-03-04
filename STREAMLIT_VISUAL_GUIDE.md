# 🎨 Streamlit App - Visual Guide

## 📱 App Layout

```
┌─────────────────────────────────────────────────────────────┐
│  📈 Investment Research Agent                                │
├──────────────┬──────────────────────────────────────────────┤
│              │                                               │
│  SIDEBAR     │           MAIN CONTENT                        │
│              │                                               │
│  🎯 Watchlist│  ┌─────────────────────────────────────────┐ │
│  ┌─────────┐│  │  Current Price    Day Change    Volume  │ │
│  │Add Stock││  │  $150.25 (+2.5%)  $3.75        1.2M     │ │
│  └─────────┘│  └─────────────────────────────────────────┘ │
│              │                                               │
│  Your Stocks │  📊 Chart | 📰 News | 💬 Social | 📈 Analysis│
│  ┌─────────┐│  ┌─────────────────────────────────────────┐ │
│  │📊 AAPL  ││  │                                          │ │
│  │🗑️       ││  │         [Interactive Chart]              │ │
│  └─────────┘│  │                                          │ │
│  ┌─────────┐│  │                                          │ │
│  │📊 TSLA  ││  └─────────────────────────────────────────┘ │
│  │🗑️       ││                                               │
│  └─────────┘│                                               │
│              │                                               │
│  ⚙️ Settings │                                               │
│              │                                               │
└──────────────┴──────────────────────────────────────────────┘
```

## 🎯 Main Features

### 1. Watchlist (Sidebar)

```
┌─────────────────┐
│ 🎯 Watchlist    │
├─────────────────┤
│ Add Stock       │
│ ┌─────────────┐ │
│ │ AAPL        │ │
│ └─────────────┘ │
│ [➕ Add]        │
├─────────────────┤
│ Your Stocks     │
│ ┌─────────────┐ │
│ │📊 AAPL  🗑️ │ │
│ │📊 TSLA  🗑️ │ │
│ │📊 NVDA  🗑️ │ │
│ └─────────────┘ │
└─────────────────┘
```

### 2. Stock Overview

```
┌──────────────────────────────────────────────────┐
│  Current Price    Day Change    Volume    Sentiment│
│  ┌────────────┐  ┌──────────┐  ┌──────┐  ┌──────┐│
│  │ $150.25    │  │ +$3.75   │  │ 1.2M │  │ 😊   ││
│  │ +2.5% ↑    │  │ +2.5%    │  │      │  │ 0.75 ││
│  └────────────┘  └──────────┘  └──────┘  └──────┘│
└──────────────────────────────────────────────────┘
```

### 3. Tabs

```
┌─────────────────────────────────────────────────┐
│ 📊 Chart | 📰 News | 💬 Social | 📈 Analysis | 🔮 Predictions │
├─────────────────────────────────────────────────┤
│                                                  │
│  [Tab Content Here]                              │
│                                                  │
└─────────────────────────────────────────────────┘
```

## 📊 Chart Tab

```
┌─────────────────────────────────────────────────┐
│ 📊 AAPL Price Chart                              │
├─────────────────────────────────────────────────┤
│ Time Range: [1D] [5D] [1M] [3M] [6M] [1Y] [5Y] │
├─────────────────────────────────────────────────┤
│                                                  │
│  $160 ┤                    ╭─╮                  │
│       │                  ╭─╯ ╰╮                 │
│  $150 ┤              ╭───╯    ╰─╮               │
│       │          ╭───╯          ╰─╮             │
│  $140 ┤      ╭───╯                ╰───╮         │
│       └──────┴────┴────┴────┴────┴────┴─────    │
│        Jan   Feb  Mar  Apr  May  Jun  Jul       │
│                                                  │
│  Volume:                                         │
│  ████ ███ ████ ██ ███ ████ ███                 │
│                                                  │
├─────────────────────────────────────────────────┤
│ Compare with Another Stock                       │
│ ┌──────────────┐                                │
│ │ Enter ticker │ [Compare]                      │
│ └──────────────┘                                │
└─────────────────────────────────────────────────┘
```

## 📰 News Tab

```
┌─────────────────────────────────────────────────┐
│ 📰 Latest News                                   │
├─────────────────────────────────────────────────┤
│ ┌───────────────────────────────────────────┐   │
│ │ Apple Announces New Product Line           │   │
│ │ Source: TechCrunch | 2 hours ago          │   │
│ │ Apple Inc. today unveiled its latest...   │   │
│ │ [Read more →]                              │   │
│ └───────────────────────────────────────────┘   │
│ ┌───────────────────────────────────────────┐   │
│ │ Stock Surges on Earnings Beat             │   │
│ │ Source: Bloomberg | 5 hours ago           │   │
│ │ Shares jumped 5% after the company...     │   │
│ │ [Read more →]                              │   │
│ └───────────────────────────────────────────┘   │
│ ┌───────────────────────────────────────────┐   │
│ │ Analysts Upgrade Rating                    │   │
│ │ Source: CNBC | 1 day ago                  │   │
│ │ Major investment firms have upgraded...    │   │
│ │ [Read more →]                              │   │
│ └───────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

## 💬 Social Media Tab

```
┌─────────────────────────────────────────────────┐
│ 💬 Social Media Sentiment                        │
├─────────────────────────────────────────────────┤
│ ┌───────────────────────────────────────────┐   │
│ │ "Just bought more AAPL! 🚀"               │   │
│ │ Platform: Reddit | 1 hour ago             │   │
│ │                              [✅ Positive] │   │
│ └───────────────────────────────────────────┘   │
│ ┌───────────────────────────────────────────┐   │
│ │ "Concerned about the recent dip..."       │   │
│ │ Platform: Twitter | 3 hours ago           │   │
│ │                              [⚠️ Neutral]  │   │
│ └───────────────────────────────────────────┘   │
│ ┌───────────────────────────────────────────┐   │
│ │ "Selling my position, too risky"          │   │
│ │ Platform: Reddit | 5 hours ago            │   │
│ │                              [❌ Negative] │   │
│ └───────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

## 📈 Analysis Tab

```
┌─────────────────────────────────────────────────┐
│ 📈 Deep Analysis                                 │
├─────────────────────────────────────────────────┤
│ Technical Indicators                             │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│ │ RSI      │ │ MACD     │ │ Signal   │         │
│ │ 65.5     │ │ 2.34     │ │ BUY      │         │
│ └──────────┘ └──────────┘ └──────────┘         │
│                                                  │
│ Fundamental Metrics                              │
│ ┌────────┐ ┌──────────┐ ┌────────┐ ┌────────┐ │
│ │ P/E    │ │ Mkt Cap  │ │ 52W Hi │ │ 52W Lo │ │
│ │ 28.5   │ │ $2.8T    │ │ $180   │ │ $125   │ │
│ └────────┘ └──────────┘ └────────┘ └────────┘ │
│                                                  │
│ AI Summary                                       │
│ ┌───────────────────────────────────────────┐   │
│ │ Based on technical and fundamental        │   │
│ │ analysis, AAPL shows strong momentum      │   │
│ │ with positive sentiment. RSI indicates    │   │
│ │ slight overbought conditions...           │   │
│ └───────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

## 🔮 Predictions Tab

```
┌─────────────────────────────────────────────────┐
│ 🔮 Predictive Analysis                           │
├─────────────────────────────────────────────────┤
│ Price Predictions        Confidence Levels       │
│ ┌──────────────────┐    ┌──────────────────┐   │
│ │ 7-Day Forecast   │    │ 7-Day: 85%       │   │
│ │ $155.50          │    │ ████████████░░░  │   │
│ │                  │    │                  │   │
│ │ 30-Day Forecast  │    │ 30-Day: 72%      │   │
│ │ $162.25          │    │ ██████████░░░░░  │   │
│ │                  │    │                  │   │
│ │ 90-Day Forecast  │    │ 90-Day: 58%      │   │
│ │ $170.00          │    │ ████████░░░░░░░  │   │
│ └──────────────────┘    └──────────────────┘   │
│                                                  │
│ Model Insights                                   │
│ ┌───────────────────────────────────────────┐   │
│ │ The model predicts continued upward       │   │
│ │ momentum based on historical patterns,    │   │
│ │ sentiment analysis, and market trends.    │   │
│ │ Confidence decreases for longer-term      │   │
│ │ predictions due to market volatility.     │   │
│ └───────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

## 🏠 Welcome Screen

```
┌─────────────────────────────────────────────────┐
│ Welcome to Investment Research Agent! 👋         │
├─────────────────────────────────────────────────┤
│                                                  │
│ This AI-powered platform helps you make          │
│ informed investment decisions by analyzing:      │
│                                                  │
│ 📊 Real-time stock prices and historical data   │
│ 📰 Latest news articles from trusted sources    │
│ 💬 Social media sentiment analysis              │
│ 📈 Technical and fundamental analysis           │
│ 🔮 AI-powered price predictions                 │
│                                                  │
│ Getting Started                                  │
│ 1. Add a stock ticker to your watchlist         │
│ 2. Click on any stock to view detailed analysis │
│ 3. Explore different tabs for insights          │
│                                                  │
│ Popular Stocks                                   │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐  │
│ │➕AAPL│ │➕TSLA│ │➕NVDA│ │➕MSFT│ │➕GOOGL│  │
│ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘  │
│                                                  │
└─────────────────────────────────────────────────┘
```

## ⚙️ Settings (Sidebar)

```
┌─────────────────┐
│ ⚙️ Settings     │
├─────────────────┤
│ API Base URL    │
│ ┌─────────────┐ │
│ │ localhost:  │ │
│ │ 5000        │ │
│ └─────────────┘ │
│                 │
│ [Test Connection]│
│                 │
│ Status: ✅ OK   │
└─────────────────┘
```

## 🎨 Color Scheme

```
Primary Color:   #1f77b4 (Blue)
Background:      #ffffff (White)
Secondary BG:    #f0f2f6 (Light Gray)
Text:            #262730 (Dark Gray)
Success:         #00c853 (Green)
Error:           #ff1744 (Red)
Warning:         #ffa726 (Orange)
```

## 📱 Mobile View

```
┌──────────────┐
│ ☰  Investment│
│    Research  │
├──────────────┤
│ Add Stock    │
│ ┌──────────┐ │
│ │ AAPL     │ │
│ └──────────┘ │
│ [➕ Add]     │
├──────────────┤
│ 📊 AAPL      │
│ $150.25      │
│ +2.5% ↑      │
├──────────────┤
│ [Chart]      │
│ [News]       │
│ [Social]     │
│ [Analysis]   │
└──────────────┘
```

## 🎯 User Flow

```
1. User arrives → Welcome screen
                    ↓
2. Add stock → Watchlist updated
                    ↓
3. Click stock → Load data
                    ↓
4. View tabs → Explore insights
                    ↓
5. Compare → Add another stock
                    ↓
6. Subscribe → Get email alerts
```

## 💡 Interactive Elements

### Buttons
```
┌──────────────┐
│ ➕ Add Stock │  ← Primary action
└──────────────┘

┌──────────────┐
│ 🗑️ Remove    │  ← Destructive action
└──────────────┘

┌──────────────┐
│ 📊 View      │  ← Secondary action
└──────────────┘
```

### Metrics
```
┌──────────────┐
│ Current Price│
│ $150.25      │
│ +2.5% ↑      │  ← Delta indicator
└──────────────┘
```

### Progress Bars
```
Confidence: 85%
████████████████░░░░
```

### Status Indicators
```
✅ Connected
❌ Error
⚠️ Warning
ℹ️ Info
```

## 🚀 Loading States

```
┌─────────────────────────────────┐
│ Loading data for AAPL...        │
│ ⏳ Please wait...               │
└─────────────────────────────────┘
```

## ✨ Success Messages

```
┌─────────────────────────────────┐
│ ✓ Added AAPL to watchlist       │
└─────────────────────────────────┘
```

## ❌ Error Messages

```
┌─────────────────────────────────┐
│ ✗ Could not load data for AAPL  │
│ Please try again later          │
└─────────────────────────────────┘
```

---

This visual guide shows the complete layout and user experience of your Streamlit app! 🎨
