"""
VERDICT SDK Client - Main client for interacting with VERDICT API.
"""

import asyncio
import time
from typing import Optional, Callable, AsyncGenerator
from urllib.parse import urljoin

import httpx
from pydantic import ValidationError

from .models import AnalysisResponse, RiskLevel
from .exceptions import (
    VerdictAPIError,
    VerdictAuthError,
    VerdictRateLimitError,
    VerdictValidationError,
    VerdictConnectionError,
)


class VerdictClient:
    """
    VERDICT SDK Client for crypto trading analysis.
    
    This client requires users to provide their own API keys (BYOK model):
    - CoinMarketCap API key for market data
    - Google Gemini API key for AI sentiment analysis
    
    Example:
        ```python
        from verdict_sdk import VerdictClient
        
        client = VerdictClient(
            api_url="https://verdict-api.example.com",
            cmc_api_key="your_cmc_key",
            gemini_api_key="your_gemini_key"
        )
        
        # Get a single analysis
        result = client.analyze(
            token="BTC",
            stablecoin="USDC",
            portfolio_amount=1000.0,
            risk_level="moderate"
        )
        
        print(f"Recommendation: {result.recommendation}")
        print(f"Confidence: {result.confidence}%")
        ```
    """

    def __init__(
        self,
        api_url: str,
        cmc_api_key: str,
        gemini_api_key: str,
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        """
        Initialize VERDICT client.
        
        Args:
            api_url: Base URL of the VERDICT API (e.g., "https://verdict-api.example.com")
            cmc_api_key: Your CoinMarketCap API key
            gemini_api_key: Your Google Gemini API key
            timeout: Request timeout in seconds (default: 30)
            max_retries: Maximum number of retries for failed requests (default: 3)
        """
        self.api_url = api_url.rstrip("/")
        self.cmc_api_key = cmc_api_key
        self.gemini_api_key = gemini_api_key
        self.timeout = timeout
        self.max_retries = max_retries
        
        # HTTP client configuration
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            follow_redirects=True,
        )
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    def _handle_error(self, response: httpx.Response):
        """Handle HTTP error responses."""
        if response.status_code == 401 or response.status_code == 403:
            raise VerdictAuthError(
                f"Authentication failed. Please check your API keys. Status: {response.status_code}"
            )
        elif response.status_code == 429:
            raise VerdictRateLimitError(
                "Rate limit exceeded. Please wait before making more requests."
            )
        elif response.status_code == 422:
            raise VerdictValidationError(
                f"Request validation failed: {response.text}"
            )
        elif response.status_code >= 500:
            raise VerdictAPIError(
                f"Server error: {response.status_code} - {response.text}"
            )
        else:
            raise VerdictAPIError(
                f"API error: {response.status_code} - {response.text}"
            )
    
    async def analyze(
        self,
        token: str,
        stablecoin: str = "USDC",
        portfolio_amount: float = 100.0,
        risk_level: str = "moderate",
    ) -> AnalysisResponse:
        """
        Perform a single trading analysis.
        
        Args:
            token: Token symbol to analyze (e.g., "BTC", "ETH", "APT")
            stablecoin: Collateral stablecoin (default: "USDC")
            portfolio_amount: Amount of stablecoin to trade (default: 100.0)
            risk_level: Risk level - "conservative", "moderate", or "aggressive" (default: "moderate")
        
        Returns:
            AnalysisResponse with full trading analysis
        
        Raises:
            VerdictAPIError: If the API request fails
            VerdictAuthError: If authentication fails
            VerdictValidationError: If request parameters are invalid
        
        Example:
            ```python
            result = await client.analyze(
                token="BTC",
                portfolio_amount=1000,
                risk_level="moderate"
            )
            print(f"{result.recommendation} with {result.confidence}% confidence")
            ```
        """
        url = urljoin(self.api_url, "/api/analyze")
        
        payload = {
            "token": token.upper(),
            "stablecoin": stablecoin.upper(),
            "portfolio_amount": portfolio_amount,
            "risk_level": risk_level,
            "cmc_api_key": self.cmc_api_key,
            "gemini_api_key": self.gemini_api_key,
        }
        
        for attempt in range(self.max_retries):
            try:
                response = await self.client.post(url, json=payload)
                
                if response.status_code == 200:
                    try:
                        return AnalysisResponse(**response.json())
                    except ValidationError as e:
                        raise VerdictValidationError(f"Invalid response format: {e}")
                else:
                    self._handle_error(response)
                    
            except httpx.RequestError as e:
                if attempt == self.max_retries - 1:
                    raise VerdictConnectionError(f"Connection failed after {self.max_retries} attempts: {e}")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    async def activate_agent(
        self,
        token: str,
        stablecoin: str = "USDC",
        portfolio_amount: float = 100.0,
        risk_level: str = "moderate",
    ) -> dict:
        """
        Activate a real-time analysis agent.
        
        The agent will continuously analyze the market and update results every second.
        Use the `get_status()` method or `stream_agent()` to receive updates.
        
        Args:
            token: Token symbol to analyze
            stablecoin: Collateral stablecoin (default: "USDC")
            portfolio_amount: Amount of stablecoin to trade
            risk_level: Risk level (default: "moderate")
        
        Returns:
            Dict with session_id and status
        
        Example:
            ```python
            response = await client.activate_agent(token="BTC", portfolio_amount=1000)
            session_id = response["session_id"]
            
            # Stream updates
            async for update in client.stream_agent(session_id, interval=1.0):
                print(f"Price: ${update.market_data.price:.2f}")
            ```
        """
        url = urljoin(self.api_url, "/api/activate")
        
        payload = {
            "token": token.upper(),
            "stablecoin": stablecoin.upper(),
            "portfolio_amount": portfolio_amount,
            "risk_level": risk_level,
            "cmc_api_key": self.cmc_api_key,
            "gemini_api_key": self.gemini_api_key,
        }
        
        response = await self.client.post(url, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            self._handle_error(response)
    
    async def deactivate_agent(self, session_id: str) -> dict:
        """
        Deactivate a running agent.
        
        Args:
            session_id: Session ID from activate_agent response
        
        Returns:
            Dict with deactivation status
        """
        url = urljoin(self.api_url, "/api/deactivate")
        
        payload = {"session_id": session_id}
        response = await self.client.post(url, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            self._handle_error(response)
    
    async def get_status(self, session_id: str) -> AnalysisResponse:
        """
        Get current status of an active agent.
        
        Args:
            session_id: Session ID from activate_agent response
        
        Returns:
            Latest AnalysisResponse from the agent
        """
        url = urljoin(self.api_url, f"/api/status/{session_id}")
        
        response = await self.client.get(url)
        
        if response.status_code == 200:
            try:
                return AnalysisResponse(**response.json())
            except ValidationError as e:
                raise VerdictValidationError(f"Invalid response format: {e}")
        else:
            self._handle_error(response)
    
    async def stream_agent(
        self,
        token: str,
        stablecoin: str = "USDC",
        portfolio_amount: float = 100.0,
        risk_level: str = "moderate",
        interval: float = 1.0,
        callback: Optional[Callable[[AnalysisResponse], None]] = None,
    ) -> AsyncGenerator[AnalysisResponse, None]:
        """
        Stream real-time updates by polling the analyze endpoint.
        
        This is a convenience method that repeatedly calls analyze() to simulate streaming.
        
        Args:
            token: Token symbol to analyze
            stablecoin: Collateral stablecoin
            portfolio_amount: Amount of stablecoin to trade
            risk_level: Risk level
            interval: Polling interval in seconds (default: 1.0)
            callback: Optional callback function to call with each update
        
        Yields:
            AnalysisResponse objects with real-time updates
        
        Example:
            ```python
            async for analysis in client.stream_agent(token="BTC", interval=1.0):
                print(f"Price: ${analysis.market_data.price:.2f}")
                print(f"Recommendation: {analysis.recommendation}")
                
                if analysis.recommendation == "LONG":
                    # Execute trade logic
                    break
            ```
        """
        while True:
            try:
                result = await self.analyze(
                    token=token,
                    stablecoin=stablecoin,
                    portfolio_amount=portfolio_amount,
                    risk_level=risk_level,
                )
                
                if callback:
                    callback(result)
                
                yield result
                
            except Exception as e:
                print(f"Error in stream_agent: {e}")
                # Continue streaming even if one request fails
            
            await asyncio.sleep(interval)
    
    # Synchronous wrappers for convenience
    def analyze_sync(
        self,
        token: str,
        stablecoin: str = "USDC",
        portfolio_amount: float = 100.0,
        risk_level: str = "moderate",
    ) -> AnalysisResponse:
        """
        Synchronous version of analyze().
        
        This is a convenience wrapper for users who prefer synchronous code.
        For better performance, use the async version.
        """
        return asyncio.run(
            self.analyze(token, stablecoin, portfolio_amount, risk_level)
        )
