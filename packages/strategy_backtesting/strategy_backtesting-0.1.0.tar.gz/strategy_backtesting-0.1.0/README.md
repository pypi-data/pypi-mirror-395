# PYTHON STRATEGY BACKTESTING
A cool Python backtesting tool.

### The idea
You load CSV chart data into the library, build your strategy on top of it and **SIMULATE** it! 🥳

## Installation
```bash
pip install strategy_backtesting
```

Install it with PIP and then **USE IT**!!

Keep in mind that all the CSV data need to follow this format:
```
timestamp,open,high,low,close,volume
```
where timestamp is in milliseconds and ordered from OLDEST to NEWEST.

## Example
To start, let's import the required libraries:

```python
import strategy_backtesting as sb
import pandas as pd
```

### After that we will define the settings for our simulation

**timespan** - The number of data points (e.g., 1000)

**buy_amount** - What the simulator will buy if triggered

**sell_amount** - What the simulator will sell if triggered

```python
settings = sb.Settings(timespan=1000, buy_amount=1, sell_amount=1)
```

Then we will create our chart object and apply the settings and CSV file (in this case the ETHUSDT chart data)
```python
eth_chart = sb.ChartManager()
eth_chart.set_chart_settings(settings=settings)
eth_chart.set_chart_data(pd.read_csv("ETHUSDT_1h.csv").iloc[::-1])
```


Then I will add my strategy, for example: Buying it only if the RSI is in cricial area
```python
buy_data = []
sell_data = []
oversold = 30
overbought = 70
for _, row in experiment_chart.iterrows():
    if not pd.notna(row["RSI"]):
        continue
    rsi = row["RSI"]
    if rsi < oversold:
        buy_data.append([row["timestamp"], row.get("close")])
    elif rsi > overbought:
        sell_data.append([row["timestamp"], row.get("close")])
```

Adding the strategy and simulating it

```python
strategy = sb.Strategy(name="RSI Strategy")
strategy.set_strategy_buys(buys=buy_data)
strategy.set_strategy_sells(sells=sell_data)

simulation = sb.Simulation(chart=experiment_chart, settings=settings, strategy=strategy)
portfolio = simulation.simulate()

print("TOTAL PnL: "+str(round((portfolio["balance"].iloc[-1])-settings.default_money, 2))+"$")

simulation.graph(rsi=True, rsi_over=[oversold, overbought], ema=True)
```