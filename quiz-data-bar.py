### Evan Wiederspan
### Advanced Python Lab 1
### 1-11-2017

from collections import defaultdict

print('Welcome to the Quiz Score Frequency Analyzer, written by Evan Wiederspan')
# string containing file name and the actual file object
fileName = inputFile = None
# loop until we get a valid filename
while True:
    fileName = input("Enter input data fileName: ")
    try:
        inputFile = open(fileName, 'r')
    except IOError:
        # Print message and loop back if file not found
        print('Error: could not find file {}, please try again'.format(fileName))
        continue
    break
print("Reading file '{}' input:".format(fileName))

# dictionary mapping scores to frequency
scores = defaultdict(int)
try:
    for l in inputFile:
        #caught by try-catch if incorrect format
        score, num = l.split(" ")
        print(l, end="")
        scores[int(score)] += int(num)
except ValueError:
    print("Error: File in incorrect format. Exiting program")
    exit()
finally:
    inputFile.close()

minScore = min(scores)
maxScore = max(scores)
maxFreq = scores[max(scores, key=lambda s: scores[s])]

print("\nThe smallest score value is {}".format(minScore))
print("The largest score value is {}".format(maxScore))
print("The largest frequency count is {}".format(maxFreq), end="\n\n")

print("---Input Data---")
print('Score: Frequency Bar Chart', end="\n\n")

# output the bar chart
for s in range(minScore,maxScore+1):
    print("{:>5}: {:>5}   {}".format(s, scores[s], scores[s] * '*')) # use format function for aligning output

print("\nFrequency: Score Bar Chart", end="\n\n")
for f in range(maxFreq,0,-1):
    print("    ^ {:>3}: {}".format(f, "".join("  *" if scores[s] >= f else "   " for s in range(minScore,maxScore+1))))

print("---------: " + ("--^" * (maxScore-minScore + 1)))
print("    Score: " + "".join("{:>3}".format(s) for s in range(minScore, maxScore+1)))