"""
Calculates detailed IPv4 subnet information given an arbitrary IPv4 address and subnet mask/CIDR value.

Author: Noah Benveniste
https://github.com/noahbenveniste/subnet-calculator
"""
# TODO: 
# - Finish implementing addr_to_str
# - Handle edge cases for /0, /31, /32
# - Finish implementing tests for ipv4 calculator and validator
# - Look up how to generate documentation
# - Set up a Jenkins server to automate unit testing
# - Create a dev branch once all IPv4 functionality is tested and implemented, only merge to main when all tests pass

# - get_subnet_info_given_mask  TODO: test
# - get_subnet_info_given_cidr  TODO: test
# - get_first_host              TODO: test, handle edge case for /0, /31 and /32 subnets
# - get_last_host               TODO: test, handle edge case for /0, /31 and /32 subnets
# - get_num_hosts               TODO: test, handle edge case for /0, /31 and /32 subnets
# - get_num_subnets             TODO: test, handle edge case for /0, /31 and /32 subnets

from v4.ipv4_validator import argument_type_validator
from v4.ipv4_validator import BAD_SUBNET_MASK_ERROR
from v4.ipv4_validator import BAD_CIDR_ERROR
from v4.ipv4_validator import CIDR_DICT
from numpy              import bitwise_and
from numpy              import bitwise_or
from numpy              import bitwise_not
from numpy              import binary_repr
from numpy              import prod
from numpy              import array
from numpy              import uint8
from itertools          import chain
from re                 import split

#|##########################################################| Argument type validator functions |###########################################################|#

# Each of these calls returns a lambda expression that will check if an input argument matches the specified data type
ensure_dtype_str = argument_type_validator( str )
ensure_dtype_int = argument_type_validator( int )
ensure_dtype_list = argument_type_validator( list )

#|#################################################################| Function definitions |#################################################################|#

def get_ipv4_subnet_info_given_mask( ipv4_str: str, subnet_mask_str: str ) -> dict:
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
            'ipv4' : '192.168.10.2',
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
    """
    # Ensure IPv4 input is a string, throw a TypeError if it is not
    ensure_dtype_str( ipv4_str )
    # Ensure subnet mask input is a string, throw a TypeError if it is not
    ensure_dtype_str( subnet_mask_str )
    # Get the IPv4 octet values as an array -> parse and tokenize the input string
    ipv4 = parse_addr_str( ipv4_str )
    # Get the subnet mask octet values as an array
    subnet_mask = parse_addr_str( subnet_mask_str )
    # Get the wildcard mask -> invert the subnet mask
    wildcard_mask = get_wildcard_mask( subnet_mask )
    # Get the network ID -> bitwise AND the IPv4 address and subnet mask
    network_id = get_network_id( ipv4, subnet_mask )
    # Get the broadcast address -> bitwise OR the network ID and wildcard mask
    broadcast = get_broadcast_addr( network_id, wildcard_mask )
    # Get the first host address -> increment network ID by 1
    first_host = get_first_host( network_id )
    # Get the last host address -> decrement broadcast addr by 1
    last_host = get_last_host( broadcast )
    # Get the subnet class -> examine the subnet mask
    subnet_class = get_subnet_class( subnet_mask )
    # Get the number of usable host addresses -> multiply wildcard mask octets (+1 to each), subtract 2 from total
    num_hosts = get_num_hosts( subnet_mask )
    # Get the number of subnets per network of the given class -> 2^(subnet_bits)
    num_subnets = get_num_subnets( subnet_mask )
    # Get the CIDR integer value from the subnet mask
    cidr_int = netmask_to_cidr( subnet_mask_str )
    # Get the CIDR string representation
    cidr_str = cidr_to_str( cidr_int )

    return {
        'ipv4' : ipv4_str,
        'network_id' : addr_to_str( network_id ), 
        'subnet_mask' : subnet_mask_str,
        'wildcard_mask' : addr_to_str( wildcard_mask ), 
        'cidr_int' : cidr_int,
        'cidr_str' : cidr_str,
        'subnet_class' : subnet_class, 
        'first_host' : addr_to_str( first_host ), 
        'last_host' : addr_to_str( last_host ), 
        'broadcast' : addr_to_str( broadcast ), 
        'num_hosts' : num_hosts, 
        'num_subnets' : num_subnets 
    }

def get_ipv4_subnet_info_given_cidr( ipv4_str: str, cidr: int ) -> dict:
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

    Raises:
        TypeError: Non-string input provided for ipv4_str, non-integer input provided for cidr.
    """
    # Ensure cidr is an integer, throw TypeError if it is not
    ensure_dtype_int( cidr )
    # Ensure IPv4 is a string, throw TypeError if it is not
    ensure_dtype_str( ipv4_str )    
    # Convert the CIDR value to a subnet mask and call get_subnet_info_given_mask
    return get_ipv4_subnet_info_given_mask( ipv4_str, cidr_to_netmask( cidr ) )

