from re import search

# Source: https://regex101.com/library/aL7tV3?orderBy=RELEVANCE&search=ip
ipv6_regex = '^((([0-9A-Fa-f]{1,4}:){1,6}:)|(([0-9A-Fa-f]{1,4}:){7}))([0-9A-Fa-f]{1,4})$'