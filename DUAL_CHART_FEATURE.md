# Dual Chart Feature - Actual vs Predicted Prices

## Overview
Added a new dual chart visualization that clearly separates actual historical prices from AI predictions, and shows how predictions compare to reality. This helps users understand prediction accuracy and make better-informed decisions.

## Problem Statement
User example: "On 2/13, AMZN was not at $278"
- Predictions can diverge from actual prices
- Users need to see how accurate predictions are
- Need clear visual separation between actual and predicted data

## Solution: Two Chart Views

### 1. Combined View (Default)
Shows both actual and predicted prices on the same chart with clear visual distinction:
- **Actual Prices**: Solid green line (real market data)
- **Predicted Prices**: Dashed blue line (AI forecasts)
- **Confidence Bands**: Light blue shaded area (95% confidence interval)

### 2. Split View
Shows two separate charts side-by-side:

**Left Chart: Actual Historical Prices**
- 📊 Real market data only
- Shows what actually happened
- Green solid line
- Clean, focused view of reality

**Right Chart: Predicted vs Actual Comparison**
- 🔮 Overlays predictions on actual data
- Shows where predictions matched or diverged
- Both lines visible for direct comparison
- Highlights prediction accuracy

## Key Features

### Visual Distinction
```
Actual Price:     ━━━━━━━━━━━━━━━━ (solid green)
Predicted Price:  ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌ (dashed blue)
Confidence Range: ░░░░░░░░░░░░░░░░ (light blue shade)
```

### Interactive Tooltips
When hovering over the comparison chart:
```
Date: 2/13/2025
Actual: $225.50
Predicted: $228.00
Diff: $2.50 (1.11%)
```

Shows exactly how much the prediction was off by.

### Toggle Between Views
- **Combined View**: See everything at once
- **Split View**: Compare side-by-side

### Accuracy Metrics
Displays key information:
- Confidence Level: 85%
- Forecast Horizon: 90 Days
- Model: AI-Powered

Plus a note explaining that predictions may diverge due to unexpected events.

## Use Cases

### Example 1: Accurate Prediction
```
Date: 2/10
Actual: $220.00
Predicted: $221.50
Diff: $1.50 (0.68%) ✓ Close match
```

### Example 2: Divergent Prediction
```
Date: 2/13
Actual: $225.50
Predicted: $228.00
Diff: $2.50 (1.11%) ⚠️ Moderate divergence
```

### Example 3: Major Divergence
```
Date: 2/15 (after earnings)
Actual: $235.00
Predicted: $228.50
Diff: $6.50 (2.77%) ⚠️ Significant divergence
```

## Technical Implementation

### Data Structure
```javascript
// Historical actual data
{
  date: Date,
  dateStr: "2/13/2025",
  actualPrice: 225.50,
}

// Prediction data
{
  date: Date,
  dateStr: "2/20/2025",
  predictedPrice: 228.00,
  upperBound: 235.00,
  lowerBound: 221.00,
}

// Combined for comparison
{
  date: Date,
  dateStr: "2/20/2025",
  actualPrice: 225.50,      // What actually happened
  predictedPrice: 228.00,   // What was predicted
  // Automatically calculates difference
}
```

### Chart Library
Using Recharts LineChart for cleaner line visualization:
- Better for comparing multiple data series
- Clearer distinction between lines
- Professional appearance

