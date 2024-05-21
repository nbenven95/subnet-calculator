import pytest
from v4._ipv4_calculator import cidr_to_str                     # Implemented
from v4._ipv4_calculator import cidr_to_netmask                 # Implemented
from v4._ipv4_calculator import netmask_to_cidr                 # Implemented
from v4._ipv4_calculator import parse_addr_str                  # Update to reflect new error throws for invalid input       
from v4._ipv4_calculator import get_subnet_class                # Implemented
from v4._ipv4_calculator import get_num_hosts
from v4._ipv4_calculator import get_num_subnets
from v4._ipv4_calculator import get_first_host
from v4._ipv4_calculator import get_last_host
from v4._ipv4_calculator import get_subnet_info_given_mask
from v4._ipv4_calculator import get_subnet_info_given_cidr
from v4._ipv4_calculator import validate_subnet_mask_octet_list as validate_octet_list # Implemented

def test_cidr_to_str():
    """Tests for cidr_to_str( cidr: int ) -> str"""

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

def test_netmask_to_cidr():
    """Tests for netmask_to_cidr( subnet_mask: str ) -> int"""
    
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

def test_parse_addr_str():
    """Tests for parse_addr_str( addr_str: str ) -> list"""
    
    # Test invalid input type
    with pytest.raises( TypeError ) as e_info:
        parse_addr_str( 123456789 )
    with pytest.raises( TypeError ) as e_info:
        parse_addr_str( 3.14 )

    # Test invalid string input
    with pytest.raises( ValueError ) as e_info:
        parse_addr_str( 'invalid' )
    with pytest.raises( ValueError ) as e_info:
        parse_addr_str( '255.255.255' )
    with pytest.raises( ValueError ) as e_info:
        parse_addr_str( '255.255' )
    with pytest.raises( ValueError ) as e_info:
        parse_addr_str( '255' )
    with pytest.raises( ValueError ) as e_info:
        parse_addr_str( '256.255.255.255' )
    with pytest.raises( ValueError ) as e_info:
        parse_addr_str( '255.256.255.255' )
    with pytest.raises( ValueError ) as e_info:
        parse_addr_str( '255.255.256.255' )
    with pytest.raises( ValueError ) as e_info:
        parse_addr_str( '255.255.255.256' )
    with pytest.raises( ValueError ) as e_info:
        parse_addr_str( '9999.2554314321.43255.254' )

    # Test valid input
    assert parse_addr_str( '0.0.0.0' ) == [0,0,0,0]
    assert parse_addr_str( '192.168.10.1' ) == [192,168,10,1]
    assert parse_addr_str( '255.255.255.255' ) == [255,255,255,255]

def test_validate_octet_list():
    """Tests for validate_subnet_mask_octet_list( subnet_mask: list ) -> bool"""

    # Test invalid input type
    with pytest.raises( TypeError ) as e_info:
        validate_octet_list( 123456789 )
    with pytest.raises( TypeError ) as e_info:
        validate_octet_list( '123456789' )
    with pytest.raises( TypeError ) as e_info:
        validate_octet_list( 12345.67890 )
    with pytest.raises( TypeError ) as e_info:
        validate_octet_list( [ 1.0, 2.0, 3.0, 4.0 ] )
    with pytest.raises( TypeError ) as e_info:
        validate_octet_list( [ '1.0', '2.0', '3.0', '4.0' ] )

    # Test invalid list input
    assert validate_octet_list( [ 255, 255, 255 ] ) == False
    assert validate_octet_list( [ 255, 255, 255, 255, 255 ] ) == False
    assert validate_octet_list( [ -255, 255, 255, 128 ] ) == False
    assert validate_octet_list( [ 255, -255, 255, 128 ] ) == False
    assert validate_octet_list( [ 255, 255, -255, 128 ] ) == False
    assert validate_octet_list( [ 255, 255, 255, -128 ] ) == False
    assert validate_octet_list( [ 256, 255, 255, 255 ] ) == False
    assert validate_octet_list( [ 0, 255, 255, 255 ] ) == False
    assert validate_octet_list( [ 254, 253, 252, 251 ] ) == False
    assert validate_octet_list( [ 255, 255, 128, 254 ] ) == False
    
    # Test valid input
    assert validate_octet_list( [ 0, 0, 0, 0 ] ) == True
    assert validate_octet_list( [ 128, 0, 0, 0 ] ) == True
    assert validate_octet_list( [ 192, 0, 0, 0 ] ) == True
    assert validate_octet_list( [ 254, 0, 0, 0 ] ) == True
    assert validate_octet_list( [ 255, 0, 0, 0 ] ) == True
    assert validate_octet_list( [ 255, 128, 0, 0 ] ) == True
    assert validate_octet_list( [ 255, 224, 0, 0 ] ) == True
    assert validate_octet_list( [ 255, 254, 0, 0 ] ) == True
    assert validate_octet_list( [ 255, 255, 0, 0 ] ) == True
    assert validate_octet_list( [ 255, 255, 128, 0 ] ) == True
    assert validate_octet_list( [ 255, 255, 240, 0 ] ) == True
    assert validate_octet_list( [ 255, 255, 254, 0 ] ) == True
    assert validate_octet_list( [ 255, 255, 255, 0 ] ) == True
    assert validate_octet_list( [ 255, 255, 255, 128 ] ) == True
    assert validate_octet_list( [ 255, 255, 255, 248 ] ) == True
    assert validate_octet_list( [ 255, 255, 255, 254 ] ) == True
    assert validate_octet_list( [ 255, 255, 255, 255 ] ) == True

def test_get_subnet_class():
    """Tests for get_subnet_class( subnet_mask: list ) -> str"""

    # Test valid input (invalid input is handled by test_validate_octet_list)
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

'''
Tests for get_num_hosts( wildcard_mask: list ) -> int
'''
def test_get_num_hosts():
    assert True

'''
Tests for get_num_subnets( subnet_mask: list ) -> int
'''
def test_get_num_subnets():
    assert True

'''
Tests for get_first_host( net_id: list ) -> list
'''
def test_get_first_host():
    assert True

'''
Tests for get_last_host( broadcast: list ) -> list
'''
def test_get_last_host():
    assert True

'''
Tests for get_subnet_info_given_mask( ipv4_str: str, subnet_mask_str: str ) -> dict
'''
def test_get_subnet_info_given_mask():
    assert True

'''
Tests for get_subnet_info_given_cidr( ipv4_str: str, cidr: int ) -> dict
'''
def test_get_subnet_info_given_cidr():
    assert True