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
# - get_first_host              TODO: test, handle edge case for /0, /31 and /32 subnets [Validation should be good, no refactoring should be necessary]
# - get_last_host               TODO: test, handle edge case for /0, /31 and /32 subnets [Validation should be good, no refactoring should be necessary]
# - get_subnet_class            TODO: 
# - get_num_hosts               TODO: test, handle edge case for /0, /31 and /32 subnets
# - get_num_subnets             TODO: test, handle edge case for /0, /31 and /32 subnets
# - cidr_to_str                 TODO: 
# - validate_octet_list         TODO: Refactor this into _ipv4_validator and change into a simple lookup table/regex for address validation

#|#############################################################| Imports |##############################################################|#

from v4._ipv4_validator import CIDR_DICT
from v4._ipv4_validator import argument_type_validator
from v4._ipv4_validator import is_valid_cidr
from numpy              import bitwise_and
from numpy              import bitwise_or
from numpy              import bitwise_not
from numpy              import binary_repr
from numpy              import prod
from re                 import split

#|#########################################################| Global constants |#########################################################|#

BAD_CIDR_ERROR = 'CIDR must be within the range [ 0, 32 ] - Given: {}'
BAD_SUBNET_MASK_ERROR = 'Octet list must consist of four integers ranging from [0, 255], sorted in descending order - Given: {}'
BAD_IPV4_ERROR = 'IPv4 address string must consist of four integers in range [0, 255] separated by \'.\' - Given: {}'

#|################################################| Argument type validator functions |#################################################|#

ensure_type_str = argument_type_validator( str )
ensure_type_int = argument_type_validator( int )
ensure_type_list = argument_type_validator( list )

