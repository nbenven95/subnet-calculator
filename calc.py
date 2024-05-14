# calc.py contains the bulk of the logic for calculating subnets. Used by netcalc.py to
# get subnet information given an arbitrary IPv4 address and subnet mask or CIDR value.

# TODO: Finish input validation

from numpy import bitwise_and
from numpy import bitwise_or
from numpy import bitwise_not
from numpy import binary_repr
 
#   Class C subnet example: 
#   - Given 192.168.10.129 255.255.255.128
#   - Mask: 11111111 11111111 11111111 10000000
#   - Addr: 11000000 10101000 00001010 10000001
#   - AND:  11000000 10101000 00001010 10000000 <- Network ID = address & netmask = 192.168.10.128
#
#   - Increment NetID by 1 to get the first usable host address = 192.168.10.129
#
#   - Wild: 00000000 00000000 00000000 01111111 <- Wildcard mask = ~(netmask)
#   - OR:   11000000 10101000 00001010 11111111 <- Broadcast address = netID | wildcard = 192.168.10.255
#
#   - Decrement Broadcast by 1 to get last usable host address = 192.168.10.254
#
#   Output:
#
#   Network ID:         192.168.10.128
#   First host:         192.168.10.129
#   Last host:          192.168.10.254
#   Broadcast:          192.168.10.255
#   Subnet class:       C
#   # of subnets:       2^1 = 2
#   # hosts/subnet:     2^7 - 2 = 126

#   Class B subnet example:
#   - Given 172.16.31.40 255.255.240.0
#   - Mask: 11111111 11111111 11110000 00000000
#   - Addr: 10101100 00010000 00011111 00101000
#   - ID:   10101100 00010000 00010000 00000000 = 172.16.16.0
#
#   - First host: 172.16.16.1
#
#   - Wild: 00000000 00000000 00001111 11111111
#   - Brd:  10101100 00010000 00011111 11111111 = 172.16.31.255 <- wild | id
#
#   - Last host: 172.16.31.254
#
#   Output:
#
#   Network ID:         172.16.16.0
#   First host:         172.16.16.1
#   Last host:          172.16.31.254
#   Broadcast:          172.16.31.255
#   Subnet class:       B
#   # of subnets:       2^4 = 16
#   # hosts/subnet:     2^12 - 2 = 4094

##### CIDR to subnet mask dictionary #####

