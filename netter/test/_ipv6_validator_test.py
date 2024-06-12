"""Tests for _ipv6_validator.py"""

from v6.ipv6_validator import is_valid_ipv6
import pytest

# Valid IPv6 addresses to test
VALID_IPV6_ADDR = [
    '1::',
    '1:2:3:4:5:6:7::',
    '1::8',
    '1:2:3:4:5:6::8',
    '1:2:3:4:5:6::8',
    '1::7:8',
    '1:2:3:4:5::7:8',
    '1:2:3:4:5::8',
    '1::6:7:8',
    '1:2:3:4::6:7:8',
    '1:2:3:4::8',
    '1::5:6:7:8',
    '1:2:3::5:6:7:8',
    '1:2:3::8',
    '1::4:5:6:7:8',
    '1:2::4:5:6:7:8',
    '1:2::8',
    '1::3:4:5:6:7:8',
    '1::3:4:5:6:7:8',
    '1::8',
    '::2:3:4:5:6:7:8',
    '::2:3:4:5:6:7:8',
    '::8',
    '::',
    'fe80::7:8%eth0',
    'fe80::7:8%1',
    '::255.255.255.255',
    '::ffff:255.255.255.255',
    '::ffff:0:255.255.255.255',
    '2001:db8:3:4::192.0.2.33',
    '64:ff9b::192.0.2.33',
    '0:0:0:0:0:0:10.0.0.1',
    # Test for correct GRP length pattern match
    '::/0',
    '1::/1',
    '1::/9',
    '1::/10',
    '1::/59',
    '1::/60',
    '1::/64',
]

# Invalid IPv6 addresses to test
INVALID_IPV6_ADDR = [
    '1:',
    '1:::',
    ':::',
    '1:2',
    '1:2:3:4',
    '1:2:3:4:5:6:7:8:9',
    '1::2:3::4:5:6:7:8'
    '1::2:3::4:5:6::7:8'
    '1::::::2:3:4:5:6:7:8',
    # Test for incorrect GRP length pattern match
    '::/',
    '1::/',
    '1:/1',
    '1::/65',
    '1::/644'
]

def test_is_valid_ipv6():
    """Tests for is_valid_ipv6"""
    # Test single address valid input
    for valid_ipv6 in VALID_IPV6_ADDR:
        assert is_valid_ipv6( valid_ipv6 )
    # Test single address invalid input
    for invalid_ipv6 in INVALID_IPV6_ADDR:
        assert not is_valid_ipv6( invalid_ipv6 )
    

