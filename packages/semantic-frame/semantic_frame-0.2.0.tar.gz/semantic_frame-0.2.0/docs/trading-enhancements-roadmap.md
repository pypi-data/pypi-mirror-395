# Trading Enhancements Roadmap

> Generated: 2024-12-04
> Context: Feedback from Battle Risen integration testing

## Overview

These enhancements would transform semantic-frame from a general-purpose data analyzer into a **trading intelligence toolkit** optimized for agent-based trading systems like Battle Risen.

---

## Priority 1: High Value, Low-Medium Complexity

### 1. Drawdown Analysis

**Tool:** `describe_drawdown`

**Input:**
```python
equity_curve = [10000, 10500, 10200, 9800, 9500, 10000, 10800]
```

**Output:**
```json
{
  "max_drawdown_pct": 9.52,
  "max_drawdown_duration": 4,
  "current_drawdown": 0,
  "drawdown_periods": [
    {"start": 1, "end": 4, "depth": 9.52, "recovered": true}
  ],
  "narrative": "Max drawdown of 9.5% lasting 4 periods, fully recovered. Currently at equity high."
}
```

**Why Battle Risen Needs This:**
- Already tracks `max_drawdown` but lacks semantic description
- Drawdown behavior (frequency, depth, recovery time) helps compare agent risk profiles
- Critical for risk management decisions

**Implementation Notes:**
- Pure math on equity curves
- Building blocks exist in `analyzers.py`
- Estimated effort: Medium

---

### 2. Trading Performance Metrics

**Tool:** `describe_trading_performance`

**Input:**
```python
trades = [100, -50, 75, -25, 150, -30, 80]  # PnL per trade
```

**Output:**
```json
{
  "win_rate": 0.65,
  "profit_factor": 2.3,
  "expectancy": 45.50,
  "risk_reward_ratio": 1.8,
  "max_consecutive_wins": 5,
  "max_consecutive_losses": 3,
  "recovery_factor": 2.1,
  "calmar_ratio": 1.5,
  "narrative": "GROK4 has high win rate (72%) but poor risk-reward (0.8:1), suggesting overtrading"
}
```

**Metrics Explained:**
| Metric | Formula | Meaning |
|--------|---------|---------|
| Win Rate | wins / total_trades | % of profitable trades |
| Profit Factor | gross_profit / gross_loss | Quality of wins vs losses |
| Expectancy | avg $ per trade | Expected value per trade |
| Risk/Reward | avg_win / avg_loss | Payoff ratio |
| Recovery Factor | net_profit / max_drawdown | Efficiency of recovery |
| Calmar Ratio | annual_return / max_drawdown | Risk-adjusted performance |

**Why Battle Risen Needs This:**
- Agent performance comparison with trading-specific context
- Identifies issues like "high win rate but poor risk-reward"
- Feeds into agent personality validation

**Implementation Notes:**
- Straightforward calculations
- Estimated effort: Medium

---

### 3. Comparative Rankings

**Tool:** `describe_rankings`

**Input:**
```python
{
  "CLAUDE": [100, 105, 110],
  "GROK4": [100, 120, 90],
  "GPT5": [100, 102, 104]
}
```

**Output:**
```json
{
  "rankings": {
    "total_return": ["CLAUDE", "GPT5", "GROK4"],
    "volatility": ["GPT5", "CLAUDE", "GROK4"],
    "risk_adjusted": ["CLAUDE", "GPT5", "GROK4"]
  },
  "leader": "CLAUDE",
  "most_volatile": "GROK4",
  "most_consistent": "GPT5",
  "narrative": "CLAUDE leads on risk-adjusted basis. GROK4 highest returns but extreme volatility. GPT5 most consistent but lowest upside."
}
```

**Why Battle Risen Needs This:**
- Leaderboard is a core feature
- Semantic rankings with context enhance the dashboard
- Multi-dimensional comparison (return vs risk vs consistency)

**Implementation Notes:**
- Already have multi-column analysis
- Just need ranking logic on top
- Estimated effort: Low

---

### 4. Enhanced Anomaly Context

**Tool:** Enhanced `describe_data` anomaly output

**Current Output:**
```json
{
  "anomalies": [{"index": 5, "value": -500, "z_score": 4.2}]
}
```

**Enhanced Output:**
```json
{
  "anomalies": [
    {
      "index": 5,
      "value": -500,
      "severity": "extreme",
      "type": "loss",
      "z_score": -4.2,
      "context": "Largest single-trade loss, 3x typical loss size"
    }
  ],
  "anomaly_frequency": "rare",
  "narrative": "1 extreme anomaly detected: catastrophic loss at index 5. This represents tail risk exposure."
}
```

**Why Battle Risen Needs This:**
- Distinguish "normal volatility" vs "something broke"
- Severity classification (mild, moderate, extreme)
- Type classification (gain, loss, volume_spike)

**Implementation Notes:**
- Extend existing anomaly detection
- Add severity thresholds and type inference
- Estimated effort: Low

---

## Priority 2: Medium Value, Medium Complexity

### 5. Time-Windowed Analysis

**Tool:** `describe_windows`

**Input:**
```python
data = [...],
windows = ["1h", "4h", "1d"]
```

**Output:**
```json
{
  "1h": {"trend": "rising", "volatility": "high"},
  "4h": {"trend": "flat", "volatility": "moderate"},
  "1d": {"trend": "rising", "volatility": "low"},
  "narrative": "Short-term noise (1h high volatility) but stable daily uptrend. Suggests hold through intraday swings."
}
```

