# Evan Wiederspan
# Advanced Python Lab 2: Calendar
# 1-18-2017

def isLeapYear(n):
    """Returns boolean value indicating if n is a leap year"""
    return (n % 4 == 0 and n % 100 != 0) or n % 400 == 0

def getMonthLength(n, y):
    """Given number of month (0-based), and the year, return length of month"""
    if n == 1: # February
        return (isLeapYear(y) and 29) or 28
    # 30 if april, june, september, or november
    return 30 if n in {3,5,8,10} else 31

def getJan1(y):
    """Return day of the week of January 1st in year y (0-based)"""
    return (y + (y-1)//4 - (y-1)//100 + (y-1)//400) % 7

months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
weekString = " Sun Mon Tue Wed Thu Fri Sat"
# width to align every line to
w = len(weekString)

year = 0
while True:
    year = input("Please enter a year: ")
    if len(year) == 4 and year.isnumeric():
        break
    else:
        print("Invalid value, try again")

# automatically takes care of IOexceptions and closing the file
with open('calendar' + str(year) + '.txt', 'w') as f:
    # day that the month begins on (0-based)
    offset = getJan1(int(year))
    for num,month in enumerate(months):
        f.write((month + " " + str(year)).center(w) + '\n')
        f.write(weekString + '\n')
        monthLength = getMonthLength(num,int(year))
        days = (["    "] * offset) + [str(d).rjust(4) for d in range(1,monthLength+1)]
        for w in range(0,monthLength + offset,7):
            f.write("".join(days[w:w+7]) + '\n')
        f.write('\n')
        offset = (offset + monthLength) % 7