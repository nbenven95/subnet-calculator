"""
Calculates detailed IPv4 subnet information given an arbitrary IPv4 address and subnet mask/CIDR value.

Author: Noah Benveniste
https://github.com/noahbenveniste/subnet-calculator
"""
# - get_subnet_info_given_mask  TODO: test
# - get_subnet_info_given_cidr  TODO: test
# - cidr_to_netmask             TODO:
# - netmask_to_cidr             TODO:
# - parse_addr_str              TODO: 
# - get_first_host              TODO: test, handle edge case for /0, /31 and /32 subnets
# - get_last_host               TODO: test, handle edge case for /0, /31 and /32 subnets
# - get_subnet_class            TODO: 
# - get_num_hosts               TODO: test, handle edge case for /0, /31 and /32 subnets
# - get_num_subnets             TODO: test, handle edge case for /0, /31 and /32 subnets
# - cidr_to_str                 TODO: 
# - validate_octet_list

#|#############################################################| Imports |##############################################################|#

from v4._ipv4_validator import argument_type_validator as arg_valid
from itertools          import chain
from numpy              import bitwise_and
from numpy              import bitwise_or
from numpy              import bitwise_not
from numpy              import binary_repr
from numpy              import prod
from re                 import split

#|##################################################| CIDR to subnet mask dictionary |##################################################|#

CIDR_DICT = {
    # No subnet, i.e. any address in the 2^32 IPv4 address space TODO: Implement an edge case to handle this
    0 : '0.0.0.0',
    # /1 - /7 subnets (not sure how to label, just using 'class: none' for now)
    1 : '128.0.0.0',
    2 : '192.0.0.0',
    3 : '224.0.0.0',
    4 : '240.0.0.0',
    5 : '248.0.0.0',
    6 : '252.0.0.0',
    7 : '254.0.0.0',
    # Class A subnets (subnetted class A network)
    8 : '255.0.0.0',
    9 : '255.128.0.0',
    10 : '255.192.0.0',
    11 : '255.224.0.0',
    12 : '255.240.0.0',
    13 : '255.248.0.0',
    14 : '255.252.0.0',
    15 : '255.254.0.0',
    # Class B subnets (subnetted class B network)
    16 : '255.255.0.0',
    17 : '255.255.128.0',
    18 : '255.255.192.0',
    19 : '255.255.224.0',
    20 : '255.255.240.0',
    21 : '255.255.248.0',
    22 : '255.255.252.0',
    23 : '255.255.254.0',
    # Class C subnets (subnetted class C network)
    24 : '255.255.255.0',
    25 : '255.255.255.128',
    26 : '255.255.255.192',
    27 : '255.255.255.224',
    28 : '255.255.255.240',
    29 : '255.255.255.248',
    30 : '255.255.255.252',
    # 31-bit subnet masks are used for interfaces that act as endpoints in point-to-point links (see RFC 3021)
    31 : '255.255.255.254',
    # 32-bit subnet masks represent a network with a single address, such as a physical external interface
    32 : '255.255.255.255'
}

#|#########################################################| Global constants |########################################################|#

BAD_CIDR_ERROR = 'CIDR must be within the range [ 0, 32 ] - Given: {}'
BAD_SUBNET_MASK_ERROR = 'Octet list must consist of four integers ranging from [0, 255], sorted in descending order - Given: {}'
BAD_IPV4_ERROR = 'IPv4 address string must consist of four integers in range [0, 255] separated by \'.\' - Given: {}'

#|################################################| Argument type validator functions |################################################|#

str_valid  = arg_valid( str )
int_valid  = arg_valid( int )
list_valid = arg_valid( list )

#|#######################################################| Function definitions |######################################################|#