def get_wildcard_mask( subnet_mask: list ) -> list:
    """Calculates the wildcard mask for a subnet given the subnet mask

    Args:
        subnet_mask:
            The subnet mask for the subnet as a list of integers corresponding to the four 8-bit integer octets

    Returns:
        The wildcard mask as a list of integer octets

    Raises:
        TypeError: Non-list input provided for subnet_mask, subnet_mask contains non-integer elements
    """
    # Ensure input is a list
    ensure_dtype_list( subnet_mask )
    '''
    Ensure all list elements are integers. The bool return from
    all() is irrelevant, only using it b/c it is an easy one-liner
    looping mechanism that allows us to call the int validator
    function which will throw an error for any non-int elements.
    '''
    all( ensure_dtype_int(oct) for oct in subnet_mask )
    # Cast to a numpy.array with datatype uint8 to prevent negative integer values being calculated
    np_subnet_mask = array( subnet_mask, dtype=uint8 )
    # Get the wildcard mask by inverting the subnet mask, cast back to integer list
    return [ int(oct) for oct in list( bitwise_not( np_subnet_mask ) ) ] 

def get_network_id( ipv4: list, subnet_mask: list ) -> list:
    """Calculates the network ID for a subnet given an arbitrary address within the subnet's address space and the subnet mask

    Args:
        ipv4:
            An IPv4 address within the subnet's address space as a list of integer values corresponding to the four 8-bit integer octets
        subnet_mask:
            The subnet mask as a list of integer octet values

    Returns:
        The network ID for the subnet as a list of integer octet values

    Raises:
        TypeError: Non-list input provided for ipv4 or subnet_mask, ipv4 or subnet_mask contain non-integer elements
    """
     # Ensure that both inputs are lists, and that both lists only contain integers
    ensure_dtype_list( ipv4 )
    all( ensure_dtype_int(oct) for oct in ipv4 )
    ensure_dtype_list( subnet_mask )
    all( ensure_dtype_int(oct) for oct in subnet_mask )
    # Cast ipv4 and subnet_mask to numpy.array with data type uint8
    np_ipv4 = array( ipv4, dtype=uint8 )
    np_subnet_mask = array( subnet_mask, dtype=uint8 )
    # Get the network ID by AND-ing the IPv4 address and subnet mask, cast back to integer list
    return [ int(oct) for oct  in list ( bitwise_and( np_ipv4, np_subnet_mask ) ) ]

def get_broadcast_addr( network_id: list, wildcard_mask: list ) -> list:
    """Calculates the broadcast address for a subnet given its network ID and wildcard mask

    Args:
        network_id:
            The network ID of the subnet as a list of integers corresponding to the four 8-bit integer octets
        wildcard_mask:
            The wildcard mask (i.e. the inverted subnet mask) for the subnet as a list of integer octet values

    Returns:
        The broadcast address for the subnet i.e. the last address in the address space

    Raises:
        TypeError: Non-list input provided for network_id or wildcard_mask, network_id or wildcard_mask contain non-integer elements
    """
    # Ensure that both inputs are lists, and that both lists only contain integers
    ensure_dtype_list( network_id )
    all( ensure_dtype_int(oct) for oct in network_id )
    ensure_dtype_list( wildcard_mask )
    all( ensure_dtype_int(oct) for oct in wildcard_mask )
    # Cast network_id and wildcard_mask to numpy.array with data type uint8
    np_network_id = array( network_id, dtype=uint8 )
    np_wildcard_mask = array( wildcard_mask, dtype=uint8 )
    # Get the broadcast address by OR-ing the network ID and wildcard mask, cast back to integer list
    return [ int(oct) for oct in list( bitwise_or( np_network_id, np_wildcard_mask ) ) ]

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
    # Ensure input is an integer
    ensure_dtype_int( cidr )
    # Return the value corresponding to the key cidr
    try:
        return CIDR_DICT[ cidr ]
    except KeyError:
        raise ValueError( BAD_CIDR_ERROR.format(cidr) )

def netmask_to_cidr( subnet_mask_str: str ) -> int:
    """Given a valid subnet mask, returns the corresponding CIDR value as an integer

    Args:
        subnet_mask:
            A valid string representation of an IPv4 subnet mask

    Returns:
        The CIDR value corresponding to the given subnet mask as an integer.

    Raises:
        TypeError: Non-string input provided for subnet_mask_str.
        ValueError: subnet_mask_str is not a valid subnet mask.
    """
    # Ensure input is a string
    ensure_dtype_str( subnet_mask_str )
    # List comprehension that generates an array of integers [0, 32]
    cidr_vals = [ c for c in range (33) ]
    # Loop over range [0,32], filter out CIDR values where cidr_dict[value] == subnet_mask
    cidr_iterator = filter( lambda cidr: CIDR_DICT[ cidr ] == subnet_mask_str, cidr_vals )
    try:
        # Only one CIDR should match subnet_mask, get it and return                                                                    
        return next( cidr_iterator )
    except StopIteration:
        # If bad input was provided, need to catch error for empty iterator
        raise ValueError( BAD_SUBNET_MASK_ERROR.format(subnet_mask_str) )

