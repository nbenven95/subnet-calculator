'''
Calculates detailed IPv4 subnet information given an arbitrary IPv4 address and subnet mask/CIDR value.

Author: Noah Benveniste
https://github.com/noahbenveniste/subnet-calculator
'''

# - get_subnet_info_given_mask  TODO: test
# - get_subnet_info_given_cidr  TODO: test
# - cidr_to_netmask             TODO:
# - netmask_to_cidr             TODO:
# - parse_addr_str              TODO: test
# - get_first_host              TODO: test, handle edge case for /0, /31 and /32 subnets
# - get_last_host               TODO: test, handle edge case for /0, /31 and /32 subnets
# - get_subnet_class            TODO: handle edge case for /0, /31 and /32 subnets
# - get_num_hosts               TODO: test, handle edge case for /0, /31 and /32 subnets
# - get_num_subnets             TODO: test, handle edge case for /0, /31 and /32 subnets
# - cidr_to_str                 TODO: 

#|#############################################################| Imports |##############################################################|#

from numpy import bitwise_and
from numpy import bitwise_or
from numpy import bitwise_not
from numpy import binary_repr
from numpy import prod
from re    import split

from v4._ipv4_validator import argument_type_validator as arg_valid

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
    31 : '255.255.255.254', # 31-bit subnet masks are used for interfaces that act as endpoints in point-to-point links (see RFC 3021)
    32 : '255.255.255.255'  # 32-bit subnet masks represent a network with a single address, such as a physical external interface
}

#|#########################################################| Global constants |########################################################|#

BAD_CIDR_ERROR = 'CIDR must be within the range [ 0, 32 ] (Given: {})'

#|################################################| Argument type validator functions |################################################|#

str_valid  = arg_valid( str )
int_valid  = arg_valid( int )
list_valid = arg_valid( list )

#|#######################################################| Function definitions |######################################################|#

'''
Returns IPv4 subnet information given an IPv4 address and a subnet mask
e.g.
get_subnet_info_given_mask( '192.168.10.1', '255.255.255.0' ) ->
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
'''
def get_subnet_info_given_mask( ipv4_str: str, subnet_mask_str: str ) -> dict:

    str_valid( ipv4_str )                                     # Input type validation
    str_valid( subnet_mask_str )

    ipv4            = parse_addr_str( ipv4_str )              # Get the IPv4 octet values as an array -> parse and tokenize the input string
    subnet_mask     = parse_addr_str( subnet_mask_str )       # Get the subnet mask octet values as an array
    wildcard_mask   = bitwise_not( subnet_mask )              # Get the wildcard mask -> invert the subnet mask
    network_id      = bitwise_and( ipv4, subnet_mask )        # Get the network ID -> bitwise AND the IPv4 address and subnet mask
    broadcast       = bitwise_or( network_id, wildcard_mask ) # Get the broadcast address -> bitwise OR the network ID and wildcard mask
    first_host      = get_first_host( network_id )            # Get the first host address -> increment network ID by 1
    last_host       = get_last_host( broadcast )              # Get the last host address -> decrement broadcast addr by 1
    subnet_class    = get_subnet_class( subnet_mask )         # Get the subnet class -> examine the subnet mask
    num_hosts       = get_num_hosts( wildcard_mask )          # Get the number of usable host addresses -> multiply wildcard mask octets (+1 to each), subtract 2 from total
    num_subnets     = get_num_subnets( subnet_mask )          # Get the number of subnets per network of the given class -> 2^(subnet_bits)
    cidr_int        = netmask_to_cidr( subnet_mask_str )      # Get the CIDR integer value from the subnet mask
    cidr_str        = cidr_to_str( cidr_int )                 # Get the CIDR string representation
    
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

'''
Returns IPv4 subnet information given an IPv4 address and a CIDR value
e.g.
See usage for get_subnet_info_given_mask
'''
def get_subnet_info_given_cidr( ipv4_str: str, cidr: int ) -> dict:
    str_valid( ipv4_str ) # Input type validation
    int_valid( cidr )
    return get_subnet_info_given_mask( ipv4_str, cidr_to_netmask( cidr ) )

'''
Given a valid CIDR value, returns the corresponding subnet mask as a string
e.g.
cidr_to_netmask( 24 ) -> '255.255.255.0'
'''
def cidr_to_netmask( cidr: int ) -> str:
    int_valid( cidr ) # Input type validation
    try:
        return CIDR_DICT[ cidr ]
    except KeyError as e:
        raise ValueError( BAD_CIDR_ERROR.format(cidr) )

