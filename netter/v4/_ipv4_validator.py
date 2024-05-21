# TODO:
# Validate the IPv4 address and subnet masks/CIDR
#   
#   - Use regex to validate IPv4 addresses by ensuring they match x.x.x.x, where x is a number from 1 - 255 inclusive
#   - If given a subnet mask, just compare it against a list of the 32 valid subnet masks and compare

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
def argument_type_validator( t: type ):
    if not isinstance( t, type ): 
        raise TypeError
    return lambda arg : True if isinstance( arg, t ) else _raise( TypeError( '\'{}\' is not a valid {}'.format(arg, repr(t)) ) )

'''
Helper function that allows us to conditionally raise errors from lambda expression
'''
def _raise( e: TypeError ): raise e