"""Chainlink price oracle service for ZeroQuant."""

from typing import Dict, Optional
from web3 import AsyncWeb3
import time

# Chainlink Aggregator V3 ABI (minimal)
CHAINLINK_AGGREGATOR_ABI = [
    {
        "inputs": [],
        "name": "latestRoundData",
        "outputs": [
            {"name": "roundId", "type": "uint80"},
            {"name": "answer", "type": "int256"},
            {"name": "startedAt", "type": "uint256"},
            {"name": "updatedAt", "type": "uint256"},
            {"name": "answeredInRound", "type": "uint80"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function",
    },
]

# Chainlink price feed addresses by network
PRICE_FEEDS: Dict[str, Dict[str, str]] = {
    "mainnet": {
        "ETH/USD": "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419",
        "BTC/USD": "0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c",
        "USDC/USD": "0x8fFfFfd4AfB6115b954Bd326cbe7B4BA576818f6",
        "DAI/USD": "0xAed0c38402a5d19df6E4c03F4E2DceD6e29c1ee9",
        "LINK/USD": "0x2c1d072e956AFFC0D435Cb7AC38EF18d24d9127c",
    },
    "sepolia": {
        "ETH/USD": "0x694AA1769357215DE4FAC081bf1f309aDC325306",
        "BTC/USD": "0x1b44F3514812d835EB1BDB0acB33d3fA3351Ee43",
        "LINK/USD": "0xc59E3633BAAC79493d908e63626716e204A45EdF",
    },
}

# Token address to price feed mapping (mainnet, checksummed)
TOKEN_TO_FEED: Dict[str, str] = {
    # WETH
    "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2": "ETH/USD",
    # WBTC
    "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599": "BTC/USD",
    # USDC
    "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48": "USDC/USD",
    # DAI (correct mainnet address)
    "0x6B175474E89094C44Da98b954EedeAC495271d0F": "DAI/USD",
    # LINK
    "0x514910771AF9Ca656af840dff83E8264EcF986CA": "LINK/USD",
}

# Cache settings
CACHE_TTL_SECONDS = 60  # 1 minute


class PriceCache:
    """Simple price cache."""

    def __init__(self):
        self._cache: Dict[str, tuple] = {}  # pair -> (price, timestamp)

    def get(self, key: str) -> Optional[float]:
        """Get cached price if still valid."""
        if key in self._cache:
            price, timestamp = self._cache[key]
            if time.time() - timestamp < CACHE_TTL_SECONDS:
                return price
        return None

    def set(self, key: str, price: float) -> None:
        """Cache a price."""
        self._cache[key] = (price, time.time())


_price_cache = PriceCache()


class ChainlinkPriceService:
    """Service for fetching prices from Chainlink oracles."""

    def __init__(self, w3: AsyncWeb3, network: str = "mainnet"):
        """
        Initialize the price service.

        Args:
            w3: AsyncWeb3 instance
            network: Network name (mainnet, sepolia, etc.)
        """
        self.w3 = w3
        self.network = network

    async def get_pair_price(self, pair: str) -> float:
        """
        Get the price for a specific pair from Chainlink.

        Args:
            pair: Price pair (e.g., "ETH/USD")

        Returns:
            Price as a float
        """
        cache_key = f"{self.network}:{pair}"

        # Check cache first
        cached = _price_cache.get(cache_key)
        if cached is not None:
            return cached

        feed_address = PRICE_FEEDS.get(self.network, {}).get(pair)
        if not feed_address:
            raise ValueError(f"No price feed found for {pair} on {self.network}")

        try:
            contract = self.w3.eth.contract(
                address=self.w3.to_checksum_address(feed_address),
                abi=CHAINLINK_AGGREGATOR_ABI,
            )

            # Get latest round data
            round_data = await contract.functions.latestRoundData().call()
            answer = round_data[1]
            updated_at = round_data[3]

            # Get decimals
            decimals = await contract.functions.decimals().call()

            # Check for stale price (older than 1 hour)
            now = int(time.time())
            if now - updated_at > 3600:
                print(f"Warning: Chainlink price for {pair} is stale")

            # Convert to float with proper decimals
            price = float(answer) / (10 ** decimals)

            # Cache the price
            _price_cache.set(cache_key, price)

            return price

        except Exception as e:
            print(f"Failed to fetch {pair} price: {e}")
            # Return cached price if available (even if stale)
            if cache_key in _price_cache._cache:
                return _price_cache._cache[cache_key][0]
            raise

    async def get_eth_price(self) -> float:
        """Get ETH/USD price."""
        return await self.get_pair_price("ETH/USD")

    async def get_token_price_usd(self, token_address: str) -> float:
        """
        Get the USD price of a token.

        Args:
            token_address: Token contract address

        Returns:
            Token price in USD
        """
        # Normalize address
        checksummed = self.w3.to_checksum_address(token_address)

        pair = TOKEN_TO_FEED.get(checksummed)
        if not pair:
            # If no direct feed, assume stablecoin
            print(f"Warning: No price feed for {token_address}, assuming $1")
            return 1.0

        return await self.get_pair_price(pair)

    async def get_expected_swap_output(
        self, from_token: str, to_token: str, amount_in: int
    ) -> int:
        """
        Calculate expected output for a swap using price feeds.

        Args:
            from_token: Input token address
            to_token: Output token address
            amount_in: Input amount in wei

        Returns:
            Expected output amount in wei
        """
        from_price = await self.get_token_price_usd(from_token)
        to_price = await self.get_token_price_usd(to_token)

        # Calculate: (amount_in * from_price) / to_price
        from_value_usd = float(amount_in) * from_price
        expected_output = from_value_usd / to_price

        return int(expected_output)

    async def wei_to_usd(self, wei_value: int) -> float:
        """
        Convert wei to USD.

        Args:
            wei_value: Value in wei

        Returns:
            USD value
        """
        eth_price = await self.get_eth_price()
        eth_value = wei_value / 10**18
        return eth_value * eth_price


# Singleton instance
_price_service_instance: Optional[ChainlinkPriceService] = None


def get_price_service(
    w3: AsyncWeb3, network: str = "mainnet"
) -> ChainlinkPriceService:
    """Get or create the price service singleton."""
    global _price_service_instance
    if _price_service_instance is None:
        _price_service_instance = ChainlinkPriceService(w3, network)
    return _price_service_instance
