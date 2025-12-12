import string

# Basic sets
LOWERCASE = string.ascii_lowercase               # 'abcdefghijklmnopqrstuvwxyz'
UPPERCASE = string.ascii_uppercase               # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUMBERS = string.digits                          # '0123456789'
SPECIAL_CHARS = string.punctuation               # '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

# Combined sets
LETTERS = LOWERCASE + UPPERCASE
ALPHANUMERIC = LETTERS + NUMBERS
ALL_CHARS = ALPHANUMERIC + SPECIAL_CHARS
