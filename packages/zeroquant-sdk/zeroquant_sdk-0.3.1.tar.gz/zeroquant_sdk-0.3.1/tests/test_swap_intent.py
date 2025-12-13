# packages/python-sdk/tests/test_swap_intent.py
import pytest
from zeroquant.intents.swap import SwapIntent
import time

def test_calculate_min_output():
    intent = SwapIntent("0x" + "a" * 40)

    expected = 2000_000000  # 2000 USDC
    min_output = intent.calculate_min_output(expected, 50)  # 0.5% slippage

    # Should be 99.5% of expected
    assert min_output == expected * 9950 // 10000

def test_get_deadline():
    intent = SwapIntent("0x" + "a" * 40)

    deadline = intent.get_deadline(3600)
    now = int(time.time())

    assert deadline > now
    assert deadline <= now + 3600 + 5  # Allow 5 second margin

def test_build_calldata():
    intent = SwapIntent("0x" + "a" * 40)

    calldata = intent.build_calldata(
        amount_in=10**18,
        amount_out_min=1990 * 10**6,
        path=["0x" + "b" * 40, "0x" + "c" * 40],
        to="0x" + "d" * 40,
        deadline=1234567890
    )

    assert calldata.startswith(b'\x6e\xf2\xb9\xc8')  # executeSwap selector
