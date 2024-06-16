from v6.ipv6_validator import argument_type_validator
from v6.ipv6_validator import IPV6_PREFIX
from re                import findall
from re                import search
from re                import split

"""
https://docs.oracle.com/cd/E18752_01/html/816-4554/ipv6-overview-10.html

###### IPv6 address structure ######

xxxx : xxxx : xxxx : yyyy : zzzz : zzzz : zzzz : zzzz

- 128 bits / 8 blocks of 4 hex digits (4 bits * 4 hex * 8 blocks = 128 bits)
- x/y bits = Global Routing Prefix (GRP) = leftmost bits, used for global routing (up to 64 bits)
- GRP is futher divided into 2 parts:
    - x bits = Site Prefix = leftmost bits (up to 48), assigned by ISP, used for routing
    - y bits = Subnet ID = 64 - (site prefix length); describes the internal topology/number of subnets available for private network
- z bits = Interface ID = used to uniquely identify hosts

##### IPv6 prefixes #####
- Two types:
1. Site prefix - occupies up to 48 bits
    e.g. 2001:db8:acad::1/48 - indicates a 48 bit long site prefix -> 64 - 48 = 16 subnet bits
2. Subnet prefix - always /64, includes the 48 bits for the site prefix 
    - In this case, I'm guessing there's an implicit assumption that the site prefix is 48 bits and subnet ID is 16 bits

##### How to determine subnet bits #####
Case 0 (default): Site prefix = 48 bits, Subnet bits = 16 [No /# at the end of address]
Case 1: User specifies site prefix
    Case 1.1: Site prefix /0 - /63
    - Subnet bits = 64 - (site prefix length)
    Case 1.2: Site prefix /64 - /128 [Not sure what the use case would be for this other than private networks]
"""

#|##########################################################| Argument type validator functions |############################################################|#

# Each of these calls returns a lambda expression that will check if an input argument matches the specified data type
ensure_dtype_str = argument_type_validator( str )
ensure_dtype_int = argument_type_validator( int )
ensure_dtype_list = argument_type_validator( list )

#|#################################################################| Function definitions |##################################################################|#

def get_ipv6_subnet_info( ipv6_str: str ) -> dict:
    """
    Given a valid, arbitrary IPv6 address string, returns a dictionary of detailed subnet information.
    """

    # Convert ipv6_str to bit string format, store in a global variable so functions don't have to make the conversion mulitple times

    return {}

def get_network_id() -> str:
    """
    Given a valid IPv6 address string, gets the network block/ID portion.
    """
    return ''

def get_if_id( ipv6_str: str ) -> str:
    """
    Given a valid IPv6 address string, gets the interface ID portion.
    """
    return ''

def get_subnet_bits( ipv6_str: str ) -> str:
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

def get_ipv6_expanded() -> str:
    """
    Given a valid IPv6 address string, returns a copy in expanded form to show all 32 digits.
    (Just get the expanded hex blocks from the ipv6_bits dictionary)
    """
    return ''

#|#############################################################| String manipulation functions |##############################################################|#

def get_subnet_prefix( ipv6_str: str ) -> int:
    """
    Given a valid IPv6 string, returns the length of the global routing prefix/subnet prefix
    """
    # Ensure string input
    ensure_dtype_str( ipv6_str )
    # Perform substring match using IPV6_PREFIX regex pattern
    regex = r'(' + IPV6_PREFIX + r')$' # Ensure that the pattern appears at the end of the string
    result = search( regex, ipv6_str )
    if result == None: 
        return -1 # No match found
    else: 
        start_index = result.span()[0] # Starting index for the substring
        grp_len = ipv6_str[start_index+1:] # Get the GRP length substring (minus the leading "/" character)
        try:
            return int( grp_len ) # Attempt to cast to int and return
        except ValueError:
            return -2 # Failed to cast substring to integer

def parse_ipv6_str( ipv6_str: str ) -> dict:
    """
    """
    # Ensure string input
    ensure_dtype_str( ipv6_str )
    # Expand the address
    ipv6_expanded_str = expand_ipv6( ipv6_str )
    # Split the address on the ":" character, generating a list of 8 hexadecimal numbers as strings
    ipv6_hextets_str = split( r':', ipv6_expanded_str )
    # Convert the hex strings to decimal using int("hex_val", 16) [may raise an error if failure to cast to int]
    ipv6_hextets_dec = [ int( h, base=16 ) for h in ipv6_hextets_str ]
    # Store result in dictionary mapping each decimal value to the corresponding hex block

