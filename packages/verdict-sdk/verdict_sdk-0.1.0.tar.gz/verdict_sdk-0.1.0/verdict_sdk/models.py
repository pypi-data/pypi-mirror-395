"""Pydantic models for VERDICT SDK."""

from typing import Optional, Dict, List
from enum import Enum
from pydantic import BaseModel, Field


class Recommendation(str, Enum):
    """Trading recommendation enum."""
    LONG = "LONG"
    SHORT = "SHORT"
    HOLD = "HOLD"


class RiskLevel(str, Enum):
    """Risk level enum."""
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


class MarketData(BaseModel):
    """Market data from CoinMarketCap."""
    price: float
    market_cap: float
    volume_24h: float
    percent_change_1h: float
    percent_change_24h: float
    percent_change_7d: float
    live_price: Optional[float] = None
    cmc_price: Optional[float] = None


class SentimentData(BaseModel):
    """AI-powered sentiment analysis data."""
    overall_sentiment: float = Field(..., description="Overall sentiment score")
    short_term_sentiment: float
    medium_term_sentiment: float
    risk_level: str
    key_factors: List[str] = Field(default_factory=list)


class OnChainData(BaseModel):
    """On-chain analysis data."""
    onchain_signal: float
    activity_score: float
    liquidity_score: float
    transaction_count_24h: int
    total_liquidity_usd: float


class LeverageSuggestion(BaseModel):
    """Leverage suggestion details."""
    suggested_leverage: int
    max_safe_leverage: int
    warning: Optional[str] = None


class PositionInfo(BaseModel):
    """Current position information."""
    status: str
    type: Optional[str] = None
    entry_price: Optional[float] = None
    current_price: Optional[float] = None
    leverage: Optional[int] = None
    collateral: Optional[float] = None
    position_size: Optional[float] = None
    pnl_usd: Optional[float] = None
    pnl_pct: Optional[float] = None


class ExecutionSignal(BaseModel):
    """Execution signal for trading."""
    action: str
    should_open: Optional[bool] = None
    should_close: Optional[bool] = None
    reason: Optional[str] = None
    exit_conditions: Optional[List[str]] = None
    current_pnl_pct: Optional[float] = None
    current_pnl_usd: Optional[float] = None


class PerpTradeDetails(BaseModel):
    """Perpetual trade calculation details."""
    collateral_stablecoin: float
    stablecoin: str
    suggested_leverage: int
    position_size_usd: float
    token_exposure: float
    current_price: float
    margin_required: float
    token: str
    if_price_moves_5pct_up: Dict[str, float]
    if_price_moves_5pct_down: Dict[str, float]


class ComponentStatus(BaseModel):
    """Component health status."""
    overall: str
    components: Dict[str, Dict]


class RulesEvaluation(BaseModel):
    """Rules engine evaluation results."""
    rules_evaluated: int
    rules_passed: int
    rules_failed: int
    overall_status: str
    should_block: bool
    failed_rules: Optional[List[Dict]] = None


class AnalysisResponse(BaseModel):
    """Complete analysis response from VERDICT API."""
    token: str
    stablecoin: str
    portfolio_amount: float
    risk_level: str
    timestamp: str
    recommendation: str
    confidence: float
    signal_score: float
    market_data: MarketData
    sentiment_data: SentimentData
    onchain_data: OnChainData
    leverage_suggestion: LeverageSuggestion
    position_info: PositionInfo
    execution_signal: ExecutionSignal
    perp_trade_details: PerpTradeDetails
    reasoning: str
    
    # Flare Network Verification
    ftso_price: float
    fdc_verified: bool
    contract_verified: Optional[bool] = None
    verified: bool
    verification_hash: str
    
    # Enhanced Verification
    component_status: Optional[ComponentStatus] = None
    rules_evaluation: Optional[RulesEvaluation] = None
    tampered: Optional[bool] = False
    
    # Agent-specific fields
    iteration: Optional[int] = None
    agent_status: Optional[str] = None
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