def parse_addr_str( addr_str: str ) -> list:
    """Parses an IPv4 address/netmask for octet values, returns a list containing the integer values

    Args:
        addr_str:
            A string of the format x.x.x.x, where x is any integer in the range [0,255]

    Returns:
        The integer octet values as a list.
        example:
        [192, 168, 10, 1]

    Raises:
        TypeError: Non-string input is provided for addr_str
    """
    # Ensure input is a string
    ensure_dtype_str( addr_str )
    # Split the input string into four separate strings
    oct_str_list = split( '[.]', addr_str )
    # Convert the string tokens to integers - don't need try/except b/c the string is already validated
    return [ int(oct) for oct in oct_str_list ]                                                               

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
    # Ensure input is a list
    ensure_dtype_list( net_id )
    # Ensure all list elements are integers
    all( ensure_dtype_int(oct) for oct in net_id )
    # Get the first host addr by incrementing the net ID by 1
    return [ sum(x) for x in zip( net_id, [0, 0, 0, 1] ) ]

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
    # Ensure input is a list
    ensure_dtype_list( broadcast )
    # Ensure all list elements are integers
    all( ensure_dtype_int(oct) for oct in broadcast )
    # Get the last host addr by decrementing the broadcast addr by 1
    return [ sum(x) for x in zip( broadcast, [0, 0, 0, -1] ) ]

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
    """ 
    # Ensure input is a list
    ensure_dtype_list( subnet_mask )
    # Ensure all list elements are integers
    all( ensure_dtype_int(oct) for oct in subnet_mask )
    # Determine the subnet class based on the interesting octet, i.e. the right-most non-255 octet
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
        The number of host addresses for the subnet (i.e. the total number of addresses, minus two for the network ID and broadcast address).

    Throws:
        TypeError: Non-list input provided for subnet_mask, non-integer elements in subnet_mask.
    """
    # Call get_wildcard_mask to convert the subnet mask to a wildcard
    wildcard_mask = get_wildcard_mask( subnet_mask )
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
    """
    # Ensure input is a list
    ensure_dtype_list( subnet_mask )
    # Ensure all list elements are integers
    all( ensure_dtype_int(oct) for oct in subnet_mask )
    # Loop over the octets in the subnet mask
    for oct in subnet_mask:
        # Find the "interesting octet", i.e. the first non-255 octet
        if oct != 255:
            # Convert the interesting octet to binary representation
            bit_str = binary_repr( oct )
            # Count the number of 1-bits
            subnet_bits = 0
            for b in bit_str:
                if b == '1': subnet_bits += 1
            # Return the number of subnets based on the number of subnet bits
            return 2**subnet_bits
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
    """
    # Ensure input is an integer
    ensure_dtype_int( cidr )
    # Build the output string
    return ''.join( ['/', str(cidr) ] )

def addr_to_str( addr: list ) -> str:
    """Given a valid IPv4 address or subnet mask as a list of integer octets, returns a string representation

    Args:
        addr:
            A list representing an IPv4 address or subnet mask containing four integers representing the four 8-bit integer octets.

    Returns:
        The IPv4 address or subnet mask as a string

    Raises:
        TypeError: Non-list input is provided for addr, addr contains non-integer elements
    """
    # Ensure input is a list
    ensure_dtype_list( addr )
    # Ensure all list elements are integers
    all( ensure_dtype_int(oct) for oct in addr )
    # Convert the elements in addr to strings
    oct_str_list = [ str(oct) for oct in addr ]
    return ''.join(_delimit_list( oct_str_list, '.', 1 ))

def _delimit_list( _list: list, _delim: str, _freq: int ) -> list:
    """Helper function for inserting a delimiter character every f elements (specified by _freq) into an existing list
    
    Source: https://www.geeksforgeeks.org/python-insert-after-every-nth-element-in-a-list/

    Args:
        _list:
            The list to insert a delimiter into
        _delim:
            The delimter character/string
        _freq:
            How often to insert the delimiter, indicated by the length of a substring within _list
    
    Returns:
        A delimited list
        example: 
        _delimit_list( [ 'a', 'b', 'c', 'd' ], '.', 1 ) -> [ 'a', '.', 'b', '.', 'c', '.', 'd' ]
    """
    delimited = list( chain( *[ _list[i : i+_freq] + [_delim] 
                               if len(_list[i : i+_freq]) == _freq
                               else _list[i : i+_freq]
                               for i in range(0, len(_list), _freq) ] ) )
    # Remove extra delimiter character from end of list (can happen when _freq == 1)
    if delimited[ len(delimited) - 1 ] == _delim: delimited.pop()
    return delimited