def get_subnet_info_given_mask( ipv4_str: str, subnet_mask_str: str ) -> dict:
    """Returns IPv4 subnet information given an IPv4 address and subnet mask

    Given an arbitrary valid IPv4 address and subnet mask, calculates and returns
    the network ID, wildcard mask, CIDR value, subnet class, host address range,
    broadcast address, number of host addresses, and the number of possible
    equivalent subnets that the given network class could be segmented into.

    Args:
        ipv4_str:
            A string representation of a valid IPv4 address.
        subnet_mask_str:
            A string representation of a valid IPv4 subnet mask.

    Returns:
        A dict mapping label keys to corresponding subnet information.
        example:
        { 
            'network_id' : '192.168.10.0', 
            'subnet_mask' : '255.255.255.0',
            'wildcard_mask' : '0.0.0.255', 
            'cidr_int' : 24,
            'cidr_str' : '/24',
            'subnet_class' : 'C', 
            'first_host' : '192.168.10.1', 
            'last_host' : '192.168.10.254', 
            'broadcast' : '192.168.10.255',
            'num_hosts' : 254, 
            'num_subnets' : 1
        }

    Raises:
        TypeError: Non-string input provided for ipv4_str or subnet_mask_str.
        ValueError: Invalid format for ipv4_str or subnet_mask_str.
    """
    # Input type validation
    str_valid( ipv4_str )
    str_valid( subnet_mask_str )

    # Get the IPv4 octet values as an array -> parse and tokenize the input string (assumes that the address has been validated by _ipv4_validator)
    ipv4 = parse_addr_str( ipv4_str )
    # Get the subnet mask octet values as an array (assumes that the address has been validated by _ipv4_validator)
    subnet_mask = parse_addr_str( subnet_mask_str )
    # Get the wildcard mask -> invert the subnet mask
    wildcard_mask = bitwise_not( subnet_mask )
    # Get the network ID -> bitwise AND the IPv4 address and subnet mask
    network_id = bitwise_and( ipv4, subnet_mask )
    # Get the broadcast address -> bitwise OR the network ID and wildcard mask
    broadcast = bitwise_or( network_id, wildcard_mask )
    # Get the first host address -> increment network ID by 1
    first_host = get_first_host( network_id )
    # Get the last host address -> decrement broadcast addr by 1
    last_host = get_last_host( broadcast )
    # Get the subnet class -> examine the subnet mask
    subnet_class = get_subnet_class( subnet_mask )
    # Get the number of usable host addresses -> multiply wildcard mask octets (+1 to each), subtract 2 from total
    num_hosts = get_num_hosts( wildcard_mask )
    # Get the number of subnets per network of the given class -> 2^(subnet_bits)
    num_subnets = get_num_subnets( subnet_mask )
    # Get the CIDR integer value from the subnet mask
    cidr_int = netmask_to_cidr( subnet_mask_str )
    # Get the CIDR string representation
    cidr_str = cidr_to_str( cidr_int )

    return { 
        'network_id' : network_id, 
        'subnet_mask' : subnet_mask,
        'wildcard_mask' : wildcard_mask, 
        'cidr_int' : cidr_int,
        'cidr_str' : cidr_str,
        'subnet_class' : subnet_class, 
        'first_host' : first_host, 
        'last_host' : last_host, 
        'broadcast' : broadcast, 
        'num_hosts' : num_hosts, 
        'num_subnets' : num_subnets 
    }

def get_subnet_info_given_cidr( ipv4_str: str, cidr: int ) -> dict:
    """Returns IPv4 subnet information given an IPv4 address and a CIDR value

    Given an arbitrary valid IPv4 address and CIDR, calculates and returns
    the network ID, subnet mask, wildcard mask, subnet class, host address range,
    broadcast address, number of host addresses, and the number of possible
    equivalent subnets that the given network class could be segmented into.

    Args:
        ipv4_str:
            A string representation of a valid IPv4 address.
        cidr:
            An integer value in the range [0,32] corresponding to a CIDR prefix length .

    Returns:
        A dict mapping label keys to corresponding subnet information.
        example:
        { 
            'network_id' : '192.168.10.0', 
            'subnet_mask' : '255.255.255.0',
            'wildcard_mask' : '0.0.0.255', 
            'cidr_int' : 24,
            'cidr_str' : '/24',
            'subnet_class' : 'C', 
            'first_host' : '192.168.10.1', 
            'last_host' : '192.168.10.254', 
            'broadcast' : '192.168.10.255',
            'num_hosts' : 254, 
            'num_subnets' : 1
        }

    Raises:
        TypeError: Non-string input provided for ipv4_str, non-integer input provided for cidr.
        ValueError: Invalid format for ipv4_str, invalid integer value for cidr.
    """
     # Input type validation
    str_valid( ipv4_str )
    int_valid( cidr )
    return get_subnet_info_given_mask( ipv4_str, cidr_to_netmask( cidr ) )

