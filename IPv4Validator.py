# This file will act as a validator for IPv4 addresses using RegEx and will be called by calc.py

# TODO:
# Validate the IPv4 address and subnet masks/CIDR
#   
#   - Use regex to validate IPv4 addresses by ensuring they match x.x.x.x, where x is a number from 1 - 255 inclusive
#   - If given a subnet mask, just compare it against a list of the 32 valid subnet masks and compare