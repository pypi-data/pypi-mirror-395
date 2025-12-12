import hashlib


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def gas_fee(gas_used: int, gwei: float, eth_price: float) -> float:
    """
    Rough ETH gas fee in USD.
    gas_used: e.g. 21000
    gwei: gas price in gwei
    eth_price: price of 1 ETH in USD
    """
    # 1 gwei = 1e-9 ETH
    eth_fee = gas_used * gwei * 1e-9
    return eth_fee * eth_price
