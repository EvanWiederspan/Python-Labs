# Evan Wiederspan
# Advanced Python Lab 4: Stock Fetching
# February 1, 2017

import re
from urllib.request import urlopen

# tag names for generating output
tagNames = ('qSymbol', 'qDate', 'qTime', 'qLastSalePrice', 'qBidPrice', 'qAskPrice', 'q52WeekLow', 'q52WeekHigh', 'qTodaysLow', 'qTodaysHigh', 'qNetChangePrice', 'qShareVolumeQty', 'qTotalOutstandingShareQty')

# regex used for slicing up the received data, basically splits everything into capture groups,
# leaving out quotation marks and allowing for N/A as an option
# the regex is fairly open and will accept alot, its main purpose is easily split up the pieces of data
dataReg = re.compile(r'[^"]*"([\w/]+)","?([\w/]+)"?,"?([\w/:]+)"?,([\w./]+),([\w./]+),([\w./]+),(?:"([\d.]+) - ([\d.]+)"|N/A),(?:"([\d.]+) - ([\d.]+)"|N/A),([\w./+-]+),(\w+),([ \w,/]+)')

# maximum number of symbols allowed per API call
maxSyms = 10

def ProcessQuotes(*strSyms):
    # removes empty or non-alphanumeric stock symbols, printing an error message for the latter
    strSyms = tuple(filter(lambda s: len(s) > 0 and (s.isalpha() or print("invalid stock symbol " + s)), strSyms))
    # loop through all symbols, only allowing maxNum per API call
    for i in range(0,len(strSyms), maxSyms):
        strUrl='http://finance.yahoo.com/d/quotes.csv?f=sd1t1l1bawmc1vj2&e=.csv&s='
        # capitalize all symbols before sending off
        strUrl += "+".join(map(str.upper, strSyms[i:i+maxSyms]))
        try:
            # handles closing the connection
            with urlopen(strUrl) as f:
                # will run once per symbol passed in
                for n, line in enumerate(f.readlines(), i):
                    # run regex
                    regMatch = dataReg.match(str(line))
                    # skip if data was not a match, probably from a fake symbol
                    if regMatch is None:
                        print("Invalid data for symbol " + strSyms[n])
                        continue
                    # get all capture groups from regex as a list, will be all data in correct order
                    data = list(regMatch.groups())
                            
                    # looks a little weird but this strips out spaces and commas
                    # from the total outstanding share qty
                    data[-1] = data[-1].translate(str.maketrans('','',' ,'))

                    # pair up data to tags and remove any with N/A or None as the data value
                    pairs = tuple(filter(lambda p: p[0] != "N/A" and p[0] is not None, zip(data, tagNames)))

                    # create tags and print data
                    # any tags with N/A will not be printed because they were pulled out by the above filter
                    print("<stockquote>\n\t" + "\n\t".join(map(lambda d: "<{}>{}</{}>".format(d[1],d[0],d[1]), pairs)) + "\n</stockquote>")
        except ValueError: # thrown when url is invalid
        # shouldn't happen since symbols with potentially destructive symbols are filtered out
            print("Invalid url: " + strUrl)

# main code, ask for input in infinite loop
while True:
    syms = input("Enter comma separated stock symbols: ")
    # separate by comma and strip spaces off of ends
    ProcessQuotes(*map(str.strip, syms.split(",")))
    