"""Tests for _ipv4_calculator.py"""

#|#######################################################################| Imports |########################################################################|#

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

#|#################################################################| Function definitions |#################################################################|#

def test_parse_addr_str():
    """Tests for parse_addr_str"""
    # Test invalid input type
    with pytest.raises( TypeError ) as e_info:
        parse_addr_str( 19216801 )
    with pytest.raises( TypeError ) as e_info:
        parse_addr_str( 192168.01 )
    with pytest.raises( TypeError ) as e_info:
        parse_addr_str( [192,168,0,1] )
    # Test valid IPv4 address structure
    assert parse_addr_str( '0.0.0.0' ) == [0,0,0,0]
    assert parse_addr_str( '10.0.1.254' ) == [10,0,1,254]
    assert parse_addr_str( '192.168.10.1' ) == [192,168,10,1]
    assert parse_addr_str( '255.255.255.255' ) == [255,255,255,255]

def test_get_network_id():
    """Tests for get_network_id"""
    assert True

def test_get_wildcard_mask():
    """Tests for get_wildcard_mask"""
    assert True

def test_get_broadcast_addr():
    """Tests for get_broadcast_addr"""
    assert True

def test_get_num_hosts():
    """Tests for get_num_hosts"""
    assert True

def test_get_num_subnets():
    """Tests for get_num_subnets"""
    assert True

def test_get_subnet_class():
    """Tests for get_subnet_class"""
    # Test valid input (don't bother with invalid, assume that everything has been validated at this point)
    assert get_subnet_class( [0,0,0,0] ) == 'none'
    assert get_subnet_class( [254,0,0,0] ) == 'none'
    assert get_subnet_class( [255,0,0,0] ) == 'A'
    assert get_subnet_class( [255,128,0,0] ) == 'A'
    assert get_subnet_class( [255,254,0,0] ) == 'A'
    assert get_subnet_class( [255,255,0,0] ) == 'B'
    assert get_subnet_class( [255,255,128,0] ) == 'B'
    assert get_subnet_class( [255,255,254,0] ) == 'B'
    assert get_subnet_class( [255,255,255,0] ) == 'C'
    assert get_subnet_class( [255,255,255,128] ) == 'C'
    assert get_subnet_class( [255,255,255,254] ) == 'C'
    assert get_subnet_class( [255,255,255,255] ) == 'C'

def test_get_first_host():
    """Tests for get_first_host"""
    assert True

def test_get_last_host():
    """Tests for get_last_host"""
    assert True

def test_netmask_to_cidr():
    """Tests for netmask_to_cidr"""
    # Test invalid input type
    with pytest.raises( TypeError ) as e_info:
        netmask_to_cidr( 123456789 )
    with pytest.raises( TypeError ) as e_info:
        netmask_to_cidr( 3.14 )
    # Test invalid string input
    with pytest.raises( ValueError ) as e_info:
        netmask_to_cidr( 'invalid' )
    with pytest.raises( ValueError ) as e_info:
        netmask_to_cidr( '254.255.255.0' )
    # Test valid input
    assert netmask_to_cidr( '0.0.0.0' ) == 0
    assert netmask_to_cidr( '128.0.0.0' ) == 1
    assert netmask_to_cidr( '254.0.0.0' ) == 7
    assert netmask_to_cidr( '255.0.0.0' ) == 8
    assert netmask_to_cidr( '255.128.0.0' ) == 9
    assert netmask_to_cidr( '255.254.0.0' ) == 15
    assert netmask_to_cidr( '255.255.0.0' ) == 16
    assert netmask_to_cidr( '255.255.128.0' ) == 17
    assert netmask_to_cidr( '255.255.254.0' ) == 23
    assert netmask_to_cidr( '255.255.255.0' ) == 24
    assert netmask_to_cidr( '255.255.255.128' ) == 25
    assert netmask_to_cidr( '255.255.255.254' ) == 31
    assert netmask_to_cidr( '255.255.255.255' ) == 32

def test_cidr_to_netmask():
    """Tests for cidr_to_netmask( cidr: int ) -> str"""
    # Test invalid input type
    with pytest.raises( TypeError ) as e_info:
        cidr_to_netmask( '16' )
    with pytest.raises( TypeError ) as e_info:
        cidr_to_netmask( 16.0 )
    # Test invalid integer input
    with pytest.raises( ValueError ) as e_info:
        cidr_to_netmask( -999 )
    with pytest.raises( ValueError ) as e_info:
        cidr_to_netmask( -1 )
    with pytest.raises( ValueError ) as e_info:
        cidr_to_netmask( 33 )
    with pytest.raises( ValueError ) as e_info:
        cidr_to_netmask( 999 )
    # Test valid inputs
    assert cidr_to_netmask( 0 ) == '0.0.0.0'
    assert cidr_to_netmask( 1 ) == '128.0.0.0'
    assert cidr_to_netmask( 7 ) == '254.0.0.0'
    assert cidr_to_netmask( 8 ) == '255.0.0.0'
    assert cidr_to_netmask( 9 ) == '255.128.0.0'
    assert cidr_to_netmask( 15 ) == '255.254.0.0'
    assert cidr_to_netmask( 16 ) == '255.255.0.0'
    assert cidr_to_netmask( 17 ) == '255.255.128.0'
    assert cidr_to_netmask( 23 ) == '255.255.254.0'
    assert cidr_to_netmask( 24 ) == '255.255.255.0'
    assert cidr_to_netmask( 25 ) == '255.255.255.128'
    assert cidr_to_netmask( 31 ) == '255.255.255.254'
    assert cidr_to_netmask( 32 ) == '255.255.255.255'

def test_cidr_to_str():
    """Tests for cidr_to_str"""
    # Test invalid input type
    with pytest.raises( TypeError ) as e_info:
        cidr_to_str( '16' )
    with pytest.raises( TypeError ) as e_info:
        cidr_to_str( 16.0 )
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
    """Tests for get_subnet_info_given_mask"""
    ### Test valid input ###
    # Class: none
    expected = {'network_id':'','subnet_mask':'','wildcard_mask':'','cidr_int':'','cidr_str':'','subnet_class':'','first_host':'','last_host':'','broadcast':'','num_hosts' :'','num_subnets':''}
    #assert get_subnet_info_given_mask( '254.172.75.42', '128.0.0.0' ) == expected
    expected = {'network_id':'','subnet_mask':'','wildcard_mask':'','cidr_int':'','cidr_str':'','subnet_class':'','first_host':'','last_host':'','broadcast':'','num_hosts' :'','num_subnets':''}
    #assert get_subnet_info_given_mask( '203.99.175.27', '254.0.0.0' ) == expected
    # Class: A
    # Class: B
    # Class: C
    assert True


def test_get_subnet_info_given_cidr():
    """Tests for get_subnet_info_given_cidr"""
    assert True