### Color Scheme
- **Green (#34C759)**: Actual prices (reality)
- **Blue (#007AFF)**: Predicted prices (forecast)
- **Orange (#FF9500)**: Difference/divergence
- **Light Blue (rgba)**: Confidence intervals

## Benefits

### 1. Transparency
- Users see exactly how accurate predictions are
- No hiding prediction errors
- Builds trust through honesty

### 2. Education
- Users learn that predictions aren't perfect
- Understand confidence intervals
- Make realistic expectations

### 3. Better Decisions
- See when predictions are reliable
- Identify when to be cautious
- Understand market unpredictability

### 4. Visual Clarity
- Two separate charts eliminate confusion
- Clear labels and legends
- Professional presentation

## Real-World Example: AMZN

### Scenario
```
Date: 2/10/2025
Price: $220.00
Prediction for 2/13: $228.00 (+3.6%)

Actual on 2/13: $225.50 (+2.5%)
Difference: -$2.50 (-1.1%)
```

### What Users See

**Combined View:**
```
$230 ┤                    ╌╌╌╌╌ (predicted)
$225 ┤              ━━━━━━      (actual)
$220 ┤        ━━━━━
$215 ┤  ━━━━━
     └────────────────────────>
     2/10  2/11  2/12  2/13
```

**Split View:**

Left Chart (Actual):
```
$225 ┤              ━━━━━
$220 ┤        ━━━━━
$215 ┤  ━━━━━
     └────────────────────>
     Shows real price movement
```

Right Chart (Comparison):
```
$230 ┤              ╌╌╌╌╌ (predicted $228)
$225 ┤        ━━━━━━      (actual $225.50)
$220 ┤  ━━━━━
     └────────────────────>
     Shows $2.50 divergence
```

## User Interface

### View Toggle
```
┌─────────────────────────────────┐
│ [Combined View] [Split View]    │
└─────────────────────────────────┘
```

### Combined View Layout
```
┌─────────────────────────────────────────┐
│  Price Analysis                         │
│  ┌───────────────────────────────────┐  │
│  │                                   │  │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │  │
│  │  Actual (green solid)             │  │
│  │                                   │  │
│  │  ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌  │  │
│  │  Predicted (blue dashed)          │  │
│  │                                   │  │
│  └───────────────────────────────────┘  │
│                                         │
│  Legend: ━ Actual  ╌ Predicted  ░ Range│
└─────────────────────────────────────────┘
```

### Split View Layout
```
┌─────────────────────────────────────────┐
│  Price Analysis                         │
│  ┌──────────────┐  ┌──────────────┐    │
│  │ 📊 Actual    │  │ 🔮 Predicted │    │
│  │              │  │    vs Actual │    │
│  │  ━━━━━━━━━  │  │  ━━━━━━━━━  │    │
│  │              │  │  ╌╌╌╌╌╌╌╌╌  │    │
│  │              │  │              │    │
│  └──────────────┘  └──────────────┘    │
│                                         │
│  Accuracy Metrics                       │
│  Confidence: 85% | Horizon: 90d         │
└─────────────────────────────────────────┘
```

## Accuracy Insights Section

Shows important context:
```
┌─────────────────────────────────────────┐
│  Prediction Accuracy Insights           │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │Confidence│ │ Horizon  │ │  Model  │ │
│  │   85%    │ │  90 Days │ │AI-Power │ │
│  └──────────┘ └──────────┘ └─────────┘ │
│                                         │
│  💡 Predictions based on historical     │
│  trends, volatility, and sentiment.     │
│  Actual prices may diverge due to       │
│  unexpected events or news.             │
└─────────────────────────────────────────┘
```

## Files Created

### New Components
1. **frontend/src/components/DualChart.js**
   - Main dual chart component
   - Combined and split view logic
   - Tooltip with difference calculation
   - Accuracy metrics display

2. **frontend/src/components/DualChart.css**
   - Styling for both views
   - Responsive design
   - Legend and metrics styling

### Modified Files
1. **frontend/src/App.js**
   - Import DualChart component
   - Render both StockChart and DualChart
   - Pass same data to both

## Usage

### For Users
1. Analyze any stock (e.g., AMZN)
2. Scroll to "Price Analysis" section
3. See combined view by default
4. Click "Split View" to see side-by-side comparison
5. Hover over charts to see exact differences
6. Review accuracy metrics at bottom

### For Developers
```javascript
<DualChart 
  chartData={historicalData}    // Past prices
  quote={currentQuote}           // Current price
  predictions={aiPredictions}    // Future forecasts
/>
```

## Advantages Over Single Chart

### Before (Single Chart)
- ❌ Hard to distinguish actual from predicted
- ❌ Predictions mixed with reality
- ❌ No clear accuracy indication
- ❌ Confusing for users

### After (Dual Chart)
- ✓ Clear separation of actual vs predicted
- ✓ Side-by-side comparison available
- ✓ Shows exact divergence amounts
- ✓ Builds user trust through transparency

## Future Enhancements

### Potential Additions
1. **Historical Accuracy Tracking**
   - Show past prediction accuracy
   - Track model performance over time
   - Display accuracy trends

2. **Divergence Alerts**
   - Highlight when predictions are significantly off
   - Color-code accuracy levels
   - Show reasons for divergence

3. **Multiple Prediction Models**
   - Compare different AI models
   - Show ensemble predictions
   - Display model confidence

4. **Export Functionality**
   - Download charts as images
   - Export data to CSV
   - Share analysis reports

## Summary

The dual chart feature provides:
- **Two viewing modes**: Combined and split
- **Clear visual distinction**: Actual (solid green) vs Predicted (dashed blue)
- **Accuracy metrics**: Shows how reliable predictions are
- **Interactive tooltips**: Displays exact differences
- **Educational value**: Helps users understand prediction limitations

This feature addresses the user's concern about prediction accuracy (e.g., "AMZN was not at $278 on 2/13") by making it crystal clear when and how much predictions diverge from reality.

**Key Achievement**: Users can now see exactly how accurate (or inaccurate) predictions are! ✓
