#!/usr/bin/env python3

# This script will be what the user actually calls on the command line and will contain mostly user interface and argument parsing logic

from argparse import ArgumentParser
from argparse import ArgumentTypeError

# import calc               <- TODO: implement
# import ipv4-validator     <- TODO: implement

# validate_ipv4( ipv4_string ) <- call using argparse type field
# validate_mask( subnetmask_string ) <- call using argparse type field
# validate CIDR values using argparse range

# subnet_from_mask( ipv4_string, subnetmask_string )
# OR
# subnet_from_cidr( ipv4_string, cidr )