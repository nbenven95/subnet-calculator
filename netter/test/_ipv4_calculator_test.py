"""Tests for _ipv4_calculator.py"""

from v4.ipv4_calculator import parse_addr_str 
from v4.ipv4_calculator import get_network_id
from v4.ipv4_calculator import get_wildcard_mask
from v4.ipv4_calculator import get_broadcast_addr
from v4.ipv4_calculator import get_num_hosts
from v4.ipv4_calculator import get_num_subnets
from v4.ipv4_calculator import get_subnet_class
from v4.ipv4_calculator import get_first_host
from v4.ipv4_calculator import get_last_host
from v4.ipv4_calculator import netmask_to_cidr
from v4.ipv4_calculator import cidr_to_netmask
from v4.ipv4_calculator import cidr_to_str
from v4.ipv4_calculator import get_subnet_info_given_mask
from v4.ipv4_calculator import get_subnet_info_given_cidr
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
    ### Class (none) ###
    assert get_network_id( [0,0,0,0], [0,0,0,0] ) == [0,0,0,0] # /0
    # Need to handle /0 as an edge case to only allow 0.0.0.0 0.0.0.0 and output information regarding default routes, possibly link to documentation
    assert get_network_id( [10,1,5,7], [0,0,0,0] ) == [0,0,0,0] # /0 semantically incorrect, mathematically correct
    assert get_network_id( [178,254,16,226], [128,0,0,0] ) == [128,0,0,0] # /1
    assert get_network_id( [70,41,146,175], [224,0,0,0] ) == [64,0,0,0] # /3
    assert get_network_id( [69,255,255,254], [254,0,0,0] ) == [68,0,0,0] # /7
    ### Class A ###
    assert get_network_id( [51,128,200,1], [255,0,0,0] ) == [51,0,0,0] # /8
    assert get_network_id( [231,217,0,1], [255,240,0,0] ) == [231,208,0,0] # /12
    assert get_network_id( [100,75,100,100], [255,254,0,0] ) == [100,74,0,0] # /15
    ### Class B ###
    assert get_network_id( [99,99,99,99], [255,255,0,0] ) == [99,99,0,0] # /16
    assert get_network_id( [101,102,103,104], [255,255,240,0] ) == [101,102,96,0] # /20
    assert get_network_id( [199,17,97,201], [199,17,96,0] ) # /23
    ### Class C ### 
    assert get_network_id( [192,168,10,1], [255,255,255,0] ) == [192,168,10,0] # /24
    assert get_network_id( [172,31,16,24], [255,255,255,192] ) == [172,31,16,0] # /26
    assert get_network_id( [10,0,0,9], [255,255,255,252] ) == [10,0,0,8] # /30
    # Should handle with edge case -> 2 addresses, 0 usable hosts (first address is network ID, second address is broadcast) -> provide link to documentation
    assert get_network_id( [1,0,0,5], [255,255,255,254] ) == [1,0,0,4] # /31
    # Should handle with edge case -> 1 address, 0 usable hosts, network ID = broadcast -> look into documentation for use cases
    assert get_network_id( [1,1,1,1], [255,255,255,255] ) == [1,1,1,1] # /32

def test_get_wildcard_mask():
    """Tests for get_wildcard_mask"""
    ### Class (none) ###
    ### Class A ###
    ### Class B ###
    ### Class C ###
    assert True

def test_get_broadcast_addr():
    """Tests for get_broadcast_addr"""
    ### Class (none) ###
    ### Class A ###
    ### Class B ###
    ### Class C ###
    assert True

def test_get_num_hosts():
    """Tests for get_num_hosts"""
    ### Class (none) ###
    assert get_num_hosts( [128,0,0,0] ) == 2147483646
    ### Class A ###
    ### Class B ###
    ### Class C ###
    assert True

def test_get_num_subnets():
    """Tests for get_num_subnets"""
    ### Class (none) ###
    ### Class A ###
    ### Class B ###
    ### Class C ###
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

    # Currently failing: wildcard mask, broadcast (due to wildcard), last host (due to wildcard), number of hosts (due to wildcard), and number of subnets (separate issue possibly).
    # Wildcard issue seems to be due to unexpected behavior from bitwise_not from numpy. e.g. 255.255.255.0 should be 0.0.0.255, not -256.-256.-256.-1

    """Tests for get_subnet_info_given_mask"""
    ##### Test valid input #####
    ### Class (none) ###
    expected = {'ipv4':'254.172.75.42','network_id':'128.0.0.0','subnet_mask':'128.0.0.0','wildcard_mask':'127.255.255.255','cidr_int':1,'cidr_str':'/1','subnet_class':'none','first_host':'128.0.0.1','last_host':'255.255.255.254','broadcast':'255.255.255.255','num_hosts':2147483646,'num_subnets':2}
    assert get_subnet_info_given_mask( '254.172.75.42', '128.0.0.0' ) == expected
    #expected = {'network_id':'','subnet_mask':'','wildcard_mask':'','cidr_int':'','cidr_str':'','subnet_class':'','first_host':'','last_host':'','broadcast':'','num_hosts' :'','num_subnets':''}
    #assert get_subnet_info_given_mask( '203.99.175.27', '254.0.0.0' ) == expected
    ### Class A ###
    ### Class B ###
    ### Class C ###
    expected = {'ipv4':'192.168.10.4','network_id':'192.168.10.0','subnet_mask':'255.255.255.0','wildcard_mask':'0.0.0.255','cidr_int':24,'cidr_str':'/24','subnet_class':'C','first_host':'192.168.10.1','last_host':'192.168.10.254','broadcast':'192.168.10.255','num_hosts':254,'num_subnets':1}
    assert get_subnet_info_given_mask( '192.168.10.4', '255.255.255.0' ) == expected
    assert True


def test_get_subnet_info_given_cidr():
    """Tests for get_subnet_info_given_cidr"""
    assert True