def cidr_to_netmask( cidr: int ) -> str:
    """Given a valid CIDR value, returns the corresponding subnet mask as a string

    Args:
        cidr:
            An integer value in the range [0,32] corresponding to a CIDR prefix length.
    
    Returns:
        A string representation of the subnet mask corresponding to the given CIDR.

    Raises:
        TypeError: Non-integer input is provided for cidr.
        ValueError: Invalid integer value is provided for cidr.
    """
    # Input type validation
    int_valid( cidr )
    try:
        return CIDR_DICT[ cidr ]
    except KeyError:
        raise ValueError( BAD_CIDR_ERROR.format(cidr) )

def netmask_to_cidr( subnet_mask_str: str ) -> int:
    """Given a valid subnet mask string, returns the corresponding CIDR value as an integer

    Args:
        subnet_mask_str:
            A string representation of a valid subnet mask.

    Returns:
        The CIDR value corresponding to the given subnet mask as an integer.

    Raises:
        TypeError: Non-string input provided for subnet_mask_str.
        ValueError: subnet_mask_str is not a valid subet mask.
    """
    # Input type validation
    str_valid( subnet_mask_str )
    # List comprehension that generates an array of integers [0, 32]
    cidr_vals = [ c for c in range (33) ]
    # Filter out CIDR values where cidr_dict[value] == subnet_mask
    key_iterator = filter( lambda k: CIDR_DICT[ k ] == subnet_mask_str, cidr_vals )
    try:
        # Only one CIDR should match subnet_mask, get it and return                                                                    
        cidr = next( key_iterator )
        return cidr
    except StopIteration:
        # If bad input was provided, need to catch error for empty iterator
        raise ValueError( BAD_SUBNET_MASK_ERROR.format(subnet_mask_str) )                                                                  

def parse_addr_str( addr_str: str ) -> list:
    """Parses an IPv4 address/netmask for octet values, returns a list containing the integer values

    Args:
        addr_str:
            A valid IPv4 address as a string.

    Returns:
        The integer octet values as a list.
        example:
        [192, 168, 10, 1]

    Raises:
        TypeError: If non-string input is provided for addr_str
        ValueError: If addr_str is not a valid IPv4 address
    """
    # Input type validation
    str_valid( addr_str )
    # Split the input string into four separate strings
    oct_list_str = split( '[.]', addr_str )
    try:
        # Convert the string tokens to integers
        oct_list_int = [ int(oct) for oct in oct_list_str ]
        # Return the list if it has exactly 4 elements that are all [0, 255]
        if len( oct_list_int ) == 4 and all( 0 <= oct <= 255 for oct in oct_list_int ):
            return oct_list_int
        # Else, throw an error                                                         
        else:
            raise ValueError( BAD_IPV4_ERROR.format(addr_str) )
    # If any cast to int fails, catch and throw a ValueError                                                                  
    except ValueError:
        raise ValueError( BAD_IPV4_ERROR.format(addr_str) )                                                                   

