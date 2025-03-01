import re
from typing import (
    Optional,
    Tuple)

from hummingbot.client.config.config_var import ConfigVar
from hummingbot.client.config.config_methods import using_exchange


CENTRALIZED = True
EXAMPLE_PAIR = "ZRX-ETH"
DEFAULT_FEES = [0.1, 0.1]

RE_4_LETTERS_QUOTE = re.compile(r"^(\w{3,})(USDT|USDC|USDS|TUSD|BUSD|IDRT|BKRW|BIDR|BVND)$")
RE_3_LETTERS_QUOTE = re.compile(r"^(\w+)(\w{3})$")


def split_trading_pair(trading_pair: str) -> Optional[Tuple[str, str]]:
    try:
        m = RE_4_LETTERS_QUOTE.match(trading_pair)
        if m is None:
            m = RE_3_LETTERS_QUOTE.match(trading_pair)
        return m.group(1), m.group(2)
    # Exceptions are now logged as warnings in trading pair fetcher
    except Exception:
        return None


def convert_from_exchange_trading_pair(exchange_trading_pair: str) -> Optional[str]:
    result = None
    splitted_pair = split_trading_pair(exchange_trading_pair)
    if splitted_pair is not None:
        # Msamex does not split BASEQUOTE (BTCUSDT)
        base_asset, quote_asset = splitted_pair
        result = f"{base_asset}-{quote_asset}"
    return result


def convert_to_exchange_trading_pair(hb_trading_pair: str) -> str:
    # Msamex does not split BASEQUOTE (BTCUSDT)
    return hb_trading_pair.replace("-", "")


KEYS = {
    "msamex_api_key":
        ConfigVar(key="msamex_api_key",
                  prompt="Enter your Binance API key >>> ",
                  required_if=using_exchange("msamex"),
                  is_secure=True,
                  is_connect_key=True),
    "msamex_api_secret":
        ConfigVar(key="msamex_api_secret",
                  prompt="Enter your Binance API secret >>> ",
                  required_if=using_exchange("msamex"),
                  is_secure=True,
                  is_connect_key=True),
}



