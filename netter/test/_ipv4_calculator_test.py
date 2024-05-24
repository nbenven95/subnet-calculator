"""Tests for _ipv4_validator.py"""

#|#############################################################| Imports |##############################################################|#

from v4._ipv4_calculator import parse_addr_str 
from v4._ipv4_calculator import get_network_id
from v4._ipv4_calculator import get_wildcard_mask
from v4._ipv4_calculator import get_broadcast_addr
from v4._ipv4_calculator import get_num_hosts
from v4._ipv4_calculator import get_num_subnets
from v4._ipv4_calculator import get_subnet_class
from v4._ipv4_calculator import get_first_host
from v4._ipv4_calculator import get_last_host
from v4._ipv4_calculator import netmask_to_cidr
from v4._ipv4_calculator import cidr_to_netmask
from v4._ipv4_calculator import cidr_to_str
from v4._ipv4_calculator import get_subnet_info_given_mask
from v4._ipv4_calculator import get_subnet_info_given_cidr
import pytest

#|#######################################################| Function definitions |#######################################################|#

def test_parse_addr_str():
    assert True

def test_get_network_id():
    assert True

def test_get_wildcard_mask():
    assert True

def test_get_broadcast_addr():
    assert True

def test_get_num_hosts():
    assert True

def test_get_num_subnets():
    assert True

def test_get_subnet_class():
    assert True

def test_get_first_host():
    assert True

def test_get_last_host():
    assert True

def test_netmask_to_cidr():
    assert True

def test_cidr_to_netmask():
    assert True

def test_cidr_to_str():
    # Test invalid input type
    with pytest.raises( TypeError ) as e_info:
        cidr_to_str( '16' )
    with pytest.raises( TypeError ) as e_info:
        cidr_to_str( 16.0 )
    # Test invalid integer input
    with pytest.raises( ValueError ) as e_info:
        cidr_to_str( -999 )
    with pytest.raises( ValueError ) as e_info:
        cidr_to_str( -1 )
    with pytest.raises( ValueError ) as e_info:
        cidr_to_str( 33 )
    with pytest.raises( ValueError ) as e_info:
        cidr_to_str( 999 )
    # Test valid integer input
    assert cidr_to_str( 0 ) == '/0'
    assert cidr_to_str( 1 ) == '/1'
    assert cidr_to_str( 7 ) == '/7'
    assert cidr_to_str( 8 ) == '/8'
    assert cidr_to_str( 9 ) == '/9'
    assert cidr_to_str( 15 ) == '/15'
    assert cidr_to_str( 16 ) == '/16'
    assert cidr_to_str( 17 ) == '/17'
    assert cidr_to_str( 23 ) == '/23'
    assert cidr_to_str( 24 ) == '/24'
    assert cidr_to_str( 25 ) == '/25'
    assert cidr_to_str( 31 ) == '/31'
    assert cidr_to_str( 32 ) == '/32'

def test_get_subnet_info_given_mask():
    assert True

def test_get_subnet_info_given_cidr():
    assert True