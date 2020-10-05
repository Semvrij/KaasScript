from src.functions import getLangSettings, getWhileLoopLimit

DIGITS = '0123456789'
ASCII_LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'
ASCII_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS = ASCII_LOWERCASE + ASCII_UPPERCASE
LETTERS_DIGITS = LETTERS + DIGITS
PUNCTUATION = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
CURRENT_LANG = getLangSettings()
WHILELOOPLIMIT = getWhileLoopLimit()
