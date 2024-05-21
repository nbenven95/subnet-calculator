#!/usr/bin/env python3

# netter.py validates and calculates detailed IPv4 subnet information given an arbitrary IPv4 address and subnet mask/CIDR
# TODO:
# - Flags for varying output options (e.g. only output first/last host) and a flag to write output directly to a text file (for use with nmap -iL <filename>)
# - IPv6 functionality
# - VLSM validator/calculator/planner/optimizer
#   - Given a valid subnet, display all possible segmentation options
#   - e.g. user inputs x.x.x.x 255.255.255.0 -> x1 /24, x2 /25, x4 /26, x8 /27, x16 /28, x32 /29, x64 /30, x128 /31, x256 /32
#   - Read/write VLSM planning info to text file
#   - Validate VLSM configuration 
#   - Given a valid VLSM configuration, display ranges of used and unused addresses, % unused address space, how optimal the configuration is, etc.
#   - Given a valid, non-optimal VLSM configuration, suggest an optimized alternative

from argparse import ArgumentParser
from argparse import ArgumentTypeError

# import ipv4_calculator
# import ipv4_validator

# validate_ipv4( ipv4_string ) <- call using argparse type field
# validate_netmask( subnetmask_string ) <- call using argparse type field
# validate CIDR values using argparse range

# subnet_from_mask( ipv4_string, subnetmask_string )

# OR

# Need a function that can parse a CIDR notation string and return a tuplet containing the address string and CIDR integer value
#   e.g parse_cidr( e.g. '192.168.10.1/24' ) -> ( '192.168.10.1', 24 )
# subnet_from_cidr( ipv4_string, cidr )