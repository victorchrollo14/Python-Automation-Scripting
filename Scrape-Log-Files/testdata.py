import sys
import re


def final_result(nlist):
    finalList = []
    splitval = "INPUT CURRENT"  # to arrange the output in an order
    for i in nlist:
        #  i = i + ","
        if ":" in i:
            i = i.split(":")
        else:
            i = i.split(" ")
        finalList.append(i)
        # done with extracting values from each line
    for l in finalList:
        a = open("output.csv", "a")
        a.write(str(l[1]) + ",")
        if splitval in l[0]:
            a.write("\n")


newList = []


def processlist(flst):
    words = ["UID [0-9]{5}", "CSQ:.{3}", "IMEI:.{15}", "CCID:.{20}", "VGSM:.*V", "SLEEP CURRENT:.*uA", "CHARGING CURRENT:.*mA", "CHARGE STATUS:.*",
             "CHARGER:.*", "ID:[0-9][0-9]", "TYPE:.{2}", "S/N:.{5}|S/N:", "VMCU:.*V", "INPUT CURRENT:.*mA"]  # putting all the words we need into a list in regex
    for l in flst:
        print(l)  # iterating through each line in the list
        for w in words:         # iterating all the words we need
            # searching if there is match and getting the value as output
            x = re.findall(w, str(l))
            if (len(x) == 1):
                x = ''.join(x)
                newList.append(x)


nameOfFile = sys.argv[1]    # passing the log file as the input
# Opening the log file for reading
fname = open(nameOfFile, "r", errors="ignore")
lines = fname.readlines()     # reading each line in the file
count = 0
flist = []
Startelement = "TESTREPORT,PASS"
endElement = "LP3 TEST PROCEDURE"
for i in range(len(lines)-1, -1, -1):  # to iterate the log file in an reversed format
    if Startelement in lines[i]:    # to check if Testreport,pass is present
        #  print(lines[i])
        # iterating to get all the elements from Startelement to endElement
        for j in range(115):
            count = count + 1          # To count the number of lines printed as output
            # print(lines[i-j])
            y = (lines[i-j])            # storing the output inside y
            flist.append(y)             # storing the output into a list
            # if the end element is found the loop breaks and then starts searching for the Startelement
            if endElement in lines[i-j]:
                break
if (count < 1):
    print("no successful test cases")
else:
    print("test run successful")
if (len(flist) > 1):
    processlist(flist)


# print(count)
# print(flist)