def expand_ipv6( ipv6_str: str ) -> str:
    """
    [ Step 1. Expand double colons "::" ]
    -------------------------------------
    1. Check for "::" substring
    2. If there's a match, count the number of ":" exact matches over the string -> use this to determine number of 0 blocks to insert
        2a. If none are found, also check if there are any characters before or after the "::"
        e.g.
        Edge cases (check for these first):
        i).     :: -> 8x zero blocks: 0:0:0:0:0:0:0:0 - no colons -> 8 zero blocks
        ii).    1:: -> 7x zero blocks 1:0:0:0:0:0:0:0 - no colons, 1 hextet before double colon -> 7 zero blocks after double colon
        iii).   ::1 -> 7x zero blocks 0:0:0:0:0:0:0:1 - no colons, 1 hextet after double colon -> 7 zero blocks before double colon
        General cases:
        i).     1::1 -> 6x zero blocks: 1:0:0:0:0:0:0:1 - no colons -> replace double colon with 6 zero blocks
        ii).    1:2::3 -> 5x zero blocks: 1:2:0:0:0:0:0:3 - 1 colon -> replace double colon with 5 zero blocks
        iii).   1:2::3:4 -> 4x zero blocks: 1:2:0:0:0:0:3:4 - 2 colons -> replace double colon with 4 zero blocks
        iv).    1:2:3::4:5 -> 3x zero blocks: 1:2:3:0:0:0:4:5 - 3 colons -> replace double colon with 3 zero blocks
        v).     1:2:3::4:5:6 -> 2x zero blocks: 1:2:3:0:0:4:5:6 - 4 colons -> replace double colon with 2 zero blocks
        vi).    1:2:3:4::5:6:7 -> 1x zero blockS: 1:2:3:4:0:5:6:7 - 5 colons -> replace double colon with 1 zero blocck
        vii).   1:2:3:4:5:6:7:8 -> fully expanded address - 7 colons -> no zero block insertions necessary
    """
    # Edge case 1: Match exactly '::'
    regex_edge_case_1 = r'^::$'
    # Edge case 2: Match x:: to xxxx::, where x is any valid hex digit
    regex_edge_case_2 = r'(?<!.)[0-9a-fA-F]{1,4}::(?!.)'
    # Edge case 3: Match ::x to ::xxxx, where x is any valid hex digit
    regex_edge_case_3 = r'(?<!.)::[0-9a-fA-F]{1,4}(?!.)'
    # Regex to match single colons by using negative lookbehind and lookahead to ensure the preceeding and following characters are not colons
    regex_single_colon = r'(?<!:):(?!:)' 

    # Check if the IPv6 string has double colon notation that must be expanded, and that it hasn't been covered by edge case 2 or 3
    result = search(r'::', ipv6_str)
    if not result == None:
        # Get the starting index of the "::" substring
        i = result.span()[0]
        # Get the ending index of the "::" substring
        j = result.span()[1]
        # Check edge cases first
        if not search( regex_edge_case_1, ipv6_str ) == None:
            # Trivial case - '::'
            return '0000' + ':0000'*7
        elif not search( regex_edge_case_2, ipv6_str ):
            # Match x:: to xxxx::
            ipv6_str = ipv6_str[:i] + ':0000'*7
        elif not search( regex_edge_case_3, ipv6_str ):
            # Match ::x to ::xxxx
            ipv6_str = '0000:'*7 + ipv6_str[j:]
        else:
            # Count the number of single colons in the string to determine how many zero blocks to insert over the double colon
            num_zero_blocks = 6 - len( findall(regex_single_colon, ipv6_str) )
            # Build the expansion substring
            zeros_expanded = ':0000' * num_zero_blocks
            # Insert the expansion substring
            ipv6_str = ipv6_str[:i] + zeros_expanded + ipv6_str[i+1:]
    """
    [ Step 2: Add leading 0s ]
    --------------------------
    """
    # Check for leading zeros - split on ":"
    hextets = split(r':', ipv6_str)
    # List comprehension that checks the length of each hextet and pads it with the appropriate number of leading 0s (the if/else is probably redundant, but it's good practice)
    hextets_padded = [ '0'*(4-len(h)) + h if len(h) < 4 else h for h in hextets ]
    # Re-insert the ":" between each hextet (remove the final ":" appended to the end)
    ipv6_expanded_tokens = [ h for i in hextets_padded for h in [i, ':'] ][:-1] # No idea how this works, sourced from https://stackoverflow.com/questions/66882498/insert-element-in-python-list-after-every-other-element-list-comprehension
    # Join the list into a single string and return
    return ''.join(ipv6_expanded_tokens)


def remove_subnet_prefix_substr( ipv6_str: str ) -> str:
    """
    Removes the '/[0-128]' from the end of the IPv6 address string.

    example:
    remove_subnet_prefix_substr( 'fe80::/10' ) -> 'fe80::'

    """
    # Ensure string input
    ensure_dtype_str( ipv6_str )
    # Get the GRP length
    grp_len = get_subnet_prefix( ipv6_str )
    # Remove characters equaling the number of digits in grp_len, minus an additional 1 for the leading / character
    return ipv6_str[:len( ipv6_str )-len( str(grp_len) )-1]

def get_subnet_prefix_str( ipv6_str: str ) -> str:
    """
    Given a valid IPv6 address string, gets the global routing prefix portion.
    """
    return ''