cidr_dict = {
    # This means no subnet, or any address in the entire IPv4 address space. Should probably handle as a special edge case.
    0 : '0.0.0.0',
    # /1 - /7 subnets (/1 takes the full IPv4 address space and divides it in half once, /2 halves each of the /1 networks, etc.)
    1 : '128.0.0.0',
    2 : '192.0.0.0',
    3 : '224.0.0.0',
    4 : '240.0.0.0',
    5 : '248.0.0.0',
    6 : '252.0.0.0',
    7 : '254.0.0.0',
    # Class A subnets (i.e. subnetted class A network)
    8 : '255.0.0.0',
    9 : '255.128.0.0',
    10 : '255.192.0.0',
    11 : '255.224.0.0',
    12 : '255.240.0.0',
    13 : '255.248.0.0',
    14 : '255.252.0.0',
    15 : '255.254.0.0',
    # Class B subnets (i.e. subnetted class B network)
    16 : '255.255.0.0',
    17 : '255.255.128.0',
    18 : '255.255.192.0',
    19 : '255.255.224.0',
    20 : '255.255.240.0',
    21 : '255.255.248.0',
    22 : '255.255.252.0',
    23 : '255.255.254.0',
    # Class C subnets (i.e. subnetted class C network)
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

# Returns IPv4 subnet information given an IPv4 address and a subnet mask
def get_subnet_info_given_mask( ipv4_str, subnet_mask_str ):
    ipv4 = parse_addr_str( ipv4_str ) # Get the IPv4 octet values as an array
    subnet_mask = parse_addr_str( subnet_mask_str ) # Get the netmask octet values as an array
    wildcard_mask = bitwise_not( subnet_mask ) # Get the wildcard mask
    network_id = bitwise_and( ipv4, subnet_mask ) # Bitwise AND to extract network bits
    broadcast = bitwise_or( network_id, wildcard_mask ) # Bitwise OR to get the broadcast address
    first_host = get_first_host( network_id ) # Get the first host address
    last_host = get_last_host( broadcast ) # Get the last host address
    subnet_class = get_subnet_class( subnet_mask ) # Get the subnet class
    num_hosts = get_num_hosts( subnet_mask )
    num_subnets = get_num_subnets( subnet_mask )

# Returns IPv4 subnet information given an IPv4 address and a CIDR value
def get_subnet_info_given_cidr( ipv4_str, cidr ):
    mask_str = cidr_to_netmask( cidr )
    return get_subnet_info_given_mask( ipv4_str, mask_str )

# Uses the CIDR dictionary to look up the corresponding subnet mask
def cidr_to_netmask( cidr ):
    try:
        cidr = int(cidr)
        if cidr < 0 | cidr > 32:
            raise ValueError('CIDR must be within the range [0,32]. Given: {}'.format(cidr))
    except ValueError:
        raise TypeError('{} is not a valid integer'.format(cidr))
    return cidr_dict[ cidr ]

# Parses an IPv4 address/netmask for octet values and returns an array containing the integer values
# e.g. parse_addr_str( '192.168.10.1' ) -> [192, 168, 10, 1]
def parse_addr_str( addr_string ):
    raise NotImplementedError( 'parse_addr_str( addr_string ) not implemented' )
    return 0

# Finds the first host address given the network ID
def get_first_host( net_id ):
    return [ sum(x) for x in zip( net_id, [0, 0, 0, 1] ) ] # Get the first host addr by incrementing the net ID by 1

# Finds the last host address given the broadcast addr
def get_last_host( broadcast ):
    return [ sum(x) for x in zip( broadcast, [0, 0, 0, -1] ) ] # Get the last host addr by decrementing the broadcast addr by 1

# Given a subnet mask in the form of an array of octets, returns the subnet class
# e.g. get_subnet_class( [255, 255, 255, 0] ) -> C
def get_subnet_class( subnet_mask ):
    if subnet_mask[0] != 255:
        return 'none'
    elif subnet_mask[1] != 255:
        return 'A'
    elif subnet_mask[2] != 255:
        return 'B'
    else:
        return 'C'

# Gets the number of host addresses for the given subnet, minus the network ID and broadcast address
def get_num_hosts( subnet_mask ):
    for oct in subnet_mask:
        if oct != 255:
            host_bits = get_num_host_bits( oct, subnet_mask )
            return 2^host_bits - 2
            
# Gets the number of possible subnets for the given mask that could segment that class of network
# e.g. get_num_subnets( [255, 255, 255, 128] ) -> 2 -> b/c 255.255.255.0 is for class C networks, 255.255.255.128 segments that class C network into two /25 subnets
def get_num_subnets( subnet_mask ):
    for oct in subnet_mask:
        if oct != 255:
            subnet_bits = get_num_subnet_bits( oct )
            return 2^subnet_bits

# Gets the number of subnet bits by counting the number of 1 bits in the given octet
def get_num_subnet_bits( octet ):
    bit_string = binary_repr( octet )
    count = 0
    for b in bit_string:
        if b == '1': count += 1
    return count

# Gets the number of host bits for an octet by subtracting the number of subnet bits from 8 (8 bits per 1-byte octet)
def get_num_host_bits( octet, subnet_mask ):
    class_to_extra_bits = { # Depending on the subnet class, need to add on extra bits to get the total number of host bits
        'none' : 24,
        'A' : 16,
        'B' : 8,
        'C' : 0
    }
    return 8 - get_num_subnet_bits( octet ) + class_to_extra_bits[ get_subnet_class( subnet_mask ) ]