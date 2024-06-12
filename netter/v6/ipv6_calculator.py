from v6.ipv6_validator import argument_type_validator
from v6.ipv6_validator import IPV6_PREFIX
from re                import search

#|##########################################################| Argument type validator functions |###########################################################|#

# Each of these calls returns a lambda expression that will check if an input argument matches the specified data type
ensure_dtype_str = argument_type_validator( str )
ensure_dtype_int = argument_type_validator( int )
ensure_dtype_list = argument_type_validator( list )

#|#################################################################| Function definitions |#################################################################|#

def get_grp_len( ipv6_str: str) -> int:
    """
    Given a valid IPv6 string, returns the length of the global routing prefix.
    """
    # Ensure string input
    ensure_dtype_str( ipv6_str )
    # Perform substring match using IPV6_PREFIX regex pattern
    _regex = r'(' + IPV6_PREFIX + r')$' # Ensure that the pattern appears at the end of the string
    result = search( _regex, ipv6_str )
    if result == None: 
        return -1 # No match found
    else: 
        substr_start_index = result.span()[0] # Starting index for the substring
        grp_len_substr = ipv6_str[substr_start_index+1:] # Get the GRP length substring (minus the leading / character)
        try:
            return int( grp_len_substr ) # Attempt to cast to int and return
        except ValueError:
            return -2 # Failed to cast substring to integer