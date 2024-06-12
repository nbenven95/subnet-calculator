"""Tests for ipv6_calculator.py"""

from v6.ipv6_calculator import get_grp_len
import pytest

VALID_IPV6_ADDR_W_PREFIX_LEN = [
    '::/0',
    '::/1',
    '::/2',
    '::/3',
    '::/4',
    '::/5',
    '::/6',
    '::/7',
    '::/8',
    '::/9',
    '::/10',
    '::/11',
    '::/12',
    '::/13',
    '::/14',
    '::/15',
    '::/16'
]

def test_get_grp_len():
    """Tests for get_grp_len"""
    index = 0
    for valid_ipv6 in VALID_IPV6_ADDR_W_PREFIX_LEN:
        assert get_grp_len( valid_ipv6 ) == index
        index+=1