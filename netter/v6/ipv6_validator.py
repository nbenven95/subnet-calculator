"""
Helper functions for validating IPv6 addresses.

IPv6 regex pattern courtesy of https://gist.github.com/dfee/6ed3a4b05cfe7a6faf40a2102408d5d8

Author: Noah Benveniste
https://github.com/noahbenveniste/subnet-calculator
"""
from re import search

#|##################################################################| IPv6 regex patterns |##################################################################|#

# IPv4 segment pattern
IPV4_SEG  = r'(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])'
# Full IPv4 address pattern
IPV4_ADDR = r'(?:(?:' + IPV4_SEG + r'\.){3,3}' + IPV4_SEG + r')'
# IPv6 segment pattern
IPV6_SEG  = r'(?:(?:[0-9a-fA-F]){1,4})'
# IPv6 GRP length pattern (fixed to end of address) - up to 128 bits
IPV6_PREFIX = r'((/1[0-2][0-8])|(/[0-9]?[0-9]))?'                         # First group checks 100-128, second checks 10-99 and 0-9
# IPv6 address type groups
IPV6_GROUPS = (
r'(?:' + IPV6_SEG + r':){7,7}' + IPV6_SEG + IPV6_PREFIX,                  # 1:2:3:4:5:6:7:8[/0-128]
r'(?:' + IPV6_SEG + r':){1,7}:' + IPV6_PREFIX,                            # 1::                                 1:2:3:4:5:6:7::
r'(?:' + IPV6_SEG + r':){1,6}:' + IPV6_SEG + IPV6_PREFIX,                 # 1::8               1:2:3:4:5:6::8   1:2:3:4:5:6::8
r'(?:' + IPV6_SEG + r':){1,5}(?::' + IPV6_SEG + r'){1,2}' + IPV6_PREFIX,  # 1::7:8             1:2:3:4:5::7:8   1:2:3:4:5::8
r'(?:' + IPV6_SEG + r':){1,4}(?::' + IPV6_SEG + r'){1,3}' + IPV6_PREFIX,  # 1::6:7:8           1:2:3:4::6:7:8   1:2:3:4::8
r'(?:' + IPV6_SEG + r':){1,3}(?::' + IPV6_SEG + r'){1,4}' + IPV6_PREFIX,  # 1::5:6:7:8         1:2:3::5:6:7:8   1:2:3::8
r'(?:' + IPV6_SEG + r':){1,2}(?::' + IPV6_SEG + r'){1,5}' + IPV6_PREFIX,  # 1::4:5:6:7:8       1:2::4:5:6:7:8   1:2::8
IPV6_SEG + r':(?:(?::' + IPV6_SEG + r'){1,6})' + IPV6_PREFIX,             # 1::3:4:5:6:7:8     1::3:4:5:6:7:8   1::8
r':(?:(?::' + IPV6_SEG + r'){1,7}|:)' + IPV6_PREFIX,                      # ::2:3:4:5:6:7:8    ::2:3:4:5:6:7:8  ::8       ::
r'fe80:(?::' + IPV6_SEG + r'){0,4}%[0-9a-zA-Z]{1,}',    # fe80::7:8%eth0     fe80::7:8%1  (link-local IPv6 addresses with zone index)
r'::(?:ffff(?::0{1,4}){0,1}:){0,1}[^\s:]' + IPV4_ADDR,  # ::255.255.255.255  ::ffff:255.255.255.255  ::ffff:0:255.255.255.255 (IPv4-mapped IPv6 addresses and IPv4-translated addresses)
r'(?:' + IPV6_SEG + r':){1,6}:?[^\s:]' + IPV4_ADDR      # 2001:db8:3:4::192.0.2.33  64:ff9b::192.0.2.33 (IPv4-Embedded IPv6 Address) - fixes not matching the address '0:0:0:0:0:0:10.0.0.1'
)
# Concatenate the IPv6 address type groups into a single regex pattern
IPV6_ADDR = '|'.join(['(?:{})'.format(g) for g in IPV6_GROUPS[::-1]])  # Reverse rows for greedy match

#|##################################################################| Function definitions |#################################################################|#

def is_valid_ipv6( ipv6_str: str ) -> bool:
    """
    Function that validates the structure of an IPv6 address.

    Primarily based on regex from https://gist.github.com/dfee/6ed3a4b05cfe7a6faf40a2102408d5d8
    Added additional pattern for matching global routing prefix length at then end of IPv6 addresses
    (e.g. ::/64) which is necessary for subnet calculations.

    Args:
        ipv6_str:
            An IPv6 address as a string.

    Returns:
        True if ipv6_str represents a valid IPv6 address, false otherwise.

    Raises:
        TypeError: Non-string input provided.
    """
    # Ensure string input
    if not isinstance( ipv6_str, str ): raise TypeError( '\'{}\' is not a valid {}'.format(ipv6_str, repr(str)) )
    # Check if the input string matches the regex pattern, return the result
    result = search( IPV6_ADDR, ipv6_str )
    if result == None: return False # No match
    else: return result.group() == ipv6_str # True - full match, False - partial match

def is_valid_grp_len( ipv6_str: str) -> bool:
    """
    Function that checks a valid IPv6 address string for a global routing prefix length at the end of the address.

    This function assumes that the address string is a valid IPv6 address. It only checks that the the string contains
    a valid GRP length as a substring at the end of the string. It does not validate that the GRP length is correct
    for the class of IPv6 address (e.g. that link-local addresses are /10).

    example:
    is_valid_grp_len( '::/128' ) -> True
    is_valid_grp_len( '::/129' ) -> False

    Args:
        ipv6_str:
            An IPv6 address as a string.

    Returns:
        True if ipv6_str has a valid GRP length, False otherwise.

    Raises:
        TypeError: Non-string input provided.
    """
    # Ensure string input
    if not isinstance( ipv6_str, str ): raise TypeError( '\'{}\' is not a valid {}'.format(ipv6_str, repr(str)) )
    # Perform substring match using IPV6_PREFIX regex pattern
    _regex = r'(' + IPV6_PREFIX + r')$' # Ensure that the pattern appears at the end of the string
    result = search( _regex, ipv6_str )
    if result == None: return False # No match
    else: return result.group() == ipv6_str # True - full match, False - partial match

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