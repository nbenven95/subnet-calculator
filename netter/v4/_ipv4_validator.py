"""
Helper functions for validating IPv4 addresses and subnet masks.

Author: Noah Benveniste
https://github.com/noahbenveniste/subnet-calculator
"""
#|#######################################################################| Imports |########################################################################|#

from re import search

#|###################################################################| Global constants |###################################################################|#

BAD_CIDR_ERROR = 'CIDR must be within the range [0, 32] - Value: {}'
BAD_SUBNET_MASK_ERROR = 'Invalid subnet mask - may only consist of integers within range [0, 255] (see help for a list of valid subnet masks) - Value: {}'
BAD_IPV4_ERROR = 'IPv4 address must consist of four integers within range [0, 255] separated by \'.\' - Value: {}'

#|############################################################| CIDR to subnet mask dictionary |############################################################|#

CIDR_DICT = {
    # No subnet, i.e. any address in the 2^32 IPv4 address space
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

#|#################################################################| Function definitions |#################################################################|#

def is_valid_ipv4( ipv4_str: str ) -> bool:
    """Function that validates the structure of a given IPv4 address

    Args:
        ipv4_str:
            An IPv4 address as a string.

    Returns:
        True if ipv4_str represents a valid IPv4 address, False otherwise.

    Raises:
        TypeError: Non-string input provided.
    """
    # Ensure string input
    if not isinstance( ipv4_str, str ): raise TypeError( '\'{}\' is not a valid {}'.format(ipv4_str, repr(str)) )
    '''
    This regex matches a string that begins with 3 instances of a series of digits followed by a '.'
    The digits can either be 250-255, 200-249, 100-199, or 0-99.
    The final block also matches these digits, but does not look for a '.' at the end
    Source: https://www.geeksforgeeks.org/python-program-to-validate-an-ip-address/#
    '''
    ipv4_regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])[.]){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    # Check if the input string matches the regex pattern, return the result
    return search( ipv4_regex, ipv4_str )

def is_valid_subnet_mask( subnet_mask_str: str ) -> bool:
    """Function that validates the structure of an IPv4 subnet mask

    Args:
        subnet_mask_str:
            A string representing an IPv4 subnet mask.

    Returns:
        True if subnet_mask_str represents a valid IPv4 subnet mask, False otherwise.

    Raises:
        TypeError: Non-string input provided.
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
    """Function that validates CIDR values i.e. checks that the input is in the range [0, 32]

    Args:
        cidr:
            The input integer to check.

    Returns:
        True if cidr is in the range [0, 32], False otherwise.

    Raises:
        TypeError: Non-integer input provided.
    """
    # Ensure integer input
    if not isinstance( cidr, int ): raise TypeError( '\'{}\' is not a valid {}'.format(cidr, repr(int)) )
    # Check for valid range
    return 0 <= cidr <= 32

def argument_type_validator( t: type ):
    """
    Function that returns a lambda expression that will ensure that input arguments are of a specified data type

    Args:
        t:
            The data type that the returned lambda expression will check for

    Returns:
        A lambda expression for validating argument data type
        example:
        int_checker = argument_type_validator(int)
        int_checker(3) -> True
        int_checker(3.0) -> TypeError

    Raises:
        TypeError: Input is not a data type
    """
    if not isinstance( t, type ): 
        raise TypeError
    return lambda arg : True if isinstance( arg, t ) else _raise( TypeError( '\'{}\' is not a valid {}'.format(arg, repr(t)) ) )

def _raise( e: TypeError ): 
    """Helper function that allows us to conditionally raise errors from lambda expression"""
    raise e