def get_first_host( net_id: list ) -> list:
    """Finds the first host address for a subnet given a valid network ID

    Args:
        net_id:
            The network ID for the subnet as a list of four integers corresponding to the four 8-bit octet values.

    Returns:
        The first host address for the subnet as a list of four integers corresponding to the four 8-bit octet values.

    Raises:
        TypeError: Non-list input is provided for net_id, non-integer elements in net_id
    """
    # Input type validation
    list_valid( net_id )
    # Ensure all list elements are integers
    all( int_valid(oct) for oct in net_id )
    # Get the first host addr by incrementing the net ID by 1
    return [ sum(x) for x in zip(net_id, [0, 0, 0, 1]) ]

def get_last_host( broadcast: list ) -> list:
    """Finds the last host address given the broadcast address

    Args:
        broadcast:
            The broadcast address for the given subnet as a list of four integers corresponding to the four 8-bit octet values.
    
    Returns:
        The last host address for the subnet as a list of four integers corresponding to the four 8-bit octet values.

    Raises:
        TypeError: Non-list input is provided for broadcast, non-integer elements in broadcast.
    """
    # Input type validation
    list_valid( broadcast )
    # Ensure all list elements are integers
    all( int_valid(oct) for oct in broadcast )
    # Get the last host addr by decrementing the broadcast addr by 1
    return [ sum(x) for x in zip(broadcast, [0, 0, 0, -1]) ]

def get_subnet_class( subnet_mask: list ) -> str:
    """Given a valid subnet mask, returns the classful network type that the subnet would segment

    Args:
        subnet_mask:
            A list representing a subnet mask containing four integers representing the four 8-bit integer octets.

    Returns:
        The classful network type that the subnet would segment.
        example:
        get_subnet_class( [255,255,255,128] ) -> 'C'

    Raises:
        TypeError: Non-list input provided for subnet_mask, non-integer elements in subnet_mask.
        ValueError: subnet_mask does not represent a valid subnet mask
    """ 
    if not validate_subnet_mask_octet_list( subnet_mask ):
        raise ValueError( BAD_SUBNET_MASK_ERROR.format(repr(subnet_mask)) )
    if subnet_mask[0] != 255:
        return 'none'
    elif subnet_mask[1] != 255:
        return 'A'
    elif subnet_mask[2] != 255:
        return 'B'
    else:
        return 'C'

def get_num_hosts( subnet_mask: list ) -> int:
    """Given a valid subnet mask, returns the number of valid host addresses for the subnet

    Args:
        subnet_mask:
            A list representing a subnet mask containing four integers representing the four 8-bit integer octets.
    
    Returns:
        The number of host addresses for the subnet (i.e. the total number of addresses minus two for the network ID and broadcast address)

    Throws:
        TypeError: Non-list input provided for subnet_mask, non-integer elements in subnet_mask.
        ValueError: subnet_mask does not represent a valid subnet mask
    """
    if not validate_subnet_mask_octet_list( subnet_mask ):
        raise ValueError( BAD_SUBNET_MASK_ERROR.format(repr(subnet_mask)) )
    # Invert to get wildcard mask
    wildcard_mask = bitwise_not( subnet_mask)
    # Get each element from the wildcard_mask array and add one
    wild_plus_1 = [ w + 1 for w in wildcard_mask ]
    # Multiply the values together to get the total number of addresses
    addr_total = prod( wild_plus_1 )
    # Subtract 2 for the network ID and broadcast address to get the final number of valid hosts
    return addr_total - 2

def get_num_subnets( subnet_mask: list ) -> int:
    """Gets the number of possible subnets for the given mask that could segment that class of network

    Args:
        subnet_mask:
            A list representing a subnet mask containing four integers representing the four 8-bit integer octets.

    Returns:
        The number of possible subnets for the given mask that could segment that class of network.

    Throws:
        TypeError: Non-list input provided for subnet_mask, non-integer elements in subnet_mask.
        ValueError: subnet_mask does not represent a valid subnet mask
    """
    if not validate_subnet_mask_octet_list( subnet_mask ):
        raise ValueError( BAD_SUBNET_MASK_ERROR.format(repr(subnet_mask)) )
    for oct in subnet_mask:
        # Find the "interesting octet", i.e. the first non-255 octet
        if oct != 255:
            # Convert the interesting octet to binary representation
            bit_string = binary_repr( oct )
            # Count the number of 1-bits
            subnet_bits = 0
            for b in bit_string:
                if b == '1': subnet_bits += 1
            # Return the number of subnets based on the number of subnet bits
            return 2 ^ subnet_bits
    # Should only reach this point if 255.255.255.255 is passed -> network with only 1 host, 256 1-host subnets
    return 256

