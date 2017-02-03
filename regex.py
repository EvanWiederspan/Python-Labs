# Evan Wiederspan
# Advanced Python Lab 3 - Regex
# 1-25-2017

from re import fullmatch

# Exercise 1-4: Valid variable identifier
# Can be upper or lowercase letters, underscores, or digits
# First characters must be a letter or an underscore
idReg = r'[A-z_][\w]*'

# Exercise 1-5: Valid street address
# Group of numbers followed by at least one mix of letters and numbers
# if one of the second group has numbers at its start, can only be followed by two letters (23rd, 21st)
# numbers can't be randomly in the middle of words
saReg = r'\d+(?: +[A-z]+| \d+[A-z]{2})+'

# Exercise 1-6: Valid web domain
# www, followed by multiple groups of alphanumerics and dashes with a period at the end, followed by 'com'
# Examples: www.google.com ; www.evan.wiederspan.com ; www.abc.123.other.com
wwwReg = r'www\.(?:[\w-]+\.)+com'

# Exercise 1-7: Valid integer literal
# Can be any of the following:
# - group of integers
# - a binary number that starts with 0b, followed by a combo of 1's and 0's
# - an octal number that starts with 0o, followed by a combo of 0-7's
# - a hexadecimal number that starts with 0x, followed by a combo of 0-F's
# optional - sign at the beginning for all of the above
intReg = r'-?(?:0[Xx][\dA-Fa-f]+|0[Bb][01]+|0[Oo][0-7]+|\d+)'

# Exercise 1-11: Valid email
# Alphanumeric characters, optionally separated by single periods,
# Ip address can be before the @ symbol in the form <[127.0.0.1]>
# must have exactly one @ symbol
# domain name after @ symbol must have at least one dot, but can have more
# domain name can also be valid ip address surrounded by square braces (e.g. [127.0.0.1])
# optionally, just before the @ symbol, the email can have double quotes ("), with anything allowed inside,
# even more @ symbols or whitespace
emailReg = r'(?:\.?\w+|\.?\"[^\"]+\")*(?:<\[\d{1,3}(?:\.\d{1,3}){3}\]>)?@(?:\[\d{1,3}(?:\.\d{1,3}){3}\]|\w+(?:\.\w+)+)'

# Exercise 1-12: Returns if string is a valid url
# optional http:// or https:// at the start of the url
# domain name needs to be alphanumeric characters separated by a single period
# (e.g. google.com, www.google.com, wiederspane1.cs.spu.edu)
# optionally followed by alphanumeric characters separated by a single /
# (e.g. www.example.com/this/is/an/example)
# last one can have a file extension
# (e.g. www.example.com/stuff/help.php)
# finally, an optional question mark followed by alphanumeric and special characters
# to represent GET parameters
# (e.g. outlook.com/owa/inbox.php?realm=spu.edu)
urlReg = r'(?:https?://)?[\w-]+(?:\.[\w-]+)+(?:/[\w_-]+)*(?:\.\w+)?(?:/?\?[\w+&=%\.]+)?'

def runTests(file, reg, desc, cases):
    '''Helper function to run regex test cases
    file - file object to write to
    reg - the regex to test against
    desc - string description to print out with the group of test cases
    cases - a list of tuples. Each tuple should contain a string followed by a boolean
    the string is the one to test against, the boolean is whether or not it should pass
    '''
    results = [(fullmatch(reg, test) != None) == match for test, match in cases]
    alignLen = max(len(case[0]) for case in cases) + 2
    print(desc, file=file)
    print(str(results.count(True)) + "/" + str(len(results)) + " passed", file=file)
    for i, t in enumerate(results):
        print((("'" + cases[i][0] + "'").ljust(alignLen, ' ') +  " should " + ("pass " if cases[i][1] else "fail ")) + "-- " + ("OK" if t else "FAILED"), file=file)
    print('-' * 15, file=file)

# --- write to tests.txt, with statement takes care of closing the file and IO Errors --- 
with open('tests.txt', 'w') as f:
# --- begin running tests ---
    runTests(f, idReg, "Variable Regex", [('abc', True), ('123', False), ('abc123', True), ('AA_AA', True), ("cant have spaces", False), ("", False)])
    runTests(f, saReg, "Street Address Regex", [('', False), ('3023 ', False), ('3023 3rd', True), ('3rd 3023', False), ('3023 rd3', False), ('asdf', False), ('3023 23232', False), ('3023 3rd ave W', True), ("3210 De la Cruz Boulevard", True)])
    runTests(f, wwwReg, "WWW Regex", [('www.google.com', True), ('', False), ('12312312', False), ('spu.edu', False), ('www..com', False), ('www.123.com', True), ('www.a.b.com', True)])
    runTests(f, intReg, "Integer Literal Regex", [('0', True), ('123', True), ('0b10101', True),('0b0', True), ('0b', False), ('0o', False), ('0o23999', False), ('0O176', True), ('0x', False), ('0xfFaA', True), ('0X123', True), ('', False), ('-3', True), ('-0b10101', True), ('--3', False)])
    runTests(f, emailReg, "Email Regex", [('wiederspane1@spu.edu', True), ('', False), ('what.ever@gmail.info.com', True), ('me@bad@gmail.com', False), ('not@real.', False), ('this.one."is@weird"@gmail.com', True), ('"Evan"<[127.0.0.1]>@gmail.com', True), ("<[127.0.1]>@gmail.com", False), ("evan@[127.0.0.1]", True)])
    runTests(f, urlReg, "URL Regex", [('', False), ('www.google.com', True), ('google.com/maps/location', True), ('www.google..com', False), ('google.com//too//many///slashes', False), ('needs/some/dots', False), ('http://facebook.com', True), ("https://z.com/zz/?get=true", True), ('http://nope/not.real.com', False), ('ht://http.only', False), ("example.com/stuff/help.php", True), ("example.com/help.php/stuff", False), ("example.com/stuff/help.php?get=true&stuff=yes", True)])