# VERDICT Python SDK

Official Python SDK for the VERDICT AI-powered crypto trading analyzer with Flare Network verification.

## Features

- 🔍 **Single Analysis** - Get instant trading recommendations
- 🔄 **Real-time Streaming** - Stream live market analysis
- 🤖 **AI-Powered** - Advanced sentiment analysis using Google Gemini
- 🔐 **Flare Verification** - On-chain price verification via FTSO
- ⚡ **Async/Sync Support** - Use async for performance or sync for simplicity
- 🔑 **BYOK Model** - Bring Your Own API Keys (zero cost to you!)

## Installation

```bash
pip install verdict-sdk
```

## Quick Start

### Get Your API Keys

You'll need two API keys:
1. **CoinMarketCap API Key**: Get it at https://coinmarketcap.com/api/
2. **Google Gemini API Key**: Get it at https://aistudio.google.com/app/apikey

### Basic Example

```python
import asyncio
from verdict_sdk import VerdictClient

async def main():
    # Initialize client with your API keys
    client = VerdictClient(
        api_url="https://verdict-api.example.com",  # Your VERDICT API URL
        cmc_api_key="your_coinmarketcap_key",
        gemini_api_key="your_gemini_key"
    )
    
    # Get trading analysis
    result = await client.analyze(
        token="BTC",
        portfolio_amount=1000.0,
        risk_level="moderate"
    )
    
    print(f"Recommendation: {result.recommendation}")
    print(f"Confidence: {result.confidence}%")
    print(f"Price: ${result.market_data.price:,.2f}")
    
    await client.close()

asyncio.run(main())
```

### Real-time Streaming

```python
async def stream_example():
    client = VerdictClient(
        api_url="https://verdict-api.example.com",
        cmc_api_key="your_key",
        gemini_api_key="your_key"
    )
    
    # Stream live updates every 2 seconds
    async for analysis in client.stream_agent(
        token="ETH",
        portfolio_amount=500.0,
        interval=2.0
    ):
        print(f"{analysis.recommendation} - ${analysis.market_data.price:.2f}")
        
        # Your trading logic here
        if analysis.confidence > 80 and analysis.verified:
            print(f"High confidence signal: {analysis.recommendation}!")

asyncio.run(stream_example())
```

## API Reference

### VerdictClient

Main client for interacting with VERDICT API.

#### `__init__(api_url, cmc_api_key, gemini_api_key, timeout=30.0, max_retries=3)`

Initialize the client.

**Parameters:**
- `api_url` (str): Base URL of the VERDICT API
- `cmc_api_key` (str): Your CoinMarketCap API key
- `gemini_api_key` (str): Your Google Gemini API key
- `timeout` (float): Request timeout in seconds
- `max_retries` (int): Maximum number of retries

#### `async analyze(token, stablecoin="USDC", portfolio_amount=100.0, risk_level="moderate")`

Perform a single trading analysis.

**Returns:** `AnalysisResponse` object

#### `async stream_agent(token, stablecoin="USDC", portfolio_amount=100.0, risk_level="moderate", interval=1.0)`

Stream real-time trading signals.

**Yields:** `AnalysisResponse` objects

#### `analyze_sync(...)`

Synchronous version of `analyze()` for non-async code.

## Response Structure

Every analysis returns an `AnalysisResponse` with:

```python
{
    "recommendation": "LONG",  # LONG, SHORT, or HOLD
    "confidence": 78.5,  # Confidence percentage
    "signal_score": 35.67,  # Combined signal score
    
    "market_data": {
        "price": 45000.50,
        "percent_change_24h": 2.45,
        "volume_24h": 25000000000,
        ...
    },
    
    "sentiment_data": {
        "overall_sentiment": 0.65,
        "key_factors": ["Strong momentum", "Positive news"],
        ...
    },
    
    "leverage_suggestion": {
        "suggested_leverage": 10,
        "max_safe_leverage": 20
    },
    
    "perp_trade_details": {
        "position_size_usd": 10000,
        "if_price_moves_5pct_up": {
            "pnl": 500,
            "roi_pct": 50
        },
        ...
    },
    
    "verified": true,  # Flare Network verification
    "ftso_price": 45001.20,  # FTSO verified price
    ...
}
```

## Examples

Check the [examples/](examples/) directory for:
- `basic_analysis.py` - Simple one-time analysis
- `real_time_stream.py` - Live streaming with formatted output
- `trading_bot.py` - Automated trading bot example

## Error Handling

```python
from verdict_sdk import VerdictClient, VerdictAPIError, VerdictAuthError

try:
    result = await client.analyze("BTC")
except VerdictAuthError:
    print("Invalid API keys!")
except VerdictAPIError as e:
    print(f"API error: {e}")
```

## Development

### Install in development mode

```bash
git clone https://github.com/yourusername/verdict-sdk
cd verdict-sdk
pip install -e ".[dev]"
```

### Run tests

```bash
pytest tests/
```

## License

MIT License - see LICENSE file

## Support

- Documentation: https://verdict-docs.example.com
- Issues: https://github.com/yourusername/verdict-sdk/issues
- Discord: https://discord.gg/verdict

## Disclaimer

⚠️ **This tool is for informational purposes only.** Trading cryptocurrencies carries significant risk. Always do your own research and never invest more than you can afford to lose.