**Why Battle Risen Needs This:**
- Uses ring buffers with different timeframes (3min intraday, 4h long-term)
- Unified multi-window analysis
- Filters noise from signal

**Implementation Notes:**
- Need to handle resampling/aggregation
- May need pandas resample or custom windowing
- Estimated effort: Medium

---

### 6. Regime Detection

**Tool:** `describe_regime`

**Input:**
```python
returns = [0.01, 0.02, 0.01, -0.05, -0.08, -0.03, 0.02, 0.03, 0.04]
```

**Output:**
```json
{
  "current_regime": "recovery",
  "regimes_detected": [
    {"type": "bull", "start": 0, "end": 2},
    {"type": "bear", "start": 3, "end": 5},
    {"type": "recovery", "start": 6, "end": 8}
  ],
  "regime_stability": "unstable",
  "narrative": "Currently in recovery regime after bear period. 3 regime changes in 9 periods suggests unstable conditions."
}
```

**Why Battle Risen Needs This:**
- GEMINI is a contrarian trader - regime context matters
- "Late bull regime" vs "early recovery" affects agent decisions
- Market state awareness

**Implementation Notes:**
- Could use Hidden Markov Models (complex) or threshold-based (simpler)
- Start with simple threshold approach
- Estimated effort: High

---

## Priority 3: Specialized, Higher Complexity

### 7. Position Sizing / Allocation Suggestions

**Tool:** `describe_allocation`

**Input:**
```python
{
  "assets": {"BTC": [...], "ETH": [...], "SOL": [...]},
  "correlations": true,
  "target_volatility": 0.15
}
```

**Output:**
```json
{
  "suggested_weights": {"BTC": 0.5, "ETH": 0.3, "SOL": 0.2},
  "portfolio_volatility": 0.14,
  "diversification_score": 0.72,
  "narrative": "BTC/ETH highly correlated (r=0.95), limited diversification benefit. SOL provides some hedge. Target volatility achievable with 50/30/20 split."
}
```

**Why Battle Risen Needs This:**
- Agents make position sizing decisions
- Semantic allocation guidance could improve agent prompts
- Risk-based portfolio construction

**Implementation Notes:**
- Mean-variance optimization
- Needs careful design to avoid bad advice
- Consider adding disclaimers
- Estimated effort: High

---

## Proposed Architecture

```
semantic_frame/
├── core/
│   ├── analyzers.py          # existing
│   ├── correlations.py       # existing
│   └── ...
├── trading/                   # NEW MODULE
│   ├── __init__.py
│   ├── metrics.py            # win_rate, profit_factor, sharpe, etc.
│   ├── drawdown.py           # drawdown analysis
│   ├── regime.py             # regime detection
│   ├── rankings.py           # comparative analysis
│   └── windows.py            # time-windowed analysis
├── integrations/
│   └── mcp.py                # add new tools here
```

**MCP Tools to Add:**
- `describe_drawdown`
- `describe_trading_performance`
- `describe_rankings`
- `describe_regime`
- `describe_windows`
- `describe_allocation`

---

## Implementation Order

| Phase | Features | Effort | Value |
|-------|----------|--------|-------|
| **Phase 1** | Drawdown + Trading Metrics | 1-2 days | High |
| **Phase 2** | Rankings + Anomaly Context | 1 day | High |
| **Phase 3** | Time Windows | 1 day | Medium |
| **Phase 4** | Regime Detection | 2-3 days | Medium |
| **Phase 5** | Allocation (optional) | 3-5 days | Specialized |

---

## Summary Table

| Enhancement | Value for Battle Risen | Complexity | Priority |
|-------------|------------------------|------------|----------|
| Drawdown Analysis | ⭐⭐⭐⭐⭐ | Medium | 1 |
| Trading Metrics | ⭐⭐⭐⭐⭐ | Medium | 1 |
| Comparative Rankings | ⭐⭐⭐⭐ | Low | 2 |
| Anomaly Context | ⭐⭐⭐⭐ | Low | 2 |
| Time Windows | ⭐⭐⭐ | Medium | 3 |
| Regime Detection | ⭐⭐⭐ | High | 3 |
| Allocation | ⭐⭐ | High | 4 |

---

## Next Steps: Discussion & Brainstorming First

**Before implementing, we should discuss:**

### Architecture Decisions
- Should this be a separate package (`semantic-frame-trading`) or integrated into core `semantic-frame`?
- How do we handle optional dependencies (e.g., if regime detection needs HMM libraries)?
- Should trading tools be a separate MCP server or extend the existing one?

### API Design
- What input formats work best for Battle Risen's data structures?
- Should we support both single-agent and multi-agent comparisons in one tool?
- How verbose should narratives be? (concise for dashboards vs detailed for analysis)

### Feature Prioritization
- Which features would have the most immediate impact on Battle Risen?
- Are there any quick wins we can ship first to validate the approach?
- Should we prototype one feature end-to-end before building the full module?

### Data Requirements
- What sample data from Battle Risen should we use for testing?
- Are there edge cases (empty trades, single data point, etc.) we need to handle?
- How should we handle different timeframes and data frequencies?

### Integration Questions
- How will Battle Risen consume these new tools? (MCP, direct Python, both?)
- Should the trading tools feed back into agent prompts automatically?
- Any performance considerations for real-time analysis?

---

## Notes

- Start with **Drawdown Analysis** and **Trading Metrics** - high value, direct mapping to Battle Risen data
- Consider whether these should be a separate package (`semantic-frame-trading`) or integrated into core
- Test with real Battle Risen data as we build
- Keep token efficiency in mind - trading summaries should still compress well
