"""Tests for ipv6_calculator.py"""

from v6.ipv6_calculator import get_grp_len
from v6.ipv6_calculator import remove_grp_len_substr
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
    '::/16',
    '::/128',
    '1:2:3:4:5:6:7:8/1',
    '1:2:3:4:5:6:7:8/64',
    '1:2:3:4:5:6:7:8/128'
]

def test_get_grp_len():
    """Tests for get_grp_len"""
    for valid_ipv6 in VALID_IPV6_ADDR_W_PREFIX_LEN:
        actual = get_grp_len( valid_ipv6 )
        try:
            expected = int( valid_ipv6[ len( valid_ipv6 )-3: ] )# Three-digit (/100 - /128)
            assert actual == expected
        except ValueError:
            try:
                expected = int( valid_ipv6[ len( valid_ipv6 )-2: ] ) # Two-digit (/10 - /99)
                assert actual == expected
            except ValueError:
                expected = int( valid_ipv6[ len( valid_ipv6 )-1: ] ) # Single-digit (/0 - /9)
                assert actual == expected
        
def test_remove_grp_len_substr():
    """Tests for remove_grp_len_substr"""
    assert remove_grp_len_substr( 'fe80::/10' ) == 'fe80::'
    assert remove_grp_len_substr( '1:2:3:4:5:6:7:8/64' ) == '1:2:3:4:5:6:7:8'