def cidr_to_str( cidr: int ) -> str:
    """Given a valid CIDR value, returns the string representation

    Args:
        cidr:
            An integer value in the range [0,32] corresponding to a CIDR prefix length.

    Returns:
        A concatenated string containing the given CIDR
        example:
        '/24'

    Raises:
        TypeError: Non-integer input provided for cidr
        ValueError: Invalid integer input provided for cidr
    """
    # Input type validation
    int_valid( cidr )
    # Check for valid integer input
    if cidr >= 0 and cidr <= 32:
        sb = []
        sb.append( '/' )
        sb.append( str(cidr) )
        return ''.join( sb )
    else:
        raise ValueError( BAD_CIDR_ERROR.format(cidr) )

def validate_subnet_mask_octet_list( subnet_mask: list ) -> bool:
    """Helper function for validating a list of integers as a subnet mask

    Validation of subnet mask strings is handled by _ipv4_validator.py, this is mostly for sanity checking.

    Args:
        subnet_mask:
            A list representing a subnet mask containing four integers representing the four 8-bit integer octets

    Returns:
        True if subnet_mask represents a valid subnet mask, False if subnet_mask does not represent a valid subnet mask

    Raises:
        TypeError: Non-list input provided for subnet_mask, non-integer elements in subnet_mask.
    """
    # Ensure input is a list
    list_valid( subnet_mask )
    # Ensure all list elements are integers
    all( int_valid(oct) for oct in subnet_mask )
    # Convert all elements back to strings
    m = [ str(oct) for oct in subnet_mask ]
    # Insert '.' between the list elements, convert to a single string
    m_str = ''.join( _delimit_list( m, '.', 1 ) )
    # Call netmask_to_cidr, check for error
    try:
        netmask_to_cidr( m_str )
    except ValueError:
        return False
    
    # Return True if no exception is caught
    return True

def _delimit_list( _list: list, _delim: str, _freq: int ) -> list:
    """Helper function for inserting a delimiter character every f elements (specified by _freq) into an existing list

    Source: https://www.geeksforgeeks.org/python-insert-after-every-nth-element-in-a-list/

    Args:
        _list:
            A list of string tokens to manipulate.
        _delim:
            The character to insert.
        _freq:
            How many tokens to skip over before inserting delimiter (minimum 1)

    Returns:
        example:
        _delimit_list( [ 'a', 'b', 'c', 'd' ], '.', 1 ) -> [ 'a', '.', 'b', '.', 'c', '.', 'd' ]
    """

    '''
    Implementation notes:

    itertools.chain takes a single or multiple iterables and combines them into a single iterable (e.g. *[ x, y, z ] turns this list into an iterable)
    This function loops over the range 0 to len(_list) - 1 in steps of _freq and attempts to construct the substring _list[i : i+_freq] 
    It then checks the substr's length -> 
        if substr.len == _freq (i.e. haven't reached the end of _list), append _delim
        else don't append _delim
    In the cases where _freq = 1, _delim will be appended to the end of the list regardless, so an additional check is performed to remove this
    The result is then returned
    '''

    list_valid( _list )
    str_valid( _delim )
    int_valid( _freq )
    delimited = list(
                    chain (
                        *[ _list[i : i+_freq] + [_delim]
                        if len(_list[i : i+_freq] ) == _freq
                        else _list[i : i+_freq]
                        for i in range( 0, len(_list), _freq ) ]
                    ) 
                )
    if delimited[ len(delimited) - 1 ] == _delim: delimited.pop()
    return delimited