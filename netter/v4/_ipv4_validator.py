# TODO:
# Validate the IPv4 address and subnet masks/CIDR
#   
#   - Use regex to validate IPv4 addresses by ensuring they match x.x.x.x, where x is a number from 1 - 255 inclusive
#   - If given a subnet mask, just compare it against a list of the 32 valid subnet masks and compare

#|##################################################| CIDR to subnet mask dictionary |##################################################|#

CIDR_DICT = {
    # No subnet, i.e. any address in the 2^32 IPv4 address space (TODO: Handle this with an edge case)
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

def is_valid_ipv4( ipv4_str: str ) -> bool:
    """
    """
    # Use regex to validate
    return True

def is_valid_subnet_mask( subnet_mask_str: str ) -> bool:
    """
    """
    # Ensure string input
    if not isinstance( subnet_mask_str, str ): raise TypeError( '\'{}\' is not a valid {}'.format(subnet_mask_str, repr(str)) )
    # Loop over all values in the CIDR dictionary
    for cidr in CIDR_DICT:
        # Compare each value to the input; if there's a match, return True
        if CIDR_DICT[ cidr ] == subnet_mask_str: return True
    # If no match is found, return False
    return False

def is_valid_cidr( cidr: int ) -> bool:
    """
    """
    # Ensure integer input
    if not isinstance( cidr, int ): raise TypeError( '\'{}\' is not a valid {}'.format(cidr, repr(int)) )
    # Check for valid range
    return 0 <= cidr <= 32

def argument_type_validator( t: type ):
    '''
    Function that returns a lambda expression that will validate input arguments of an arbitrary data type
    e.g.
    float_valid = argument_type_validator( float )
    float_valid( 3.14 ) -> True
    float_valid( 3 ) -> raise TypeError

    int_valid = argument_type_validator( int )
    int_valid( 3 ) -> True
    int_valid( 3.14 ) -> raise TypeError
    '''
    if not isinstance( t, type ): 
        raise TypeError
    return lambda arg : True if isinstance( arg, t ) else _raise( TypeError( '\'{}\' is not a valid {}'.format(arg, repr(t)) ) )

def _raise( e: TypeError ): 
    '''Helper function that allows us to conditionally raise errors from lambda expression'''
    raise e