#|#######################################################| Function definitions |#######################################################|#

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
    # Ensure IPv4 input is a string, throw a TypeError if it is not
    ensure_type_str( ipv4_str )
    # Validate IPv4 address structure
    # TODO: Implement
    # Ensure subnet mask input is a string, throw a TypeError if it is not
    ensure_type_str( subnet_mask_str )
    # Validate subnet mask structure
    # TODO: Implement
    # Get the IPv4 octet values as an array -> parse and tokenize the input string (assumes that the address has been validated by _ipv4_validator)
    ipv4 = parse_addr_str( ipv4_str )
    # Get the subnet mask octet values as an array (assumes that the address has been validated by _ipv4_validator)
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

    Raises:
        TypeError: Non-string input provided for ipv4_str, non-integer input provided for cidr.
        ValueError: Invalid format for ipv4_str, invalid integer value for cidr.
    """
    # Ensure cidr is an integer, throw error if it is not
    ensure_type_int( cidr )
    # Validate that cidr value is within the correct range
    if not is_valid_cidr( cidr ): raise ValueError( BAD_CIDR_ERROR.format(cidr) )
    # Ensure IPv4 is a string, throw error if it is not
    ensure_type_str( ipv4_str )
    # Validate IPv4 address structure
    # TODO: Implement
    return get_subnet_info_given_mask( ipv4_str, cidr_to_netmask( cidr ) )

def get_wildcard_mask( subnet_mask: list ) -> list:
    """
    """
    # Ensure input is a list
    ensure_type_list( subnet_mask )
    '''
    Ensure all list elements are integers. The bool return from
    all() is irrelevant, only using it b/c it is an easy one-liner
    looping mechanism that allows us to call the int validator
    function which will throw an error for any non-int elements.
    '''
    all( ensure_type_int(oct) for oct in subnet_mask )
    # Get the wildcard mask by inverting the subnet mask
    return bitwise_not( subnet_mask )

def get_network_id( ipv4: list, subnet_mask: list ) -> list:
    """
    """
     # Ensure that both inputs are lists, and that both lists only contain integers
    ensure_type_list( ipv4 )
    all( ensure_type_int(oct) for oct in ipv4 )
    ensure_type_list( subnet_mask )
    all( ensure_type_list(oct) for oct in subnet_mask )
    # Get the network ID by AND-ing the IPv4 address and subnet mask
    return bitwise_and( ipv4, subnet_mask )

def get_broadcast_addr( network_id: list, wildcard_mask: list ) -> list:
    """
    """
    # Ensure that both inputs are lists, and that both lists only contain integers
    ensure_type_list( network_id )
    all( ensure_type_int(oct) for oct in network_id )
    ensure_type_list( wildcard_mask )
    all( ensure_type_int(oct) for oct in wildcard_mask )
    # Get the broadcast address by OR-ing the network ID and wildcard mask
    return bitwise_or( network_id, wildcard_mask )

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
    ensure_type_int( cidr )
    # Ensure cidr is within the correct range
    if not is_valid_cidr( cidr ): raise ValueError( BAD_CIDR_ERROR.format(cidr) )
    '''
    Try to retrieve the corresponding subnet mask value using cidr as a key.
    Because  we've already validated cidr, no errors should occur. The try/except
    is just a sanity check.
    '''
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
        ValueError: subnet_mask_str is not a valid subet mask.
    """
    # Ensure input is a string
    ensure_type_str( subnet_mask_str )
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
            A string of the format x.x.x.x, where x is any integer in the range [0,255]

    Returns:
        The integer octet values as a list.
        example:
        [192, 168, 10, 1]

    Raises:
        TypeError: If non-string input is provided for addr_str
        ValueError: If the string contains any invalid characters
    """
    # Ensure input is a string
    ensure_type_str( addr_str )
    # Validate IPv4 address structure (yes it's redundant, just a sanity check)
    # TODO: Implement
    # Split the input string into four separate strings
    oct_list_str = split( '[.]', addr_str )
    try:
    # Convert the string tokens to integers
       return [ int(oct) for oct in oct_list_str ]
    # If any cast to int fails, catch and throw a ValueError with a descriptive error message                                                                
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
    # Ensure input is a list
    ensure_type_list( net_id )
    # Ensure all list elements are integers
    all( ensure_type_int(oct) for oct in net_id )
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
    ensure_type_list( broadcast )
    # Ensure all list elements are integers
    all( ensure_type_int(oct) for oct in broadcast )
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
        ValueError: subnet_mask does not represent a valid subnet mask
    """ 
    # Ensure input is a list
    ensure_type_list( subnet_mask )
    # Ensure all list elements are integers
    all( ensure_type_int(oct) for oct in subnet_mask )
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
    # Ensure input is a list
    ensure_type_list( subnet_mask )
    # Ensure all list elements are integers
    all( ensure_type_int(oct) for oct in subnet_mask )
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
    # Ensure input is a list
    ensure_type_list( subnet_mask )
    # Ensure all list elements are integers
    all( ensure_type_int(oct) for oct in subnet_mask )
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
    # Ensure input is an integer
    ensure_type_int( cidr )
    # Ensure input is in the valid range
    if not is_valid_cidr( cidr ): raise ValueError( BAD_CIDR_ERROR.format(cidr) )
    # Build the output string
    return ''.join( ['/', str(cidr) ] )

'''
# TODO: Deprecate
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
'''
'''
def _delimit_list( _list: list, _delim: str, _freq: int ) -> list:
    """Helper function for inserting a delimiter character every f elements (specified by _freq) into an existing list

    Source: https://www.geeksforgeeks.org/python-insert-after-every-nth-element-in-a-list/

    Args:
        _list:
            A list of string tokens to manipulate.
        _delim:
            The character to insert.
        _freq:
            How many tokens to skip over before inserting delimiter (minimum 1).

    Returns:
        A copy of _list updated with _delim inserted after the number of elements specified by _freq,
        repeated until the end of the list. _delim will not be inserted as the last element of the list.
        example:
        _delimit_list( [ 'a', 'b', 'c', 'd' ], '.', 1 ) -> [ 'a', '.', 'b', '.', 'c', '.', 'd' ]
    """
    """
    Implementation notes:

    itertools.chain takes a single or multiple iterables and combines them into a single iterable (e.g. *[ x, y, z ] turns this list into an iterable)
    This function loops over the range 0 to len(_list) - 1 in steps of _freq and attempts to construct the substring _list[i : i+_freq] 
    It then checks the substr's length -> 
        if substr.len == _freq (i.e. haven't reached the end of _list), append _delim
        else don't append _delim
    In the cases where _freq = 1, _delim will be appended to the end of the list regardless, so an additional check is performed to remove this
    The result is then returned
    """

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
'''