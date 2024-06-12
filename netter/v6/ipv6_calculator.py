from v6.ipv6_validator import argument_type_validator
from v6.ipv6_validator import IPV6_PREFIX
from re                import search

#|##########################################################| Argument type validator functions |###########################################################|#

# Each of these calls returns a lambda expression that will check if an input argument matches the specified data type
ensure_dtype_str = argument_type_validator( str )
ensure_dtype_int = argument_type_validator( int )
ensure_dtype_list = argument_type_validator( list )

#|#################################################################| Function definitions |#################################################################|#

def get_ipv6_subnet_info( ipv6_str: str ) -> dict:
    """
    Given a valid, arbitrary IPv6 address string, returns a dictionary of detailed subnet information.
    """
    return {}

def get_ipv6_expanded( ipv6_compressed: str ) -> str:
    """
    Given a valid IPv6 address string, returns a copy in expanded form to show all 32 digits.
    """
    return ''

def get_grp_len( ipv6_str: str ) -> int:
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
        
def get_grp_str( ipv6_str: str ) -> str:
    """
    Given a valid IPv6 address string, gets the global routing prefix portion.
    """
    return ''
        
def remove_grp_len_substr( ipv6_str: str ) -> str:
    """
    Removes the '/[0-128]' from the end of the IPv6 address string.

    example:
    remove_grp_len_substr( 'fe80::/10' ) -> 'fe80::'

    """
    # Get the GRP length
    grp_len = get_grp_len( ipv6_str )
    # Remove characters equaling the number of digits in grp_len, minus an additional 1 for the leading / character
    return ipv6_str[:len( ipv6_str )-len( str(grp_len) )-1]

def get_if_id( ipv6_str: str ) -> str:
    """
    Given a valid IPv6 address string, gets the interface ID portion.
    """
    return ''

def get_subnet_bits( ipv6_str: str ) -> str:
    return ''

def get_network_id() -> str:
    return ''

def get_num_subnets() -> int:
    return 0

def get_num_hosts_on_subnet() -> int:
    return 0

def get_num_hosts_total() -> int:
    return 0

def get_first_host() -> str:
    return ''

def get_last_host() -> str:
    return ''