'''
Given a valid subnet mask string, returns the corresponding CIDR value as an integer
e.g.
netmask_to_cidr( '255.255.255.0' ) -> 24
'''
def netmask_to_cidr( subnet_mask: str ) -> int:
    str_valid( subnet_mask )                                                    # Input type validation
    cidr_vals = [ c for c in range (33) ]                                       # List comprehension that generates an array of integers [0, 32]
    key_iterator = filter( lambda k: CIDR_DICT[ k ] == subnet_mask, cidr_vals ) # Filter out CIDR values where cidr_dict[value] == subnet_mask
    try:                                                                        
        cidr = next( key_iterator )                                             # Only one CIDR should match subnet_mask, get it and return
        return cidr
    except StopIteration:                                                       # If bad input was provided, need to catch error for empty iterator
        return -1                                                               # If no matching CIDR was found, return -1

'''
Parses an IPv4 address/netmask for octet values and returns an array containing the integer values
e.g.
parse_addr_str( '192.168.10.1' ) -> [192, 168, 10, 1]
'''
def parse_addr_str( addr_str: str ) -> list:
    str_valid( addr_str )                               # Input type validation
    oct_list_str = split( '[.]', addr_str )             # Split the input string into four separate strings
    oct_list_int = [ int(oct) for oct in oct_list_str ] # Convert the string tokens to integers
    return oct_list_int

'''
Finds the first host address given the network ID
e.g.
get_first_host( [192, 168, 10, 0] ) -> [192, 168, 10, 1]
'''
def get_first_host( net_id: list ) -> list:
    list_valid( net_id )                                 # Input type validation
    return [ sum(x) for x in zip(net_id, [0, 0, 0, 1]) ] # Get the first host addr by incrementing the net ID by 1

'''
Finds the last host address given the broadcast address
e.g.
get_last_host( [192, 168, 10, 255] ) -> [192, 168, 10, 254]
'''
def get_last_host( broadcast: list ) -> list:
    list_valid( broadcast )                                  # Input type validation
    return [ sum(x) for x in zip(broadcast, [0, 0, 0, -1]) ] # Get the last host addr by decrementing the broadcast addr by 1

'''
Given a subnet mask in the form of an array of octets, returns the subnet class
e.g.
get_subnet_class( [255, 255, 128, 0] ) -> 'B'
'''
def get_subnet_class( subnet_mask: list ) -> str:
    list_valid( subnet_mask ) # Input type validation
    if subnet_mask[0] != 255:
        return 'none'
    elif subnet_mask[1] != 255:
        return 'A'
    elif subnet_mask[2] != 255:
        return 'B'
    else:
        return 'C'

'''
Given a valid wildcard mask, returns the number of valid host addresses, minus the network ID and broadcast address
e.g.
get_num_hosts( [0, 0, 0, 127] ) -> 126
'''
def get_num_hosts( wildcard_mask: list ) -> int:
    list_valid( wildcard_mask )                     # Input type validation
    wild_plus_1 = [ w + 1 for w in wildcard_mask ]  # Get each element from the wildcard_mask array and add one
    addr_total = prod( wild_plus_1 )                # Multiply the values together to get the total number of addresses
    return addr_total - 2                           # Subtract 2 for the network ID and broadcast address to get the final number of valid hosts

'''
Gets the number of possible subnets for the given mask that could segment that class of network
e.g. get_num_subnets( [255, 255, 255, 128] ) -> 2

255.255.255.0 is the class C netmask
255.255.255.128 takes the 8 availabe host bits in the fourth octet, reserves one for subnetting
This segments the /24 network into 2^(subnet_bits) = 2^1 = 2 /25 subnets.
'''
def get_num_subnets( subnet_mask: list ) -> int:
    list_valid( subnet_mask )                   # Input type validation
    for oct in subnet_mask:
        if oct != 255:                          # Find the "interesting octet", i.e. the first non-255 octet
            bit_string = binary_repr( oct )     # Convert the interesting octet to binary representation
            subnet_bits = 0                     # Count the number of 1-bits
            for b in bit_string:
                if b == '1': subnet_bits += 1
            return 2 ^ subnet_bits              # Return the number of subnets based on the number of subnet bits
    return 256                                  # Should only reach this point if 255.255.255.255 is passed -> network with only 1 host, 256 1-host subnets

'''
Given a valid CIDR value, returns the string representation
e.g.
cidr_to_string( 24 ) -> '/24'
'''
def cidr_to_str( cidr: int ) -> str:
    int_valid( cidr ) # Input type validation
    if cidr >= 0 and cidr <= 32:
        sb = []
        sb.append( '/' )
        sb.append( str(cidr) )
        return ''.join( sb )
    else:
        raise ValueError( BAD_CIDR_ERROR.format(cidr) )