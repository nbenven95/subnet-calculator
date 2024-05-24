# TODO:
# Validate the IPv4 address and subnet masks/CIDR
#   
#   - Use regex to validate IPv4 addresses by ensuring they match x.x.x.x, where x is a number from 1 - 255 inclusive
#   - If given a subnet mask, just compare it against a list of the 32 valid subnet masks and compare

def validate_ipv4_str( ipv4_str: str ) -> bool:
    """
    """
    # Use regex to validate
    return True

def validate_subnet_mask_str( subnet_mask_str: str ) -> bool:
    """
    """
    # Use a lookup table of all IPv4 subnet masks, loop through and compare the input string against all existing strings
    return True

def validate_cidr_int( cidr: int ) -> bool:
    """
    """
    # Ensure that CIDR is in the range [0,32]
    return True

def int_list_to_string( int_list: list ) -> str:
    """
    """
    # Validate the input type -> check that its a list, check that all elements are ints
    # Convert the list to an IPv4 string using the delimiter logic from _ipv4_calculator -> don't validate anything, just convert
    return ""

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